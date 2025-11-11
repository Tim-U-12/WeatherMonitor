from bom_parser import *

# Load file
with open("data/IDV10460.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()

# Parse last 3 days
forecasts = get_last_n_days_forecast(raw_text, n=3)

# Print structured data
for day in forecasts:
    print(day)

# Save to JSON
save_forecast_as_json(forecasts, "data/structured_last_3_days.json")
print("✅ Saved to data/structured_last_3_days.json")