from pathlib import Path

from tools.base import Tool, ToolsResult

MAX_BYTES = 100_000  # 100 KB limit


class FileReaderTool(Tool):
    def __init__(self, sandbox="sandbox"):
        super().__init__(
            name="file_reader",
            description="Reads a text file from the sandbox folder. Input: path (file name).",
        )
        self._sandbox = Path(sandbox).resolve()

    def run(self, **kwargs) -> ToolsResult:
        path = kwargs.get("path")

        if not isinstance(path, str) or not path.strip():
            return ToolsResult(success=False, error="path must be a non-empty string")

        target = (self._sandbox / path.strip()).resolve()

        if not target.is_relative_to(self._sandbox):
            return ToolsResult(success=False, error="Access denied: outside sandbox")

        if not target.exists():
            return ToolsResult(success=False, error="File not found")

        if not target.is_file():
            return ToolsResult(success=False, error="Path is not a file")

        if target.stat().st_size > MAX_BYTES:
            return ToolsResult(success=False, error="File too large")

        try:
            return ToolsResult(success=True, output=target.read_text(encoding="utf-8"))
        except UnicodeDecodeError:
            return ToolsResult(success=False, error="File is not readable as text")
        except OSError as e:
            return ToolsResult(success=False, error=f"Could not read file: {e}")