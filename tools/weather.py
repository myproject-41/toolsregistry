from tools.base import Tool, ToolsResult

FAKE_WEATHER = {
    "delhi": {"temperature_c": 31, "conditions": "Sunny"},
    "mumbai": {"temperature_c": 29, "conditions": "Humid"},
    "london": {"temperature_c": 12, "conditions": "Cloudy"},
}


class WeatherTool(Tool):
    def __init__(self):
        super().__init__(
            name="weather",
            description="Gets current weather for a city. Input: city (name).",
        )

    def run(self, **kwargs) -> ToolsResult:
        city = kwargs.get("city")

        if not isinstance(city, str) or not city.strip():
            return ToolsResult(success=False, error="city must be a non-empty string")

        data = FAKE_WEATHER.get(city.strip().lower())
        if data is None:
            return ToolsResult(success=False, error=f"No weather data for '{city}'")

        return ToolsResult(success=True, output={"city": city.strip(), **data})