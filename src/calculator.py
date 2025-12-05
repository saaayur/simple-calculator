from __future__ import annotations
import ast
import operator
import sys

_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

class CalcError(Exception):
    pass

def _eval_node(node: ast.AST) -> float | int:
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    if isinstance(node, ast.Constant):
        val = node.value
        if isinstance(val, (int, float)):
            return val
        raise CalcError(f"Unsupported constant: {val!r}")

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in _BIN_OPS:
            try:
                return _BIN_OPS[op_type](left, right)
            except ZeroDivisionError:
                raise CalcError("Division by zero")
        raise CalcError("Unsupported operator")

    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type in _UNARY_OPS:
            return _UNARY_OPS[op_type](_eval_node(node.operand))
        raise CalcError("Unsupported unary operator")

    raise CalcError("Invalid input")

def evaluate_expression(expr: str):
    try:
        parsed = ast.parse(expr, mode="eval")
    except SyntaxError:
        raise CalcError("Invalid expression")

    return _eval_node(parsed)

def main():
    if len(sys.argv) > 1:
        expr = " ".join(sys.argv[1:])
        try:
            print(evaluate_expression(expr))
        except CalcError as e:
            print("Error:", e)
        return

    print("Simple Calculator — type 'exit' to quit.")
    while True:
        expr = input("calc> ").strip()
        if expr.lower() in ("exit", "quit"):
            break
        try:
            print(evaluate_expression(expr))
        except CalcError as e:
            print("Error:", e)

if __name__ == "__main__":
    main()
