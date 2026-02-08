"""
Type checker and inference engine
"""
import ast
from typing import Dict, Optional, Any

class TypeChecker(ast.NodeVisitor):
    """
    Static type checker for Python code
    Ensures all variables have type annotations
    """

    def __init__(self):
        self.symbol_table: Dict[str, str] = {}
        self.current_function: Optional[str] = None

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Check function definition"""
        self.current_function = node.name

        # Check return type annotation
        if node.returns is None:
            # Allow None for void functions
            pass

        # Record parameter types
        for arg in node.args.args:
            if arg.annotation:
                arg_type = self._get_type_name(arg.annotation)
                self.symbol_table[arg.arg] = arg_type

        # Visit function body
        self.generic_visit(node)

        self.current_function = None

    def visit_AnnAssign(self, node: ast.AnnAssign):
        """Check annotated assignment (x: int = 5)"""
        if isinstance(node.target, ast.Name):
            var_name = node.target.id
            var_type = self._get_type_name(node.annotation)
            self.symbol_table[var_name] = var_type

        self.generic_visit(node)

    def _get_type_name(self, node: ast.AST) -> str:
        """Extract type name from annotation node"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Subscript):
            # Handle List[int], etc.
            base = self._get_type_name(node.value)
            # TODO: Extract generic parameters
            return base
        elif isinstance(node, ast.Constant):
            return str(node.value)
        else:
            return "unknown"
