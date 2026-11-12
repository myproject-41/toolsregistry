from abc import ABC,abstractmethod
from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class ToolsResult:
    success: bool
    output: Any = None
    error: Optional[str] = None

class Tool(ABC):
    "contract that everythool must follow"
    def __init__(self,name:str,description:str):
        if not name or " " in name or name != name.lower():
            raise ValueError("Tool name must be lowercase with no spaces")
        if not description:
            raise ValueError("Tool description cannot be empty")
        self.name = name
        self.description = description

    @abstractmethod
    def run(self,**kwargs) ->ToolsResult:
        " to do work. everyclass must be NotImplemented this"

    def info(self) ->dict:
        "shared helper: tool details as dictionary"
        return{"name":self.name, "description":self.description}
    
    

    
