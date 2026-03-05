# py2mcu - Agent Instructions

Python to MCU C Compiler with automatic memory management.

## Project Overview

py2mcu converts typed Python code to efficient C for microcontrollers. Key features:
- Python to C translation with type annotations
- Automatic memory management (arena allocator + reference counting)
- Inline C support via `__C_CODE__` markers
- Cross-platform development (test on PC, deploy to MCU)
- Multiple MCU support (STM32, ESP32, RP2040)

## Essential Commands

### Installation
```bash
pip install -e .
```

### Compilation
```bash
# Without installation
python -m py2mcu.cli compile examples/demo1_led_blink.py --target pc

# With installation
py2mcu compile examples/demo1_led_blink.py --target pc -o build/
```

### Target Options
- `--target pc` → `#define TARGET_PC 1`
- `--target stm32f4` → `#define TARGET_STM32F4 1`
- `--target esp32` → `#define TARGET_ESP32 1`
- `--target rp2040` → `#define TARGET_RP2040 1`

Target is case-insensitive: `pc`, `PC`, `TARGET_PC` all normalize to same value.

### Build & Run (PC Testing)
```bash
py2mcu compile examples/demo1_led_blink.py --target pc -o build/
gcc -Iruntime/ build/demo1_led_blink.c runtime/gc_runtime.c -o build/demo1_led_blink
./build/demo1_led_blink
```

### Direct Execution (PC Simulation)
```bash
python examples/demo1_led_blink.py
```

## Code Organization

### Core Modules (`py2mcu/`)
- `cli.py` - Click-based CLI with `compile`, `run`, `deploy` commands
- `compiler.py` - Main compiler orchestrating parsing, type checking, codegen
- `parser.py` - Python AST parsing, extracts `@#define` and variable modifiers
- `codegen.py` - C code generation from AST (inherits `ast.NodeVisitor`)
- `type_checker.py` - Static type checking, symbol table management
- `decorators.py` - `@inline_c`, `@arena`, `@static_alloc` decorators

### Runtime (`runtime/`)
- `gc_runtime.c/h` - GC runtime with `gc_malloc()` and `gc_free()`

### Examples (`examples/`)
- `demo1_led_blink.py` - Basic control flow, GPIO
- `demo2_adc_average.py` - Array processing
- `demo3_inline_c.py` - Performance optimization
- `demo4_memory.py` - Memory management strategies
- `demo5_docstring_c.py` - Docstring embedded C
- `demo6_defines.py` - Preprocessor defines

## Key Patterns

### 1. Inline C via `__C_CODE__`

**In function docstrings:**
```python
def delay_ms(ms: int) -> None:
    """__C_CODE__
    #ifdef TARGET_PC
    struct timespec ts;
    ts.tv_sec = ms / 1000;
    nanosleep(&ts, NULL);
    #else
    uint32_t start = HAL_GetTick();
    while ((HAL_GetTick() - start) < ms) { __NOP(); }
    #endif
    """
    import time
    time.sleep(ms / 1000.0)
```

**As expression statements:**
```python
"""
__C_CODE__
volatile uint32_t* register_ptr = (uint32_t*)0x40020000;
"""
```

**Module-level:**
```python
"""
__C_CODE__
#ifdef TARGET_PC
    #include <time.h>
#endif
"""
```

### 2. Type Annotations

Use C type names directly:
```python
def process(data: uint8_t, count: int32_t) -> bool:
    value: uint16_t = 0
    return True
```

Supported types: `uint8_t`, `uint16_t`, `int8_t`, `int16_t`, `uint32_t`, `int32_t`, `float`, `bool`

### 3. C Preprocessor Defines

Mark constants with `# @#define`:
```python
LED_PIN = 13  # @#define uint8_t
MAX_SAMPLES = 100  # @#define
TIMEOUT_MS = 1000 * 60  # @#define
DEBUG_ENABLED = True  # @#define
DEVICE_NAME = "py2mcu"  # @#define
```

Generates:
```c
#define LED_PIN ((uint8_t)13)
#define MAX_SAMPLES 100
#define TIMEOUT_MS (1000 * 60)
#define DEBUG_ENABLED 1
#define DEVICE_NAME "py2mcu"
```

