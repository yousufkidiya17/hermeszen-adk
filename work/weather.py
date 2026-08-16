#!/usr/bin/env python3
"""weather.py — fetch current weather from wttr.in, no API key needed."""
import json
import sys
import urllib.request


def fetch(city):
    url = "https://wttr.in/{0}?format=j1".format(city or "")
    with urllib.request.urlopen(url, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    city = sys.argv[1] if len(sys.argv) > 1 else ""
    data = fetch(city)
    current = data["current_condition"][0]
    area = data["nearest_area"][0]["areaName"][0]["value"]
    country = data["nearest_area"][0]["country"][0]["value"]
    print("Weather for {0}, {1}".format(area, country))
    print("{0}  {1}°C (feels {2}°C)".format(
        current["weatherDesc"][0]["value"],
        current["temp_C"],
        current["FeelsLikeC"],
    ))
    print("Humidity: {0}%   Wind: {1} km/h {2}".format(
        current["humidity"], current["windspeedKmph"], current["winddir16Point"]
    ))
    if "localObsDateTime" in current:
        print("Observed at {0}".format(current["localObsDateTime"][:16]))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("Error fetching weather: {0}".format(exc), file=sys.stderr)
        sys.exit(1)