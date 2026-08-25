import sqlite3

def init_db(cursor):
    """Create relational tables for the train ticketing system."""
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS passengers (
        passenger_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        contact_number TEXT UNIQUE NOT NULL,
        passenger_type TEXT NOT NULL CHECK(passenger_type IN ('Regular', 'Student', 'Senior'))
    );

    CREATE TABLE IF NOT EXISTS trains (
        train_id INTEGER PRIMARY KEY AUTOINCREMENT,
        train_code TEXT UNIQUE NOT NULL,
        origin TEXT NOT NULL,
        destination TEXT NOT NULL,
        capacity INTEGER NOT NULL,
        fare REAL NOT NULL
    );

    CREATE TABLE IF NOT EXISTS bookings (
        booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
        passenger_id INTEGER NOT NULL,
        train_id INTEGER NOT NULL,
        seat_number INTEGER NOT NULL,
        booking_status TEXT NOT NULL DEFAULT 'Confirmed',
        FOREIGN KEY (passenger_id) REFERENCES passengers(passenger_id) ON DELETE CASCADE,
        FOREIGN KEY (train_id) REFERENCES trains(train_id) ON DELETE CASCADE
    );
    """)

def seed_data(cursor):
    """Seed sample railway data."""
    passengers = [
        ("Daniel Velasco", "09171234567", "Student"),
        ("Ana Cruz", "09187654321", "Regular"),
        ("Carlos Tan", "09221113334", "Senior"),
        ("Elena Gomez", "09334445556", "Regular")
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO passengers (name, contact_number, passenger_type) VALUES (?, ?, ?);",
        passengers
    )

    trains = [
        ("EXP-101", "Tutuban", "Calamba", 120, 150.00),
        ("COMM-202", "North Ave", "Taft", 300, 30.00),
        ("LTD-303", "Bicutan", "Alabang", 80, 50.00)
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO trains (train_code, origin, destination, capacity, fare) VALUES (?, ?, ?, ?, ?);",
        trains
    )

    # (passenger_id, train_id, seat_number, booking_status)
    bookings = [
        (1, 1, 12, "Confirmed"),
        (2, 1, 14, "Confirmed"),
        (3, 2, 45, "Confirmed"),
        (4, 2, 46, "Confirmed"),
        (1, 3, 5, "Confirmed")
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO bookings (passenger_id, train_id, seat_number, booking_status) VALUES (?, ?, ?, ?);",
        bookings
    )

def run_test_queries(cursor):
    print("=" * 65)
    print("TEST CASE 1: Passenger Ticket Manifest (INNER JOIN)")
    print("=" * 65)
    cursor.execute("""
        SELECT p.name, p.passenger_type, t.train_code, t.origin || ' -> ' || t.destination, b.seat_number, t.fare
        FROM bookings b
        JOIN passengers p ON b.passenger_id = p.passenger_id
        JOIN trains t ON b.train_id = t.train_id
        ORDER BY t.train_code;
    """)
    for row in cursor.fetchall():
        print(f"Passenger: {row[0]:<15} | Type: {row[1]:<7} | Train: {row[2]} ({row[3]}) | Seat: {row[4]} | Fare: PHP {row[5]:.2f}")

    print("\n" + "=" * 65)
    print("TEST CASE 2: Passenger Filtering by Fare and Type (WHERE & FILTER)")
    print("=" * 65)
    cursor.execute("""
        SELECT p.name, p.passenger_type, t.train_code, t.fare
        FROM bookings b
        JOIN passengers p ON b.passenger_id = p.passenger_id
        JOIN trains t ON b.train_id = t.train_id
        WHERE p.passenger_type = 'Student' OR t.fare >= 100.00;
    """)
    for row in cursor.fetchall():
        print(f"Name: {row[0]:<15} | Type: {row[1]:<8} | Train: {row[2]} | Fare: PHP {row[3]:.2f}")

    print("\n" + "=" * 65)
    print("TEST CASE 3: Train Revenue & Occupancy (GROUP BY & AGGREGATION)")
    print("=" * 65)
    cursor.execute("""
        SELECT t.train_code, t.origin, t.destination, COUNT(b.booking_id) AS total_passengers, SUM(t.fare) AS total_revenue
        FROM trains t
        LEFT JOIN bookings b ON t.train_id = b.train_id
        GROUP BY t.train_id;
    """)
    for row in cursor.fetchall():
        print(f"Train: {row[0]} ({row[1]} to {row[2]}) | Booked Seats: {row[3]} | Total Revenue: PHP {row[4]:.2f}")

def main():
    conn = sqlite3.connect("train_system.db")
    cursor = conn.cursor()

    init_db(cursor)
    seed_data(cursor)
    conn.commit()

    run_test_queries(cursor)

    conn.close()

if __name__ == "__main__":
    main()