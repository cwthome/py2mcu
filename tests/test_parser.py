import ast
import pytest
from py2mcu.parser import (
    parse_python_file,
    parse_python_string,
    extract_define_constants,
    extract_variable_modifiers,
)


class TestExtractDefineConstants:
    def test_simple_define(self):
        source = "MAX_SIZE = 100  # @#define"
        result = extract_define_constants(source)
        assert len(result) == 1
        assert result[0]['name'] == 'MAX_SIZE'
        assert result[0]['value'] == '100'
        assert result[0]['type'] is None

    def test_define_with_type(self):
        source = "LED_PIN = 13  # @#define uint8_t"
        result = extract_define_constants(source)
        assert len(result) == 1
        assert result[0]['name'] == 'LED_PIN'
        assert result[0]['value'] == '13'
        assert result[0]['type'] == 'uint8_t'

    def test_multiple_defines(self):
        source = """
LED_PIN = 13  # @#define uint8_t
MAX_SIZE = 100  # @#define
DEBUG = True  # @#define
"""
        result = extract_define_constants(source)
        assert len(result) == 3
        assert result[0]['name'] == 'LED_PIN'
        assert result[1]['name'] == 'MAX_SIZE'
        assert result[2]['name'] == 'DEBUG'

    def test_define_with_expression(self):
        source = "TIMEOUT_MS = 1000 * 60  # @#define"
        result = extract_define_constants(source)
        assert len(result) == 1
        assert result[0]['value'] == '1000 * 60'

    def test_define_with_string(self):
        source = 'DEVICE_NAME = "py2mcu"  # @#define'
        result = extract_define_constants(source)
        assert len(result) == 1
        assert result[0]['value'] == '"py2mcu"'

    def test_no_define(self):
        source = "x = 10  # regular comment"
        result = extract_define_constants(source)
        assert len(result) == 0


class TestExtractVariableModifiers:
    def test_const_modifier(self):
        source = """# @const
config_version: uint32_t = 100"""
        result = extract_variable_modifiers(source, 2)
        assert result['const'] is True
        assert result['public'] is False
        assert result['volatile'] is False

    def test_public_modifier(self):
        source = """# @public
system_state: uint8_t = 0"""
        result = extract_variable_modifiers(source, 2)
        assert result['const'] is False
        assert result['public'] is True
        assert result['volatile'] is False

    def test_volatile_modifier(self):
        source = """# @volatile
isr_flag: uint8_t = 0"""
        result = extract_variable_modifiers(source, 2)
        assert result['const'] is False
        assert result['public'] is False
        assert result['volatile'] is True

    def test_combined_modifiers(self):
        source = """# @public @const
shared_config: uint32_t = 0xFF"""
        result = extract_variable_modifiers(source, 2)
        assert result['const'] is True
        assert result['public'] is True
        assert result['volatile'] is False

    def test_all_three_modifiers(self):
        source = """# @public @const @volatile
global_hw_config: uint32_t = 0xDEADBEEF"""
        result = extract_variable_modifiers(source, 2)
        assert result['const'] is True
        assert result['public'] is True
        assert result['volatile'] is True

    def test_no_modifier(self):
        source = """x: int = 10"""
        result = extract_variable_modifiers(source, 2)
        assert result['const'] is False
        assert result['public'] is False
        assert result['volatile'] is False

    def test_modifier_without_at_sign(self):
        source = """# const public
y: int = 20"""
        result = extract_variable_modifiers(source, 2)
        assert result['const'] is True
        assert result['public'] is True


class TestParsePythonString:
    def test_parse_simple_function(self):
        source = "def foo():\n    pass"
        tree = parse_python_string(source)
        assert isinstance(tree, ast.Module)
        assert len(tree.body) == 1
        assert isinstance(tree.body[0], ast.FunctionDef)

    def test_parse_typed_function(self):
        source = "def add(a: int, b: int) -> int:\n    return a + b"
        tree = parse_python_string(source)
        func = tree.body[0]
        assert func.name == 'add'
        assert len(func.args.args) == 2

    def test_source_attached(self):
        source = "def foo():\n    pass"
        tree = parse_python_string(source)
        assert hasattr(tree, '_source')
        assert tree._source == source

    def test_defines_attached(self):
        source = "MAX = 100  # @#define"
        tree = parse_python_string(source)
        assert hasattr(tree, 'py2mcu_defines')
        assert len(tree.py2mcu_defines) == 1
