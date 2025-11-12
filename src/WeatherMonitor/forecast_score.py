import re
from utils import load_json


def forecast_score(filename: str):
    """
    Load forecast data from a JSON file in the data directory and
    return a suitability score (0–100) for diving based on the last 3 days.
    Anything above 15 knots or 1m seas is considered unsafe.
    """
    forecasts = load_json(filename)
    if not forecasts:
        raise ValueError("Forecast data is empty")

    last_days = forecasts[-3:]  # last 3 days (or fewer)

    def parse_day(day):
        """Parse one day's conditions into numeric components."""
        winds = day.get("winds", "").lower()
        seas = day.get("seas", "").lower()
        weather = day.get("weather", "").lower()

        # --- Wind direction scoring (supports compound directions) ---
        direction_weights = {"e": 100, "n": 75, "w": 50, "s": 25}
        compound_map = {
            "northeast": ("n", "e"),
            "northwest": ("n", "w"),
            "southeast": ("s", "e"),
            "southwest": ("s", "w"),
        }

        dir_score = 50  # default neutral
        for comp, (d1, d2) in compound_map.items():
            if comp in winds:
                dir_score = (direction_weights[d1] + direction_weights[d2]) / 2
                break
        else:
            for key, val in direction_weights.items():
                if key in winds:
                    dir_score = val
                    break

        # --- Wind strength (knots) ---
        knots = [int(n) for n in re.findall(r"\b\d+\b", winds)]
        avg_knots = sum(knots) / len(knots) if knots else 10
        if avg_knots <= 10:
            wind_speed_score = 100
        elif avg_knots <= 15:
            wind_speed_score = 75
        else:
            wind_speed_score = 0  # above 15 knots = no go

        # --- Seas ---
        match = re.search(r"(\d+(?:\.\d+)?)\s*m", seas)
        sea_height = float(match.group(1)) if match else 1.0
        if sea_height <= 0.5:
            sea_score = 100
        elif sea_height <= 1:
            sea_score = 75
        else:
            sea_score = 0  # above 1m = no go

        # --- Weather ---
        if "sunny" in weather or "clear" in weather:
            weather_score = 100
        elif "partly cloudy" in weather:
            weather_score = 80
        elif "showers" in weather or "rain" in weather:
            weather_score = 40
        elif "thunderstorm" in weather:
            weather_score = 20
        else:
            weather_score = 70

        return {
            "dir_score": dir_score,
            "wind_speed_score": wind_speed_score,
            "sea_score": sea_score,
            "weather_score": weather_score,
            "winds": winds,
            "weather": weather,
            "avg_knots": avg_knots,
            "sea_height": sea_height,
        }

    parsed_days = [parse_day(d) for d in last_days]
    last = parsed_days[-1]

    # --- Base score for the last day ---
    base_score = (
        last["dir_score"] * 1.5 +
        last["wind_speed_score"] +
        last["sea_score"] +
        last["weather_score"]
    ) / 4.5

    # --- Adjustments from previous days ---
    adjustment = 0.0
    for prev in parsed_days[:-1]:
        if "east" in prev["winds"] or "north" in prev["winds"]:
            adjustment += 5
        if "south" in prev["winds"] or "west" in prev["winds"]:
            adjustment -= 5
        if prev["avg_knots"] >= 20:
            adjustment -= 10
        if "rain" in prev["weather"] or "showers" in prev["weather"]:
            adjustment -= 10
        if prev["avg_knots"] <= 10:
            adjustment += 3

    # --- Apply "no-go" overrides ---
    if last["avg_knots"] > 15 or last["sea_height"] > 1:
        final_score = 0
    else:
        final_score = min(max(round(base_score + adjustment, 1), 0), 100)

    return final_score
