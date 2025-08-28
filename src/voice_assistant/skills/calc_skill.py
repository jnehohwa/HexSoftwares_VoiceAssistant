import ast
import operator as op
import math
from .base import Skill

ALLOWED = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
    ast.BitXor: op.xor,
    ast.BitAnd: op.and_,
    ast.BitOr: op.or_,
    ast.LShift: op.lshift,
    ast.RShift: op.rshift,
}

# Add math functions
MATH_FUNCTIONS = {
    'sqrt': math.sqrt,
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'log': math.log,
    'log10': math.log10,
    'abs': abs,
    'round': round,
    'floor': math.floor,
    'ceil': math.ceil,
}

def _eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if hasattr(ast, "Num") and isinstance(node, getattr(ast, "Num")):  # legacy
        return node.n
    if isinstance(node, ast.BinOp):
        fn = ALLOWED.get(type(node.op))
        if not fn:
            raise ValueError("Operator not allowed")
        return fn(_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp):
        fn = ALLOWED.get(type(node.op))
        if not fn:
            raise ValueError("Operator not allowed")
        return fn(_eval(node.operand))
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name in MATH_FUNCTIONS:
                if len(node.args) == 1:
                    return MATH_FUNCTIONS[func_name](_eval(node.args[0]))
                else:
                    raise ValueError(f"Function {func_name} expects 1 argument")
        raise ValueError("Function calls not allowed")
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    raise ValueError("Unsupported expression")

class CalcSkill(Skill):
    def names(self):
        return ["calc", "math"]

    def handle(self, cmd: str, args: str) -> str:
        if not args:
            return "Usage: calc <expression>"
        try:
            tree = ast.parse(args, mode="eval")
            val = _eval(tree)
            return str(val)
        except Exception as e:
            return f"Invalid expression: {e}"
