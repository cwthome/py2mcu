# py2mcu - Python to MCU C Compiler

[![Sponsor](https://img.shields.io/badge/Sponsor-GitHub%20Sponsors-ea4aaa?logo=github)](https://github.com/sponsors/wenchung)
[![Support](https://img.shields.io/badge/Support-Buy%20Me%20a%20Coffee-FFDD00?logo=buymeacoffee)](https://github.com/sponsors/wenchung)

Write Python, test on PC, deploy to microcontrollers with automatic memory management.

## 📜 License

py2mcu is **dual-licensed**:

- **AGPLv3** - Free for open source projects, personal use, and education
- **Commercial License** - Required for proprietary/closed-source products

See [LICENSE_DUAL.md](LICENSE_DUAL.md) for details.

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
| `uint32_t` | `uint32_t` | 0 ~ 4294967295 |
| `int8_t` | `int8_t` | -128 ~ 127 |
| `int16_t` | `int16_t` | -32768 ~ 32767 |
| `int32_t` | `int32_t` | -2147483648 ~ 2147483647 |
| `bool` | `bool` | TRUEL/FALSE |
| `float` | `float` | - |
| `double` | `double` | - |
| `None` | `void` | return type only |

## Cross-Platform Development

py2mcu uses target macros to enable unified development across PC and various MCUs.

### How to Define Target Macros?

**Method 1: Compiler flags (recommended)**
```bash
# For PC simulation (matches --target pc)
gcc -DTARGET_PC main.c -o main

# For STM32 (matches --target stm32)
arm-none-eabi-gcc -DTARGET_STM32 -DTARGETS_HARDWARE main.c -o main.elf

# For ESP32 (matches --target esp32)
xtensa-esp32-elf-gcc -DTARGET_ESP32 -DTARGETS_HARDWARE main.c -o main.elf
```

**Method 2: Define in code**
```c
#define TARGET_PC 1
// or
#define TARGET_STM32 1
// or
#define TARGET_ESP32 1
```

**Method 3: Using py2mcu CLI**
```bash
# Command line uses lowercase (easier to type)
py2mcu compile --target pc input.py
py2mcu compile --target stm32 input.py
py2mcu compile --target esp32 input.py

# Automatically generates uppercase macros (C convention)
# --target pc     → #define TARGET_PC 1
# --target stm32  → #define TARGET_STM32 1
# --target esp32  → #define TARGET_ESP32 1
```

### Target Macros

| Macro | Description | Use Case |
|-----|-----------|---------|
| `TARGETS_HARDWARE` | Defined when targeting any hardware (no PC) | Skip PC-specific code |
| `TARGETS_EMBEDDED` | Alias for `TARGETS_HARDWARE` | Alternative naming |
| `TARGETS_FMUCX_ENABLE` | Enable simulated FMUC for targets without FMUC (PC, RP2040) | Software FPU emulation |
| `TARGETS_PSEUDO_FINFO ` | Enable finfo-simulation where hardware FPU is available but `finfo` isn't | FPU info shim |

### Platform-Specific Macros

**Example: PC Target**
```bash
py2mcu compile --target pc input.py
```

Generated C code defines:
```c
#define TARGET_PC 1
```

**Example: STM32 Target**
```bash
py2mcu compile --target stm32 input.py
```

Generated C code defines:
```c
#define TARGET_STM32 1
#define TARGETS_HARDWARE 1
```

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## License

AGPLv3 - see [LICENSE](LICENSE) for details
Commercial License - contact fwthome@gmail.com
