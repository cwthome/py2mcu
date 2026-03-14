# py2mcu Test Plan

## 1. Overview

This test plan defines the testing strategy for py2mcu, a Python to MCU C compiler. The goal is to ensure reliable compilation of typed Python code to C for microcontrollers.

## 2. Test Scope

### In Scope
- Python to C translation accuracy
- Type annotation handling
- Inline C code generation
- Memory management decorators
- C preprocessor define generation
- Variable modifier support
- Cross-platform target compilation
- PC simulation execution

### Out of Scope
- MCU hardware testing
- Runtime performance profiling
- Third-party library integration

## 3. Test Types

### 3.1 Unit Tests

#### Parser Tests
| Test Case | Description |
|-----------|-------------|
| Parse simple function | Parse `def foo(): pass` |
| Parse typed function | Parse `def foo(x: int) -> bool:` |
| Extract @#define | Verify constant extraction |
| Extract variable modifiers | Test @const, @public, @volatile |
| Extract __C_CODE__ | Verify inline C extraction |

#### Type Checker Tests
| Test Case | Description |
|-----------|-------------|
| Resolve uint8_t | Type resolution for C types |
| Resolve list type | Array type inference |
| Type mismatch detection | Detect invalid assignments |
| Symbol table scope | Local vs global scope |

#### Code Generator Tests
| Test Case | Description |
|-----------|-------------|
| Emit function definition | C function signature generation |
| Emit while loop | Loop translation |
| Emit if statement | Conditional translation |
| Emit assignment | Variable assignment |
| Escape string literals | Test \n → \\n conversion |
| Handle print() | printf conversion |

### 3.2 Integration Tests

#### Compilation Workflow
| Test Case | Description |
|-----------|-------------|
| demo1_led_blink.py | Basic control flow compilation |
| demo2_adc_average.py | Array processing compilation |
| demo3_inline_c.py | Inline C compilation |
| demo4_memory.py | Memory management compilation |
| demo5_docstring_c.py | Docstring C code compilation |
| demo6_defines.py | Preprocessor defines compilation |

#### Build & Execute
| Test Case | Description |
|-----------|-------------|
| Compile demo1 to C | gcc build succeeds |
| Run demo1 on PC | Output matches expected |
| Compile demo4 with GC | gc_runtime linking works |

### 3.3 Target Platform Tests

| Target | Test |
|--------|------|
| pc | All demos compile, executable runs |
| stm32f4 | All demos compile (no execution) |
| esp32 | All demos compile (no execution) |
| rp2040 | All demos compile (no execution) |

## 4. Test Data

### Sample Programs

#### Simple Function
```python
def add(a: int, b: int) -> int:
    return a + b

def main():
    result: int = add(1, 2)
```

#### With Arrays
```python
def sum_array(arr: list, size: int) -> int:
    total: int = 0
    i: int = 0
    while i < size:
        total = total + arr[i]
        i = i + 1
    return total
```

#### With Inline C
```python
def fast_set(pin: int, value: bool) -> None:
    """__C_CODE__
    GPIOA->BSRR = (1 << pin);
    """
    print(f"Set pin {pin}")
```

#### With Defines
```python
LED_PIN = 13  # @#define uint8_t
MAX_SIZE = 100  # @#define
ENABLED = True  # @#define
```

## 5. Test Environment

### Requirements
- Python 3.8+
- GCC compiler
- Linux environment

### Setup
```bash
pip install -e .
```

## 6. Test Execution

### Run All Demos
```bash
for demo in demo1_led_blink demo2_adc_average demo3_inline_c demo4_memory demo5_docstring_c demo6_defines; do
    python -m py2mcu.cli compile examples/${demo}.py --target pc -o build/
    gcc -I runtime/ build/${demo}.c runtime/gc_runtime.c -o ${demo}
    ./${demo}
done
```

### Run Single Demo
```bash
python -m py2mcu.cli compile examples/demo1_led_blink.py --target pc -o build/
gcc -I runtime/ build/demo1_led_blink.c runtime/gc_runtime.c -o demo1_led_blink
./demo1_led_blink
```

## 7. Acceptance Criteria

### Must Pass
- [ ] All 6 demos compile to valid C
- [ ] All demos execute on PC without errors
- [ ] String escape sequences work correctly
- [ ] __C_CODE__ detection works (exact line match)
- [ ] @#define extraction works
- [ ] Variable modifiers generate correct C code

### Should Pass
- [ ] All target platforms compile (stm32f4, esp32, rp2040)
- [ ] Type annotations map correctly to C types
- [ ] Memory management decorators work

### Edge Cases
- [ ] Empty function bodies
- [ ] Nested loops
- [ ] Multiple __C_CODE__ in same file
- [ ] Combined variable modifiers (@public @const @volatile)
- [ ] f-strings in print()
- [ ] Multi-line string constants

## 8. Known Issues

See GitHub issues for current bugs and limitations.

## 9. Test Reporting

After each release:
1. Run all demo compilations
2. Execute PC builds
3. Verify output matches expected
4. Document any failures

## 10. Maintenance

- Add new tests for each feature addition
- Update acceptance criteria as features change
- Review and prune obsolete tests quarterly
