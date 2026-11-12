from tools.base import Tool, ToolsResult


class ToolRegistry:
    def __init__(self):
        self._tools = {}  # name -> tool object

    def register(self, tool):
        if not isinstance(tool, Tool):
            raise TypeError("Only Tool objects can be registered")
        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' is already registered")
        self._tools[tool.name] = tool

    def get(self, name):
        if name not in self._tools:
            raise KeyError(f"Tool not found: {name}")
        return self._tools[name]

    def list_tools(self):
        return [tool.info() for tool in self._tools.values()]

    def run(self, name, /, **kwargs) -> ToolsResult:
        tool = self._tools.get(name)
        if tool is None:
            return ToolsResult(success=False, error=f"Unknown tool: {name}")
        try:
            return tool.run(**kwargs)
        except Exception as e:  # noqa: BLE001 - registry must survive any tool failure
            return ToolsResult(success=False, error=f"Tool '{name}' crashed: {e}")