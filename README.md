# py2mcu - Python to Microcontroller Compiler

**py2mcu** is a specialized Python-to-C compiler designed for resource-constrained microcontrollers (MCUs). It translates a subset of Python into efficient C code with automatic memory management, making embedded development more accessible without sacrificing performance.

---

## Features

### 🚀 Core Capabilities
- **Python-to-C Translation**: Compiles Python functions decorated with `@mcu_function` into optimized C code
- **Automatic Memory Management**: Built-in garbage collector using Arena allocation + Reference Counting
- **Type Inference**: Automatically determines variable types from usage patterns
- **Inline C Support**: Use `@inline_c` for performance-critical sections (GPIO, DMA, etc.)

### 🎯 Why py2mcu?
- Write embedded code in Python syntax
- Automatic memory safety (no manual malloc/free)
- Seamless integration with existing C libraries
- Optimized for MCU constraints (RAM, Flash, CPU)

---

## Installation

```bash
pip install py2mcu
```

---

## Quick Start

### Example: LED Blink (Demo 1)

```python
from py2mcu import mcu_function

@mcu_function
def blink_led(pin: int, times: int) -> None:
    """Blink LED using Python control flow"""
    for i in range(times):
        gpio_set(pin, 1)
        delay_ms(500)
        gpio_set(pin, 0)
        delay_ms(500)
```

**Compile to C:**
```bash
py2mcu compile examples/demo1_led_blink.py -o build/demo1.c
```

---

## Architecture

### Compiler Pipeline
```
Python Source → AST Parser → Type Checker → Code Generator → C Output
                                                ↓
                                        GC Runtime (Arena + RefCount)
```

### Memory Management
- **Arena Allocator**: Fast bump-pointer allocation for short-lived objects
- **Reference Counting**: Automatic cleanup when objects are no longer used
- **Manual Control**: `gc_collect()` for explicit cleanup in tight loops

---

## Demo Examples

| Demo | Description | Key Features |
|------|-------------|-------------|
| **demo1_led_blink.py** | LED blinking with delays | Basic control flow, loops |
| **demo2_adc_average.py** | ADC sampling with moving average | Arrays, arithmetic operations |
| **demo3_inline_c.py** | High-speed GPIO toggling | Inline C for performance |
| **demo4_memory.py** | Memory management showcase | Arena allocation, ref counting |

Run examples:
```bash
py2mcu compile examples/demo1_led_blink.py
py2mcu deploy build/demo1.c --port /dev/ttyUSB0
```

---

## Command-Line Interface

```bash
# Compile Python to C
py2mcu compile input.py -o output.c

# Compile + Deploy to MCU
py2mcu deploy output.c --port /dev/ttyUSB0 --board arduino_uno

# Show generated C code
py2mcu compile input.py --show
```

---

## Limitations

⚠️ **Currently Unsupported:**
- Object-oriented programming (classes)
- Dynamic typing (variables must have consistent types)
- Recursion (limited stack on MCUs)
- String manipulation (minimal support)

---

## Roadmap

- [ ] STM32 HAL integration
- [ ] ESP32 FreeRTOS support
- [ ] Interrupt handler decorators
- [ ] DMA buffer management
- [ ] RTOS task scheduling

---

## Contributing

Contributions welcome! Please check [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Author

Developed for embedded developers who want Python's simplicity with C's performance. 🚀
