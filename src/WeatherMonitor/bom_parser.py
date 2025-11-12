import re
import json
from typing import List, Dict

def clean_footer(text: str) -> str:
    """Remove trailing BOM footer / copyright information."""
    footer_markers = [
        "The next routine forecast will be issued",
        "Check the latest Coastal Waters Forecast",
        "Copyright Commonwealth of Australia"
    ]
    for marker in footer_markers:
        idx = text.find(marker)
        if idx != -1:
            text = text[:idx]
            break
    return text.strip()


def parse_forecast_sections(text: str) -> List[Dict[str, str]]:
    text = clean_footer(text)  # 🧹 remove footer first

    section_re = re.compile(
        r"Forecast for ([A-Za-z]+\s+\d{1,2}\s+\w+)[^\n]*\n(.*?)(?=Forecast for|$)",
        re.DOTALL
    )
    matches = section_re.findall(text)

    results = []
    for day, body in matches:
        clean = re.sub(r"\s+\n", "\n", body.strip())
        clean = re.sub(r"\n{2,}", "\n", clean)

        winds_match = re.search(r"Winds:\s*(.*?)(?=\s+[A-Z][a-z]+:|$)", clean, re.DOTALL)
        seas_match = re.search(r"Seas:\s*(.*?)(?=\s+[A-Z][a-z]+:|$)", clean, re.DOTALL)
        weather_match = re.search(r"Weather:\s*(.*?)(?=\s+[A-Z][a-z]+:|$)", clean, re.DOTALL)

        result = {
            "day": day.strip(),
            "winds": winds_match.group(1).replace("\n", " ").strip() if winds_match else None,
            "seas": seas_match.group(1).replace("\n", " ").strip() if seas_match else None,
            "weather": weather_match.group(1).replace("\n", " ").strip() if weather_match else None,
        }

        results.append(result)

    return results


def get_last_n_days_forecast(text: str, n: int = 3) -> List[Dict[str, str]]:
    sections = parse_forecast_sections(text)
    return sections[-n:]


def save_forecast_as_json(forecasts: List[Dict[str, str]], output_file: str):
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(forecasts, f, ensure_ascii=False, indent=2)
