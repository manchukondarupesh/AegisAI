import sqlite3

DB_NAME = "data/drone_data.db"


def create_database():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # DRONES TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS drones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        drone_id TEXT UNIQUE,
        model TEXT,
        status TEXT,
        battery REAL,
        temperature REAL,
        location TEXT
    )
    """)

    # MISSIONS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS missions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mission_id TEXT UNIQUE,
        drone_id TEXT,
        mission_type TEXT,
        status TEXT,
        duration INTEGER
    )
    """)

    # TELEMETRY TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS telemetry (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        drone_id TEXT,
        altitude REAL,
        speed REAL,
        battery REAL,
        temperature REAL,
        signal_strength REAL
    )
    """)

    # ALERTS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        drone_id TEXT,
        alert_type TEXT,
        severity TEXT,
        message TEXT
    )
    """)

    # SAMPLE DRONES
    drones = [
        ("D-01", "DJI-Matrice", "Active", 82, 42, "Site-A"),
        ("D-02", "DJI-Matrice", "Active", 67, 45, "Site-B"),
        ("D-03", "Autonomous-X1", "Warning", 28, 61, "Site-A"),
        ("D-04", "Autonomous-X2", "Idle", 91, 38, "Site-C"),
        ("D-05", "Autonomous-X3", "Active", 74, 47, "Site-B")
    ]

    cursor.executemany("""
    INSERT OR IGNORE INTO drones
    (drone_id, model, status, battery, temperature, location)
    VALUES (?, ?, ?, ?, ?, ?)
    """, drones)

    # SAMPLE MISSIONS
    missions = [
        ("M-001", "D-01", "Inspection", "Completed", 32),
        ("M-002", "D-02", "Surveillance", "Completed", 45),
        ("M-003", "D-03", "Inspection", "Failed", 18),
        ("M-004", "D-04", "Mapping", "Completed", 52),
        ("M-005", "D-05", "Surveillance", "In Progress", 27)
    ]

    cursor.executemany("""
    INSERT OR IGNORE INTO missions
    (mission_id, drone_id, mission_type, status, duration)
    VALUES (?, ?, ?, ?, ?)
    """, missions)

    # SAMPLE TELEMETRY
    telemetry = [
        ("D-01", 120, 18, 82, 42, 96),
        ("D-02", 150, 22, 67, 45, 91),
        ("D-03", 90, 15, 28, 61, 72),
        ("D-04", 100, 20, 91, 38, 98),
        ("D-05", 135, 24, 74, 47, 88)
    ]

    cursor.executemany("""
    INSERT INTO telemetry
    (drone_id, altitude, speed, battery, temperature, signal_strength)
    VALUES (?, ?, ?, ?, ?, ?)
    """, telemetry)

    # SAMPLE ALERTS
    alerts = [
        (
            "D-03",
            "Low Battery",
            "HIGH",
            "Battery level below safe operating threshold"
        ),
        (
            "D-03",
            "High Temperature",
            "HIGH",
            "Drone temperature is above normal range"
        ),
        (
            "D-05",
            "Weak Signal",
            "MEDIUM",
            "Signal strength is decreasing"
        )
    ]

    cursor.executemany("""
    INSERT INTO alerts
    (drone_id, alert_type, severity, message)
    VALUES (?, ?, ?, ?)
    """, alerts)

    conn.commit()
    conn.close()

    print("Drone database created successfully.")
    print("Sample drone data inserted successfully.")


if __name__ == "__main__":
    create_database()