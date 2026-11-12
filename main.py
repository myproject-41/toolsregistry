from registry import ToolRegistry
from tools.calculator import CalculatorTool
from tools.file_reader import FileReaderTool
from tools.weather import WeatherTool


def main():
    registry = ToolRegistry()
    registry.register(CalculatorTool())
    registry.register(FileReaderTool())
    registry.register(WeatherTool())

    print("Available tools:")
    for info in registry.list_tools():
        print(f"  - {info['name']}: {info['description']}")

    print()
    print(registry.run("calculator", expression="25*4"))
    print(registry.run("weather", city="Delhi"))
    print(registry.run("file_reader", path="sample.txt"))
    print(registry.run("file_reader", path="../registry.py"))   # blocked
    print(registry.run("teleporter", where="Mars"))             # unknown tool


if __name__ == "__main__":
    main()