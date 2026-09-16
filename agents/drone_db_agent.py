import sqlite3
import os


DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "drone_data.db"
)


def get_drones():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT drone_id, model, status, battery, temperature, location
        FROM drones
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows


def get_low_battery_drones():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT drone_id, battery, status
        FROM drones
        WHERE battery < 30
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows


def get_high_temperature_drones():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT drone_id, temperature, status
        FROM drones
        WHERE temperature > 55
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows


def get_failed_missions():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT mission_id, drone_id, mission_type, status
        FROM missions
        WHERE status = 'Failed'
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows


def get_high_alerts():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT drone_id, alert_type, severity, message
        FROM alerts
        WHERE severity = 'HIGH'
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows


def get_missions():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT mission_id, drone_id, mission_type, status, duration
        FROM missions
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows


def get_telemetry():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT drone_id, altitude, speed, battery, temperature, signal_strength
        FROM telemetry
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows


if __name__ == "__main__":

    print("\nALL DRONES:")
    for drone in get_drones():
        print(drone)

    print("\nLOW BATTERY DRONES:")
    for drone in get_low_battery_drones():
        print(drone)

    print("\nHIGH TEMPERATURE DRONES:")
    for drone in get_high_temperature_drones():
        print(drone)

    print("\nFAILED MISSIONS:")
    for mission in get_failed_missions():
        print(mission)

    print("\nHIGH SEVERITY ALERTS:")
    for alert in get_high_alerts():
        print(alert)
def get_drone_telemetry(drone_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT battery, temperature, signal_strength
        FROM telemetry
        WHERE drone_id = ?
    """, (drone_id,))

    row = cursor.fetchone()
    conn.close()

    return row        