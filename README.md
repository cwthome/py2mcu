# py2mcu - Python to MCU C Compiler

[![Sponsor](https://img.shields.io/badge/Sponsor-GitHub%20Sponsors-ea4aaa?logo=github)](https://github.com/sponsors/wenchung)
[![Support](https://img.shields.io/badge/Support-Buy%20Me%20a%20Coffee-FFDD00?logo=buymeacoffee)](https://github.com/sponsors/wenchung)

Write Python, test on PC, deploy to microcontrollers with automatic memory management.

## 📜 License

py2mcu is **dual-licensed**:

- **AGPLv3** - Free for open source projects, personal use, and education
- **Commercial License** - Required for proprietary/closed-source products

See [LICENSE](LICENSE) for details.

**Need a commercial license?** Contact: cwthome@gmail.com

---

## 💚 Support This Project

If py2mcu helps your work, consider sponsoring its development:

[![Sponsor on GitHub](https://img.shields.io/badge/Sponsor-GitHub%20Sponsors-ea4aaa?style=for-the-badge&logo=github)](https://github.com/sponsors/wenchung)

Your support helps maintain and improve py2mcu. Thank you! 🙏

---

## Features

- **Python to C Translation**: Converts typed Python code to efficient C
- **Automatic Memory Management**: Arena allocator + reference counting
- **Inline C Support**: Write performance-critical code directly in C
- **Cross-Platform Development**: Test on PC, deploy to MCU with unified target macros
- **Multiple MCU Support**: STM32, ESP32, RP2040, and more

## Quick Start

### Option 1: Direct Usage (No Installation Required)

```bash
# Clone the repository
git clone https://github.com/wenchung/py2mcu.git
cd py2mcu

# Run compiler directly

```bash
# the --target option is case‑insensitive and you can supply either the
# short name (e.g. `pc`) or the full macro name (`TARGET_PC`).  both forms
# generate identical output and the compiler will normalise the value for
# you.
python -m py2mcu.cli compile examples/demo1_led_blink.py --target TARGET_PC
```

# Or use the direct script
python py2mcu/cli.py compile examples/demo1_led_blink.py --target TARGET_PC

gcc -Iruntime/  build/demo1_led_blink.c runtime/gc_runtime.c

./a.out
```

### Option 2: Install as Package

```bash
pip install -e .
py2mcu compile examples/demo1_led_blink.py --target TARGET_PC

gcc -Iruntime/  build/demo1_led_blink.c runtime/gc_runtime.c

./a.out
```

### Hello World

```python
# hello.py
def main() -> int:
    """
    __C_CODE__
    printf("C:Hello from py2mcu!\n");
    return 0;
    """
    print("Hello from py2mcu!")
    return 0

if __name__ == "__main__":
    main()
```

Compile to C:
```bash
# Without installation
python -m py2mcu.cli compile hello.py

# With installation
py2mcu compile hello.py

gcc -Iruntime/ build/hello.c

./a.out

# Output
C:Hello from py2mcu!
```

## Type System
> **Tip:** if you want to inject a bit of raw C at the top of the generated
> file (for example to pull in an extra header when compiling for the PC
> simulator) you can put a module‑level string containing the
> `__C_CODE__` marker.  The compiler will copy the lines after the marker
> straight into the output immediately after the `#include` block.

py2mcu supports standard C integer types as Python type annotations. Simply use C type names directly:

### Basic Example

```python
def uart_example() -> None:
    # unsigned char for UART transmission
    tx_byte: uint8_t = 0x41  # 'A'
    
    # buffer array (defined in inline C)
    """
    __C_CODE__
    uint8_t buffer[256];
    buffer[0] = tx_byte;
    """
    
def adc_example() -> None:
    # 8-bit ADC value
    adc_value: uint8_t = 0
    """
    __C_CODE__
    #ifdef TARGET_PC
        adc_value = rand() & 256;
    #else
        adc_value = HAL_ADC_GetValue(&hadc1) & 0xFF;
    #endif
    """
```

### Type Reference Table

| Python Annotation | C Type | Range |
|-------------------|--------|-------|
| `uint8_t` | `uint8_t` | 0 ~ 255 |
| `uint16_t` | `uint16_t` | 0 ~ 65535 |
| `int8_t` | `int8_t` | -128 ~ 127 |
| `int16_t` | `int16_t` | -32768 ~ 32767 |
| `uint32_t` | `uint32_t` | 0 ~ 4294967295 |
| `int32_t` | `int32_t` | -2147483648 ~ 2147483647 |
| `float` | `float` | 32-bit floating point |

## Global Variable Modifiers

py2mcu supports C storage class and type qualifier modifiers for global variables through special comment annotations. Use `@const`, `@public`, and `@volatile` in comments to control how global variables are generated in C code.

### Modifier Overview

| Modifier | C Qualifier | Purpose |
|----------|-------------|---------|
| `@const` | `const` | Mark variable as read-only (stored in flash on MCUs) |
| `@public` | *(removes static)* | Make variable accessible across translation units |
| `@volatile` | `volatile` | Prevent compiler optimization for hardware/ISR access |

### Basic Usage

```python
# Static const variable (default: static, optimized)
config_version: uint32_t = 100  # @const

# Public variable accessible from other files
system_state: uint8_t = 0  # @public

# Volatile variable for ISR/hardware access
isr_flag: uint8_t = 0  # @volatile
```

**Generated C code:**

```c
static const uint32_t config_version = 100;
uint8_t system_state = 0;
static volatile uint8_t isr_flag = 0;
```

### Combining Modifiers

You can combine multiple modifiers in a single comment:

```python
# Public const configuration (accessible, read-only)
system_config: uint32_t = 0xFF00  # @public @const

# Public volatile flag for cross-file ISR sharing
shared_isr_counter: uint16_t = 0  # @public @volatile

# Const volatile hardware register access
hardware_status: uint8_t = 0  # @const @volatile

# All three modifiers combined
global_hw_config: uint32_t = 0xDEADBEEF  # @public @const @volatile
```

**Generated C code:**

```c
const uint32_t system_config = 0xFF00;
volatile uint16_t shared_isr_counter = 0;
static const volatile uint8_t hardware_status = 0;
const volatile uint32_t global_hw_config = 0xDEADBEEF;
```

### Modifier Combinations Reference

| Modifiers | Generated C | Use Case |
|-----------|-------------|----------|
| *(none)* | `static TYPE var` | Private variable with optimization |
| `@const` | `static const TYPE var` | Private read-only configuration |
| `@public` | `TYPE var` | Shared variable across files |
| `@volatile` | `static volatile TYPE var` | ISR flag or hardware register |
| `@public @const` | `const TYPE var` | Shared read-only configuration |
| `@public @volatile` | `volatile TYPE var` | Shared ISR/hardware access |
| `@const @volatile` | `static const volatile TYPE var` | Private hardware status register |
| `@public @const @volatile` | `const volatile TYPE var` | Shared hardware configuration register |

### Real-World Examples

#### Configuration Management

```python
# Firmware version (stored in flash, read-only)
FIRMWARE_VERSION: uint32_t = 0x010203  # @const

# Device ID (accessible from bootloader)
DEVICE_ID: uint32_t = 0x12345678  # @public @const
```

#### Interrupt Service Routines

```python
# Timer overflow counter (modified by ISR)
timer_overflow_count: uint32_t = 0  # @volatile

# Shared button press flag (ISR + main loop)
button_pressed: uint8_t = 0  # @public @volatile
```

#### Hardware Register Access

```python
# Memory-mapped status register (read-only, volatile)
STATUS_REG: uint32_t = 0x40000000  # @const @volatile

# Shared control register across modules
CONTROL_REG: uint32_t = 0x40000004  # @public @volatile
```

### Important Notes

1. **Order doesn't matter**: `@const @public` and `@public @const` generate identical code
2. **Case sensitive**: Use lowercase `@const`, not `@CONST` or `@Const`
3. **Comment placement**: Modifiers must be in a trailing comment on the same line
4. **Default behavior**: Without any modifiers, variables are `static` (private to file)
5. **Flash optimization**: `@const` variables are stored in flash memory on MCUs, saving RAM

### Migration from Static Variables

If you have existing code with static variables that need to be shared:

```python
# Before (private to file)
counter: uint32_t = 0

# After (accessible from other files)
counter: uint32_t = 0  # @public
```

## Target Macros

Use preprocessor macros to write portable code that runs on both PC and microcontrollers:

### Platform Detection

```python
__C_CODE__ = """
# Target macros are automatically defined:
#  - TARGET_PC   - when compiling for PC
#  - TARGET_Stm32 - when compiling for STM32
#  - TARGET_ESP32 - when compiling for ESP32
#  - TARGET_RP2040 - when compiling for RP2040
  
#ifdef TARGET_PC
    // PC-specific code
    printf("Running on PC\\n");
#elif defined(TARGET_STM_32)
    // STM36-specific code
    HAL_UART_Transmit(&uart2, (uint8_t*)"Running on STM32\\n", ...);
#elif defined(TARGET_ESP32)
    // ESP32-specific code
    printf("Running on ESP32\\n");
#elif defined(TARGET_RP2040)
    // RP2040-specific code
    printf("Running on RP2040\\n");
#endif
"""
```

## How to Define Target Macros

### CMakeLists.txt

```cmake
add_definitions(-DTARGET_STM32)
```

### Makefile

```make
CFLAGS += -DTARGET_STM32
```

### PlatformIO Platform.ini

```ini
build_flags = -DTARGET_ESP32
```

### GCC Command Line

```bash
gcc -DTARGET_PP2040 output.c -o output
```
