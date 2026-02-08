"""
py2mcu - Python to MCU C Compiler
"""

__version__ = "0.1.0"

from py2mcu.decorators import inline_c, arena, static_alloc

__all__ = ['inline_c', 'arena', 'static_alloc']
