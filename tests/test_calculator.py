from tools.calculator import CalculatorTool

def test_basic_multiplication():
    result = CalculatorTool().run(expression="25*4")
    assert result.success is True
    assert result.output == 100

def test_parentheses_and_precedence():
    assert CalculatorTool().run(expression="(2+3)*4").output == 20
    assert CalculatorTool().run(expression="2+3*4").output == 14

def test_negative_number():
    assert CalculatorTool().run(expression="-5 + 2").output == -3

def test_division_by_zero():
    result = CalculatorTool().run(expression="1/0")
    assert result.success is False
    assert "zero" in result.error.lower()

def test_empty_expression():
    assert CalculatorTool().run(expression="").success is False

def test_missing_expression():
    assert CalculatorTool().run().success is False

def test_dangerous_input_rejected():
    result = CalculatorTool().run(expression="__import__('os').system('echo hi')")
    assert result.success is False

def test_malformed_expression():
    assert CalculatorTool().run(expression="2+").success is False

def test_huge_exponent_rejected():
    assert CalculatorTool().run(expression="9**9**9").success is False