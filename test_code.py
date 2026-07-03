def fetch_sensor_data():
    """Simulates reading data from an external sensor."""
    return [10, 20, 30]

def normalize_metrics():
    """Processes and cleans the raw data."""
    raw_data = fetch_sensor_data()
    return [x / 100.0 for x in raw_data]

def trigger_alert_system():
    """Triggers external systems based on normalized data."""
    clean_data = normalize_metrics()
    if max(clean_data) > 0.8:
        print("Alert triggered!")

def main_execution_loop():
    """The main orchestration loop."""
    trigger_alert_system()