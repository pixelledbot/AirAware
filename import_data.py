import sys
import time
import csv
from datetime import datetime
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random

# --------- Disable Matplotlib Window ---------
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# ---------------- CSV Setup ----------------
csv_file = 'gas_sensor_data.csv'
file = open(csv_file, mode='w', newline='')
writer = csv.writer(file)
writer.writerow(['Timestamp', 'Gas'])

# ---------------- Plot Setup (OFFSCREEN) ----------------
fig, ax = plt.subplots()
gas_vals = []
MAX_POINTS = 100
line1, = ax.plot([], [], label='Gas Sensor')
ax.set_xlabel('Samples')
ax.set_ylabel('Gas Value (PPM)')
ax.legend()
ax.grid(True)

# ---------------- ThingSpeak Setup ----------------
THINGSPEAK_API_KEY = 'W3O05QU6TR06OEOA'
THINGSPEAK_URL = 'https://api.thingspeak.com/update'

# ---------------- Email Setup ----------------
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465
EMAIL_USER = 'zoyasubedi04@gmail.com'
EMAIL_APP_PASSWORD = 'kuro alzt eozz ulcy'
EMAIL_RECEIVER = 'simran2315222@gmail.com'

# ---------------- Gas Threshold ----------------
THRESHOLD = 800
UPDATE_INTERVAL = 15

print("Simulation started (no matplotlib window)...\n")

try:
    while True:
        gas = random.randint(300, 1000)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        gas_vals.append(gas)

        writer.writerow([timestamp, gas])
        file.flush()

        print(f"{timestamp} -> Simulated Gas: {gas} ppm")

        # ---- Update plot internally (NOT displayed) ----
        plot_vals = gas_vals[-MAX_POINTS:]
        line1.set_data(range(len(plot_vals)), plot_vals)
        ax.relim()
        ax.autoscale_view()

        # ---- Send to ThingSpeak ----
        try:
            response = requests.get(
                THINGSPEAK_URL,
                params={'api_key': THINGSPEAK_API_KEY, 'field1': gas},
                timeout=5
            )
            print("[OK] Data sent to ThingSpeak successfully.")
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Error sending data to ThingSpeak: {e}")

        # ---- Email Alert ----
        if gas > THRESHOLD:
            try:
                msg = MIMEMultipart()
                msg['From'] = EMAIL_USER
                msg['To'] = EMAIL_RECEIVER
                msg['Subject'] = 'Gas Alert! High Reading Detected'
                msg.attach(MIMEText(
                    f'Gas value = {gas} ppm exceeded threshold {THRESHOLD} ppm at {timestamp}.',
                    'plain'
                ))

                server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
                server.login(EMAIL_USER, EMAIL_APP_PASSWORD)
                server.send_message(msg)
                server.quit()
                print("[EMAIL] Alert email sent!")
            except Exception as e:
                print(f"[ERROR] Error sending email: {e}")

        print("-" * 50)
        time.sleep(UPDATE_INTERVAL)

except KeyboardInterrupt:
    print("\nExiting...")
    file.close()
