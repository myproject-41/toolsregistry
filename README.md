# Tool Registry

A small backend that lets an AI agent call tools safely by name.

## Features
- Abstract `Tool` base class with a standard `ToolsResult` return type
- Tools: calculator (safe `ast` parsing, no `eval`), file reader (sandboxed, blocks path traversal), weather (fake data for now)
- `ToolRegistry`: register, list, and run tools; a crashing tool never crashes the system

## Run the demo
```bash
python main.py
```

## Run the tests
```bash
python -m pip install -r requirements.txt
python -m pytest -v
```

## Structure
```
tools/      base.py, calculator.py, weather.py, file_reader.py
tests/      one test file per component
sandbox/    the only folder the file reader may access
registry.py the ToolRegistry
main.py     demo script
```