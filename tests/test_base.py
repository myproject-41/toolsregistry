import pytest
from tools.base import Tool,ToolsResult

class GoodTool(Tool):
    def __init__(self):
        super().__init__(name ="good", description="A working test tool")

    def run(self,**kwargs) ->ToolsResult:
        return ToolsResult(success=True,output="ok")

def test_cannot_create_base_tool_directly():
     with pytest.raises(TypeError):
        Tool("x", "y")

def test_subclass_without_run_fails():
    class BadTool(Tool):
        pass

    with pytest.raises(TypeError):
        BadTool("bad", "has no run method")

def test_subclass_with_run_works():
    tool = GoodTool()
    result = tool.run()
    assert result.success is True
    assert result.output == "ok"

def info(self) -> dict:
    """Shared helper: tool details as a dictionary."""
    return {"name": self.name, "description": self.description}

def test_invalid_name_rejected():
    class SpacedTool(Tool):
        def __init__(self):
            super().__init__(name="Bad Name", description="x")

        def run(self, **kwargs) -> ToolsResult:
            return ToolsResult(success=True)

    with pytest.raises(ValueError):
        SpacedTool()