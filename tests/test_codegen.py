import pytest
from py2mcu.compiler import Compiler


class TestCodegen:
    def setup_method(self):
        self.compiler = Compiler(target='pc')

    def test_simple_function(self):
        source = """
def add(a: int, b: int) -> int:
    return a + b
"""
        c_code = self.compiler.compile_string(source)
        assert 'int32_t add(int32_t a, int32_t b)' in c_code

    def test_void_function(self):
        source = """
def foo() -> None:
    x: int = 1
"""
        c_code = self.compiler.compile_string(source)
        assert 'void foo(void)' in c_code

    def test_main_function(self):
        source = """
def main() -> None:
    x: int = 1
"""
        c_code = self.compiler.compile_string(source)
        assert 'int main(void)' in c_code

    def test_while_loop(self):
        source = """
def loop() -> None:
    i: int = 0
    while i < 10:
        i = i + 1
"""
        c_code = self.compiler.compile_string(source)
        assert 'while' in c_code
        assert '(i < 10)' in c_code

    def test_if_statement(self):
        source = """
def check(x: int) -> bool:
    if x > 0:
        return True
    return False
"""
        c_code = self.compiler.compile_string(source)
        assert 'if' in c_code
        assert '(x > 0)' in c_code

    def test_array_assignment(self):
        source = """
def foo() -> None:
    arr: list = [0] * 10
    arr[0] = 5
"""
        c_code = self.compiler.compile_string(source)
        assert 'arr[0] = 5' in c_code

    def test_print_string(self):
        source = """
def foo() -> None:
    print("Hello")
"""
        c_code = self.compiler.compile_string(source)
        assert 'printf' in c_code
        assert 'Hello' in c_code

    def test_print_with_newline_escape(self):
        source = """
def foo() -> None:
    print("Hello\\nWorld")
"""
        c_code = self.compiler.compile_string(source)
        assert 'printf' in c_code
        assert 'Hello\\nWorld' in c_code

    def test_print_variable(self):
        source = """
def foo() -> None:
    x: int = 10
    print(x)
"""
        c_code = self.compiler.compile_string(source)
        assert 'printf' in c_code
        assert '%d' in c_code


class TestDefines:
    def setup_method(self):
        self.compiler = Compiler(target='pc')

    def test_define_generation(self):
        source = """
LED_PIN = 13  # @#define uint8_t
MAX_SIZE = 100  # @#define
"""
        c_code = self.compiler.compile_string(source)
        assert '#define LED_PIN' in c_code
        assert '#define MAX_SIZE' in c_code

    def test_define_with_type(self):
        source = """
LED_PIN = 13  # @#define uint8_t
"""
        c_code = self.compiler.compile_string(source)
        assert '#define LED_PIN ((uint8_t)13)' in c_code

    def test_define_bool_true(self):
        source = """
DEBUG = True  # @#define
"""
        c_code = self.compiler.compile_string(source)
        assert '#define DEBUG 1' in c_code

    def test_define_bool_false(self):
        source = """
DEBUG = False  # @#define
"""
        c_code = self.compiler.compile_string(source)
        assert '#define DEBUG 0' in c_code


class TestInlineC:
    def setup_method(self):
        self.compiler = Compiler(target='pc')

    def test_c_code_in_docstring(self):
        source = """
def gpio_write(pin: int, value: bool) -> None:
    \"\"\"__C_CODE__
    GPIOA->BSRR = (1 << pin);
    \"\"\"
    print("done")
"""
        c_code = self.compiler.compile_string(source)
        assert 'GPIOA->BSRR' in c_code
        assert '#define TARGET_PC 1' in c_code

    def test_c_code_preserves_exact_line_match(self):
        source = """
def foo() -> None:
    \"\"\"This demonstrates __C_CODE__ usage in text.
    __C_CODE__
    int x = 1;
    \"\"\"
    pass
"""
        c_code = self.compiler.compile_string(source)
        assert 'int x = 1' in c_code

    def test_module_level_c_code(self):
        source = """
\"\"\"
__C_CODE__
#include <time.h>
\"\"\"
"""
        c_code = self.compiler.compile_string(source)
        assert '#include <time.h>' in c_code


class TestVariableModifiers:
    def setup_method(self):
        self.compiler = Compiler(target='pc')

    def test_const_modifier(self):
        source = """
# @const
config_version: uint32_t = 100
"""
        c_code = self.compiler.compile_string(source)
        assert 'static const uint32_t config_version' in c_code

    def test_public_modifier(self):
        source = """
# @public
system_state: uint8_t = 0
"""
        c_code = self.compiler.compile_string(source)
        assert 'uint8_t system_state' in c_code

    def test_volatile_modifier(self):
        source = """
# @volatile
isr_flag: uint8_t = 0
"""
        c_code = self.compiler.compile_string(source)
        assert 'static volatile uint8_t isr_flag' in c_code


class TestTargets:
    def setup_method(self):
        self.compiler = Compiler(target='pc')

    def test_pc_target(self):
        source = "def main() -> None:\n    pass"
        c_code = self.compiler.compile_string(source)
        assert '#define TARGET_PC 1' in c_code

    def test_stm32f4_target(self):
        compiler = Compiler(target='stm32f4')
        source = "def main() -> None:\n    pass"
        c_code = compiler.compile_string(source)
        assert '#define TARGET_STM32F4 1' in c_code

    def test_esp32_target(self):
        compiler = Compiler(target='esp32')
        source = "def main() -> None:\n    pass"
        c_code = compiler.compile_string(source)
        assert '#define TARGET_ESP32 1' in c_code

    def test_target_case_insensitive(self):
        compiler1 = Compiler(target='PC')
        compiler2 = Compiler(target='pc')
        compiler3 = Compiler(target='TARGET_PC')
        source = "def main() -> None:\n    pass"
        c1 = compiler1.compile_string(source)
        c2 = compiler2.compile_string(source)
        c3 = compiler3.compile_string(source)
        assert '#define TARGET_PC 1' in c1
        assert '#define TARGET_PC 1' in c2
        assert '#define TARGET_PC 1' in c3
