# 🌤️ WeatherMonitor

**WeatherMonitor** determines whether the upcoming **Saturday** and **Sunday** are good days to go **snorkelling or diving**.  

It checks the **Bureau of Meteorology (BOM)** site midweek (on **Wednesdays** and **Thursdays**) and analyzes the forecast data to generate a **snorkelling suitability score** between **0 and 100**.  
The app also sends an **email summary** with the results.

---

## 🧭 Features

- 🌊 Fetches weather forecasts from the BOM website  
- 📅 Evaluates upcoming weekend conditions  
- 📈 Generates a **snorkelling score (0–100)** based on forecast data  
- ✉️ Sends an email summary of the results  
- 🕒 Designed to run automatically on Wednesdays and Thursdays

---

## ⚙️ How It Works

1. **Data Fetching** – Retrieves forecast data from the BOM.  
2. **Analysis** – Evaluates relevant metrics such as:
   - Wind speed  
   - Visibility  
   - Wave height  
   - Temperature  
3. **Scoring** – Combines those factors into a snorkelling score between 0 and 100.  
4. **Reporting** – Sends an email report summarizing the weekend’s conditions.

---

## 🧱 Project Structure

weather_monitor/
│
├── src/
│   └── weather_monitor/
│       ├── bom_fetcher.py    # downloads IDV10460.txt
│       ├── bom_parser.py     # parses the text into structured data
│       ├── core.py           # orchestrates: fetch → parse → score → email
│       ├── emailer.py
│       ├── main.py
│       └── utils.py
│
└── data/
│
├── requirements.txt
└── README.md
