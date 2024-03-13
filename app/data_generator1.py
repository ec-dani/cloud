import time
import random
import requests
from datetime import datetime, timezone, timedelta

analysis_ip= 'http://172.19.0.3:5000'

def generate_data():
    current_time = datetime.now(timezone.utc)
    new_time = current_time + timedelta(hours=3)
    timestamp = new_time.isoformat()
    sensor_id = "SENSOR_1.1" 
    humans_detected = random.randint(0, 20)
    unknown_detected = random.randint(0, humans_detected)
    data = {
        "timestamp": timestamp,
        "sensor_id": sensor_id,
        "humans_detected": humans_detected,
        "unknown_detected": unknown_detected
    }
    return data

def main():
    while True:
        data = generate_data()
        try:
            print('HOoola')
            response = requests.post(f"{analysis_ip}/api/store_data", json=data)
            print("Data sent successfully:", data)
        except Exception as e:

            print("Error sending data:", e)
        time.sleep(5)

if __name__ == "__main__":
    main()
