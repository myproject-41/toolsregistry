from tools.weather import WeatherTool


def test_known_city():
    result = WeatherTool().run(city="Delhi")
    assert result.success is True
    assert result.output["temperature_c"] == 31


def test_city_is_case_and_space_insensitive():
    result = WeatherTool().run(city="  LONDON ")
    assert result.success is True


def test_unknown_city():
    result = WeatherTool().run(city="Atlantis")
    assert result.success is False


def test_empty_city():
    assert WeatherTool().run(city="").success is False


def test_missing_city():
    assert WeatherTool().run().success is False