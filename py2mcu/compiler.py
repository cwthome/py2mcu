"""
Main compiler - Python to C translation
"""
import ast
from typing import Optional
from pathlib import Path

from py2mcu.parser import parse_python_file
from py2mcu.type_checker import TypeChecker
from py2mcu.codegen import CCodeGenerator

class Compiler:
    def __init__(self, target: str = 'pc', optimize: str = '2'):
        self.target = target
        self.optimize = optimize
        self.type_checker = TypeChecker()
        self.codegen = CCodeGenerator(target)

    def compile_file(self, filepath: str) -> str:
        """Compile a Python file to C code"""

        # Parse Python source
        tree = parse_python_file(filepath)

        # Type checking
        self.type_checker.visit(tree)

        # Code generation
        c_code = self.codegen.generate(tree)

        return c_code

    def compile_string(self, source: str) -> str:
        """Compile Python source string to C code"""
        tree = ast.parse(source)
        self.type_checker.visit(tree)
        c_code = self.codegen.generate(tree)
        return c_code
