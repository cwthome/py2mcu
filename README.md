# py2mcu - Python to MCU C Compiler

Write Python, test on PC, deploy to microcontrollers with automatic memory management.

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
python -m py2mcu.cli compile examples/demo1_led_blink.py --target pc

# Or use the direct script
python py2mcu/cli.py compile examples/demo1_led_blink.py --target pc
```

### Option 2: Install as Package

```bash
pip install -e .
py2mcu compile examples/demo1_led_blink.py --target pc
```

### Hello World

```python
# hello.py
def main() -> None:
    print("Hello from py2mcu!")

if __name__ == "__main__":
    main()
```

Compile to C:
```bash
# Without installation
python -m py2mcu.cli compile hello.py --target pc

# With installation
py2mcu compile hello.py --target pc
```

## Type System

py2mcu supports standard C integer types as Python type annotations. Simply use C type names directly:

### Basic Example

```python
def uart_example() -> None:
    # unsigned char for UART transmission
    tx_byte: uint8_t = 0x41  # 'A'
    
    # buffer array (defined in inline C)
    __C_CODE__ = """
    uint8_t buffer[256];
    buffer[0] = tx_byte;
    """
    
def adc_example() -> None:
    # 8-bit ADC value
    adc_value: uint8_t = 0
    
    __C_CODE__ = """
    #ifdef TARGET_PC
        adc_value = rand() % 256;
    #else
        adc_value = HAL_ADC_GetValue(&hadc1) & 0xFF;
    #endif
    """
```

### Type Reference Table

| Python Annotation | C Type | Range |
|------------------|--------|-------|
| `uint8_t` | `uint8_t` | 0 ~ 255 |
| `uint16_t` | `uint16_t` | 0 ~ 65535 |
| `uint32_t` | `uint32_t` | 0 ~ 4294967295 |
| `int8_t` | `int8_t` | -128 ~ 127 |
| `int16_t` | `int16_t` | -32768 ~ 32767 |
| `int32_t` or `int` | `int32_t` | -2147483648 ~ 2147483647 |
| `float` | `float` | 32-bit floating point |
| `bool` | `bool` | true/false |

### Key Points

- **Use C type names directly** as Python type annotations
- py2mcu preserves these type names in generated C code
- `#include <stdint.h>` is automatically added
- Default `int` maps to `int32_t` (signed 32-bit)
- For unsigned 32-bit, explicitly use `uint32_t`

### Example

```python
byte: uint8_t = 255        # ✅ unsigned char (0-255)
value: int = -100          # ✅ int32_t (signed)
counter: uint32_t = 1000   # ✅ unsigned 32-bit
temperature: float = 25.5  # ✅ 32-bit float
```

## Target Platform Support

py2mcu uses a unified target macro system for cross-platform development:

### Compilation Targets

- `--target pc` → Generates `#define TARGET_PC 1` - Desktop simulation
- `--target stm32f4` → Generates `#define TARGET_STM32F4 1` - STM32F4 MCUs
- `--target esp32` → Generates `#define TARGET_ESP32 1` - ESP32 MCUs
- `--target arduino` → Generates `#define TARGET_ARDUINO 1` - Arduino boards

### Platform-Specific Code

Write code that adapts to the target platform using `#ifdef` directives:

```python
def read_sensor() -> int:
    """Read sensor value
    
    __C_CODE__
    #ifdef TARGET_PC
        return rand() % 1024;  // Simulate sensor on PC
    #elif defined(TARGET_STM32F4)
        HAL_ADC_Start(&hadc1);
        HAL_ADC_PollForConversion(&hadc1, HAL_MAX_DELAY);
        return HAL_ADC_GetValue(&hadc1);
    #elif defined(TARGET_ESP32)
        return analogRead(34);
    #endif
    """
    import random
    return random.randint(0, 1023)
```

### Development Workflow

1. **Develop and test on PC:**
   ```bash
   py2mcu compile my_code.py --target pc -o build/
   gcc build/my_code.c -o build/my_code
   ./build/my_code
   ```

2. **Deploy to target MCU:**
   ```bash
   py2mcu compile my_code.py --target stm32f4 -o build/
   # Use your MCU toolchain to build and flash
   ```

This unified approach enables rapid development on PC with immediate feedback, then seamless deployment to embedded targets.

## Architecture

```
Python Source → AST Parser → Type Checker → C Code Generator → MCU Compiler → Binary
```

## Memory Management

py2mcu uses a hybrid memory management strategy:

- **Stack allocation** for fixed-size types (int, float, small structs)
- **Arena allocator** for dynamic data (strings, lists, objects)
- **Reference counting** for automatic cleanup

## Examples

See `examples/` directory for complete examples:
- `demo1_led_blink.py` - Basic LED control
- `demo2_adc_average.py` - ADC reading with averaging
- `demo3_inline_c.py` - Inline C code usage

## Development Status

**Active Development** - Core features working, API may change

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please open an issue or PR.