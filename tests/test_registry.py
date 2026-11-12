import pytest

from registry import ToolRegistry
from tools.base import Tool, ToolsResult
from tools.calculator import CalculatorTool


class CrashTool(Tool):
    """Fake tool that always crashes, to test the safety net."""

    def __init__(self):
        super().__init__(name="crash", description="Always crashes")

    def run(self, **kwargs) -> ToolsResult:
        raise RuntimeError("boom")


def test_register_and_get():
    registry = ToolRegistry()
    calc = CalculatorTool()
    registry.register(calc)
    assert registry.get("calculator") is calc


def test_duplicate_name_rejected():
    registry = ToolRegistry()
    registry.register(CalculatorTool())
    with pytest.raises(ValueError):
        registry.register(CalculatorTool())


def test_non_tool_rejected():
    registry = ToolRegistry()
    with pytest.raises(TypeError):
        registry.register("not a tool")


def test_get_unknown_raises():
    with pytest.raises(KeyError):
        ToolRegistry().get("missing")


def test_run_unknown_tool_returns_error():
    result = ToolRegistry().run("missing", expression="1+1")
    assert result.success is False
    assert "Unknown tool" in result.error


def test_run_calculator_through_registry():
    registry = ToolRegistry()
    registry.register(CalculatorTool())
    result = registry.run("calculator", expression="25*4")
    assert result.success is True
    assert result.output == 100


def test_crashing_tool_does_not_crash_registry():
    registry = ToolRegistry()
    registry.register(CrashTool())
    result = registry.run("crash")
    assert result.success is False
    assert "boom" in result.error


def test_list_tools():
    registry = ToolRegistry()
    registry.register(CalculatorTool())
    names = [t["name"] for t in registry.list_tools()]
    assert names == ["calculator"]