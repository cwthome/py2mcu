# py2mcu - Agent Instructions

Python to MCU C Compiler with automatic memory management.

## Project Overview

py2mcu converts typed Python code to efficient C for microcontrollers:
- Python to C translation with type annotations
- Automatic memory management (arena allocator + reference counting)
- Inline C support via `__C_CODE__` markers in docstrings
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
python -m py2mcu.cli compile examples/demo1_led_blink.py --target pc -o build/

# With installation
py2mcu compile examples/demo1_led_blink.py --target pc -o build/
```

### Target Options
- `--target pc` → `#define TARGET_PC 1`
- `--target stm32f4` → `#define TARGET_STM32F4 1`
- `--target esp32` → `#define TARGET_ESP32 1`
- `--target rp2040` → `#define TARGET_RP2040 1`

### Build & Run (PC Testing)
```bash
py2mcu compile examples/demo1_led_blink.py --target pc -o build/
gcc -I runtime/ build/demo1_led_blink.c runtime/gc_runtime.c -o demo1_led_blink
./demo1_led_blink
```

### Direct Execution (PC Simulation)
```bash
python examples/demo1_led_blink.py
```

## Testing

### Run Unit Tests
```bash
# Install pytest first
pip install pytest

# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_parser.py -v

# Run single test
python -m pytest tests/test_parser.py::TestExtractDefineConstants::test_simple_define -v
```

### Run Examples
```bash
python examples/demo1_led_blink.py
python examples/demo3_inline_c.py
python examples/demo4_memory.py
```

### Test Compilation
```bash
# Compile all demos
for demo in demo1_led_blink demo2_adc_average demo3_inline_c demo4_memory demo5_docstring_c demo6_defines; do
    python -m py2mcu.cli compile examples/${demo}.py --target pc -o build/
done

# Build and run each
gcc -I runtime/ build/demo4_memory.c runtime/gc_runtime.c -o demo4_memory
./demo4_memory
```

## Code Style Guidelines

### General Rules
- **No comments** unless explicitly requested by user
- Use Python 3 type annotations throughout
- Keep functions focused and small (under 50 lines preferred)
- Use descriptive names for variables and functions

### Imports
- Standard library first, then third-party
- Use absolute imports: `from py2mcu import something`
- Avoid wildcard imports

### Naming Conventions
- Functions: `snake_case` (e.g., `parse_module`, `emit_statement`)
- Classes: `PascalCase` (e.g., `CCodeGenerator`, `TypeChecker`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `TARGET_PC`, `MAX_BUFFER_SIZE`)
- Variables: `snake_case` (e.g., `node`, `func_name`)

### Type Annotations
```python
# Function annotations
def process_data(items: list, threshold: int) -> bool:
    result: int = 0
    return True

# Supported C types as annotations:
uint8_t, uint16_t, int8_t, int16_t, uint32_t, int32_t, float, bool
```

### Error Handling
- Use exceptions for critical errors (parsing, compilation)
- Return `None` or empty collections for non-critical failures
- Include descriptive error messages

### Code Generation (codegen.py)
- Emit C code via `self.emit(line)` for proper indentation
- Use `_expr_to_c()` to convert Python expressions to C
- Handle `ast.Constant` specially for strings, numbers, bools
- Use `_escape_c_string()` to escape newlines/tabs in strings

### Parser/Extractor Patterns
- Extract patterns in `parser.py` using regex on source text
- Store extracted data in AST node attributes (e.g., `node._source`)
- Use `py2mcu_defines` attribute on Module for extracted defines

### Decorators
- `@inline_c(c_code)`: Wraps function for PC simulation (returns typed default)
- `@arena`: Context manager for bulk temporary allocations
- `@static_alloc`: Force stack allocation for small fixed buffers

### Key Patterns

#### 1. Inline C in Docstrings
The `__C_CODE__` marker must be on its own line:
```python
def gpio_write(pin: int, value: bool) -> None:
    """__C_CODE__
#ifdef TARGET_PC
    printf("GPIO %d: %s\\n", pin, value ? "HIGH" : "LOW");
#else
    HAL_GPIO_WritePin(GPIOA, (1 << pin), value ? GPIO_PIN_SET : GPIO_PIN_RESET);
#endif
    """
    print(f"GPIO {pin}: {'HIGH' if value else 'LOW'}")
```

#### 2. Module-Level C Code
```python
"""
__C_CODE__
#ifdef TARGET_PC
#include <time.h>
#endif
"""
```

#### 3. C Preprocessor Defines
```python
LED_PIN = 13  # @#define uint8_t
MAX_SIZE = 100  # @#define
```

#### 4. Global Variable Modifiers
```python
config_version: uint32_t = 100  # @const
system_state: uint8_t = 0  # @public
isr_flag: uint8_t = 0  # @volatile
```

## Gotchas

1. **Escape sequences**: Python AST evaluates `\n` to actual newline. Use `_escape_c_string()` in codegen to convert back to `\\n` for C.

2. **Target normalization**: Both `cli.py` and `codegen.py` normalize targets. Input `TARGET_PC`, `pc`, `PC` all become `pc`.

3. **`__C_CODE__` detection**: Must be exact line match `__C_CODE__`, not just containing text.

4. **Self-referencing assignments**: `count = count + 1` detected and emitted as assignment.

5. **GUI in demos**: Don't run GUI mainloop in separate thread - use `root.after()` for updates.

## File Structure
```
py2mcu/
├── py2mcu/
│   ├── __init__.py
│   ├── cli.py           # Click CLI
│   ├── compiler.py      # Main compiler orchestrator
│   ├── codegen.py       # C code generator (ast.NodeVisitor)
│   ├── parser.py        # AST parser
│   ├── type_checker.py  # Type checking
│   └── decorators.py    # @inline_c, @arena, @static_alloc
├── runtime/
│   ├── gc_runtime.c/h   # GC implementation
├── examples/
│   ├── demo*.py         # Example programs
├── README.md
├── AGENTS.md
└── hello.py
```

## License
Dual-licensed: AGPLv3 for open source, commercial license for proprietary use.
