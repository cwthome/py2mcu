# py2mcu - Python to MCU C Compiler

Write Python, test on PC, deploy to microcontrollers with automatic memory management.

## 📜 License

py2mcu is **dual-licensed**:

- **AGPLv3** - Free for open source projects, personal use, and education
- **Commercial License** - Required for proprietary/closed-source products

See [LICENSE_DUAL.md](LICENSE_DUAL.md) for details.

**Need a commercial license?** Contact: cwthome@gmail.com

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

## print() to printf() Conversion

py2mcu automatically converts Python's `print()` statements to C's `printf()`. The compiler detects the variable type (`int`, `float`, `str`) and uses the appropriate format specifier:

- `int` → `%d` or `%ld`
- `float` → `%f`
- `str` → `%s`

### Example

```python
temp: float = 23.5
print("Temperature:", temp)
```

Compiles to:
```c
float temp = 23.5;
printf("Temperature: %f\n", temp);
```

### PCs vs MCUs

- **PC target**: Uses standard `printf()` output
- **MCU target** (STM32/ESP32): Directs output to UART peripherals

## Examples

Check the `examples/` directory for complete demos:

- `demo1_led_blink.py` - Simple LED control
- `demo2_adc_average.py` - ADC reading with moving average
- `demo3_inline_c.py` - Inline C code for optimization

## Project Structure

```
py2mcu/
├── python_to_c/      # Core compiler
    ├── ast_parser.py
    ├── codegen.py
    ├── type_checker.py
    └── ...
├── runtime/          # Runtime libraries (memory management)
├── examples/         # Demo projects
├── tests/           # Unit tests
├── cli.py           # Command-line interface
└── README.md
```

## Roadmap

- [ X ] Basic type inference and C code generation
- [ X ] Automatic memory management
- [ X ] Inline C code support
- [ X ] Target macros for cross-platform compilation
- [ X ] Basic print() to printf() conversion
- [   ] Array and pointer support
- [   ] Struct and class support
- [   ] Full Standard Library emulation
- [   ] More MCU targets (RP2040, AVR, etc.)

## Contributing

Contributions welcome! Please open issues or submit PRs.

## License

py2mcu is dual-licensed under AGPLv3 (for open source) and a Commercial License (for proprietary use).

See [LICENSE_DUAL.md](LICENSE_DUAL.md) for complete licensing information.