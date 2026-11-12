import ast
import operator

from tools.base import Tool, ToolsResult

# Map allowed operator types to the real Python functions that do the math
ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,   # negative numbers like -5
}

MAX_EXPONENT = 100  # blocks things like 9**9**9


class CalculatorTool(Tool):
    def __init__(self):
        super().__init__(
            name="calculator",
            description="Evaluates a math expression such as '25*4' or '(2+3)**2'.",
        )

    def run(self, **kwargs) -> ToolsResult:
        expression = kwargs.get("expression")

        if not isinstance(expression, str) or not expression.strip():
            return ToolsResult(success=False, error="expression must be a non-empty string")

        try:
            tree = ast.parse(expression.strip(), mode="eval")
            value = self._evaluate(tree.body)
            return ToolsResult(success=True, output=value)
        except ZeroDivisionError:
            return ToolsResult(success=False, error="Division by zero")
        except (SyntaxError, ValueError) as e:
            return ToolsResult(success=False, error=f"Invalid expression: {e}")

    def _evaluate(self, node):
        # A plain number like 25 or 3.5
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
                return node.value
            raise ValueError("only numbers are allowed")

        # Two numbers with an operator, like 25 * 4
        if isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in ALLOWED_OPERATORS:
                raise ValueError("operator not allowed")
            left = self._evaluate(node.left)
            right = self._evaluate(node.right)
            if op_type is ast.Pow and abs(right) > MAX_EXPONENT:
                raise ValueError("exponent too large")
            return ALLOWED_OPERATORS[op_type](left, right)

        # A negative number like -5
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return ALLOWED_OPERATORS[ast.USub](self._evaluate(node.operand))

        # Everything else (names, function calls, strings...) is rejected
        raise ValueError("unsupported expression")