from bom_fetcher import download_bom_forecast
from bom_parser import get_last_n_days_forecast, save_forecast_as_json 

def core():
  # download_bom_forecast()

  # Load file
  with open("data/IDV10460.txt", "r", encoding="utf-8") as f:
      raw_text = f.read()

  # Parse last 3 days
  forecasts = get_last_n_days_forecast(raw_text, n=3)

  # Save to JSON
  save_forecast_as_json(forecasts,"data/forecast.json")
  print("✅ Saved to data/forecast.json")