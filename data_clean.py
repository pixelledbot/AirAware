import csv

# ---------------- Parameters ----------------
INPUT_FILE = 'gas_sensor_data.csv'
OUTPUT_FILE = 'gas_sensor_cleaned.csv'
MOVING_AVG_N = 5       # Number of points for moving average
MAX_CHANGE = 200       # Maximum allowed change between readings
MIN_VALUE = 0          # Minimum valid gas value
MAX_VALUE = 4095       # Maximum valid gas value (12-bit ADC)

# ---------------- Read original data ----------------
timestamps = []
gas_vals = []

with open(INPUT_FILE, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            gas = float(row['Gas'])
            # Ignore invalid values
            if gas < MIN_VALUE or gas > MAX_VALUE:
                continue
            # Spike filtering
            if gas_vals and abs(gas - gas_vals[-1]) > MAX_CHANGE:
                continue
            timestamps.append(row['Timestamp'])
            gas_vals.append(gas)
        except:
            continue

# ---------------- Apply moving average smoothing ----------------
smooth_vals = []
for i in range(len(gas_vals)):
    if i + 1 >= MOVING_AVG_N:
        smooth = sum(gas_vals[i - MOVING_AVG_N + 1:i + 1]) / MOVING_AVG_N
    else:
        smooth = gas_vals[i]
    smooth_vals.append(smooth)

# ---------------- Write cleaned data ----------------
with open(OUTPUT_FILE, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Timestamp', 'Gas', 'SmoothedGas'])
    for t, g, s in zip(timestamps, gas_vals, smooth_vals):
        writer.writerow([t, g, s])

print(f"Cleaned data saved to {OUTPUT_FILE}")