### 4. Global Variable Modifiers

Use comment annotations for storage class:
```python
# @const
config_version: uint32_t = 100  # static const

system_state: uint8_t = 0  # @public  # removes static

isr_flag: uint8_t = 0  # @volatile  # static volatile

# @public @const
shared_config: uint32_t = 0xFF  # const (no static)

# @public @volatile
shared_isr_flag: uint8_t = 0  # volatile (no static)
```

Modifiers: `@const`, `@public`, `@volatile` (case-sensitive, lowercase)

### 5. Platform-Specific Code

Use target macros in `__C_CODE__`:
```python
def gpio_write(pin: int, value: bool) -> None:
    """__C_CODE__
    #ifdef TARGET_PC
    printf("GPIO Pin %d: %s\n", pin, value ? "HIGH" : "LOW");
    #else
    if (value) {
        GPIOA->BSRR = (1 << pin);
    } else {
        GPIOA->BSRR = (1 << (pin + 16));
    }
    #endif
    """
    print(f"GPIO Pin {pin}: {'HIGH' if value else 'LOW'}")
```

### 6. Main Function

```python
def main() -> None:
    setup()
    while True:
        loop()
```

Generates `int main(void)` for PC (with implicit `return 0`), `void main(void)` for MCU targets.

## Code Generation Rules

### Preprocessor Directives
Lines starting with `#` in `__C_CODE__` are emitted at column 0 (no indentation).

### Final Newline
Generated C files always end with a trailing newline.

### Includes
Always includes `gc_runtime.h`. PC target adds `time.h` for `nanosleep`.

### Module-Level C Code
Treated in source order (not hoisted). Conditional blocks stay positioned correctly.

### Undefined Names
Expression statements using undefined names are skipped (e.g., GUI calls in PC simulation).

## Testing Patterns

1. Write Python code that runs on PC for testing
2. Use `__C_CODE__` for MCU-specific optimizations
3. Use `#ifdef TARGET_PC` for platform branching
4. Test with `python examples/demo*.py` before compiling

## Gotchas

1. **Escape sequences in docstrings**: AST evaluates strings, so `\n` becomes newline. Parser stores raw source to recover original escapes for C code.

2. **Target normalization**: Both `cli.py` and `codegen.py` normalize target names. Input `TARGET_PC`, `pc`, `PC` all become `pc` internally with macro `TARGET_PC`.

3. **`if __name__ == "__main__"` blocks**: Skipped during code generation (main() function already exists).

4. **Self-referencing assignments**: `count = count + 1` is detected and emitted as assignment, not re-declaration.

5. **Variable modifiers**: Must be in comment on line above declaration, not same line.

6. **Memory management**: 
   - `@static_alloc` for small fixed-size stack data
   - `@arena` for temporary bulk allocations
   - Default: reference counting for persistent data

## File Structure

```
py2mcu/
├── py2mcu/
│   ├── __init__.py
│   ├── cli.py           # Click CLI
│   ├── compiler.py      # Main compiler
│   ├── codegen.py       # C code generator
│   ├── parser.py        # AST parser
│   ├── type_checker.py  # Type checking
│   └── decorators.py    # Memory decorators
├── runtime/
│   ├── gc_runtime.c     # GC implementation
│   └── gc_runtime.h     # GC header
├── examples/
│   ├── demo*.py         # Example programs
│   └── test_output/     # GIF outputs
├── setup.py             # Package setup
├── README.md            # Main docs
└── hello.py             # Hello world example
```

## Build Pipeline

1. Parse Python source → AST (with `_source` attached)
2. Extract `@#define` constants and variable modifiers
3. Type check AST (build symbol table)
4. Generate C code:
   - Add includes + target macro
   - Add `#define` directives
   - Include `gc_runtime.h`
   - Visit AST nodes (functions, globals, expressions)
5. Output to `build/<filename>.c`

## License

Dual-licensed: AGPLv3 for open source, commercial license for proprietary use. Contact: cwthome@gmail.com