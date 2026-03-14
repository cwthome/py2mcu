"""
Decorators for py2mcu compiler hints
"""

def inline_c(c_code: str):
    """
    Decorator to embed inline C code

    Usage:
        @inline_c('''
        int fast_add(int a, int b) {
            return a + b;
        }
        ''')
        def add(a: int, b: int) -> int:
            return fast_add(a, b)
    """
    def decorator(func):
        func._inline_c = c_code
        def wrapper(*args, **kwargs):
            print(f"[PC SIM] {func.__name__}({', '.join(str(a) for a in args)})")
            import inspect
            from typing import get_origin, get_args
            sig = inspect.signature(func)
            ret_annotation = sig.return_annotation
            if ret_annotation is not None and ret_annotation is not inspect.Parameter.empty:
                origin = get_origin(ret_annotation)
                name = getattr(origin, '__name__', None) or getattr(ret_annotation, '__name__', None)
                if name == 'int':
                    return 0
                elif name == 'float':
                    return 0.0
                elif name == 'bool':
                    return False
                elif name == 'str':
                    return ""
            return None
        wrapper._inline_c = c_code
        return wrapper
    return decorator

def arena(func=None):
    """
    Context manager for arena memory allocation

    Usage:
        with arena():
            temp = large_computation()
        # temp is automatically freed
    """
    if func is None:
        # Used as context manager
        class ArenaContext:
            def __enter__(self):
                return self
            def __exit__(self, *args):
                pass
        return ArenaContext()
    else:
        # Used as decorator
        func._use_arena = True
        return func

def static_alloc(func):
    """
    Decorator to force static/stack allocation
    """
    func._static_alloc = True
    return func
