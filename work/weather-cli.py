#!/usr/bin/env python3
"""weather-cli: Print current weather for a city via wttr.in."""

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://wttr.in/{}?format=j1"


def get_weather(city):
    url = API.format(urllib.parse.quote(city))
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as err:
        raise SystemExit(f"error: network issue reaching wttr.in: {err.reason}")
    except json.JSONDecodeError:
        raise SystemExit("error: could not parse weather data")
    return data


def main():
    parser = argparse.ArgumentParser(description="Show current weather for a city.")
    parser.add_argument("city", help="City to query (e.g. 'London')")
    args = parser.parse_args()

    if not args.city.strip():
        parser.error("missing city: provide a city name")

    data = get_weather(args.city)
    try:
        current = data["current_condition"][0]
        temp = current["temp_C"]
        condition = current["weatherDesc"][0]["value"]
        humidity = current["humidity"]
    except (KeyError, IndexError):
        raise SystemExit("error: unexpected weather data format")
    except TypeError:
        raise SystemExit("error: city not found")

    area = data.get("nearest_area", [{}])[0].get("areaName", [{}])[0].get("value", args.city)
    print(f"{area}: {temp}°C, {condition}, humidity {humidity}%")
    return 0


if __name__ == "__main__":
    sys.exit(main())