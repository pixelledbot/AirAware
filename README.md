# AirAware

AirAware is a real-time gas monitoring project built around an MQ2-style sensor workflow.  
It includes:

- **Data simulation + ingestion** with automatic CSV logging
- **Cloud upload to ThingSpeak** for live remote monitoring
- **Threshold-based email alerts** when gas values are high
- **Data cleaning and smoothing** for better analysis
- **Interactive web dashboard** for visualization and status tracking

## Project Files

- `import_data.py`  
  Simulates gas sensor readings, stores timestamped values in `gas_sensor_data.csv`, sends data to ThingSpeak, and triggers email alerts when readings cross the threshold.

- `data_clean.py`  
  Cleans raw readings by removing invalid/outlier values and applies moving-average smoothing, then writes output to `gas_sensor_cleaned.csv`.

- `dashboard.html`  
  Frontend dashboard using Chart.js to fetch ThingSpeak data and display current value, min/max/avg stats, alert state, and historical trends.

## Workflow

1. Run `import_data.py` to generate/read sensor values and upload them to ThingSpeak.
2. Open `dashboard.html` in a browser to monitor live gas data.
3. Run `data_clean.py` when you want a cleaned dataset for analysis.

## Notes

- The current scripts include generic placeholder API/email credentials.  
  Replace them with your own values, and use environment variables for production.
- CSV files expected/generated:
  - `gas_sensor_data.csv`
  - `gas_sensor_cleaned.csv`
