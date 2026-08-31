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
    """Seed initial sample railway data."""
    passengers = [
        ("Sui Shinano", "09171234567", "Student"),
        ("Ana Cruz", "09187654321", "Regular"),
        ("Carlos Tan", "09221113334", "Senior"),
        ("Elena Gomez", "09334445556", "Regular"),
        ("Mateo Garcia", "09191112233", "Regular"),
        ("Beatrice Ramos", "09202223344", "Student"),
        ("Fernando Reyes", "09173334455", "Senior"),
        ("Jasmine Lim", "09284445566", "Student"),
        ("Rafael Santos", "09185556677", "Regular"),
        ("Lourdes Mendoza", "09226667788", "Senior"),
        ("Gabriel Navarro", "09177778899", "Regular"),
        ("Samantha Perez", "09298889900", "Student"),
        ("Antonio Dizon", "09189990011", "Senior"),
        ("Katrina Villanueva", "09210001122", "Regular"),
        ("Dominic Alcantara", "09172228833", "Regular"),
        ("Patricia Sy", "09273339944", "Student")
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

def view_trains(cursor):
    print("\n" + "=" * 65)
    print("AVAILABLE TRAIN ROUTES")
    print("=" * 65)
    cursor.execute("SELECT train_id, train_code, origin, destination, capacity, fare FROM trains;")
    rows = cursor.fetchall()
    for row in rows:
        print(f"[{row[0]}] {row[1]:<8} | {row[2]} -> {row[3]:<10} | Cap: {row[4]:<4} | Fare: PHP {row[5]:.2f}")

def view_bookings(cursor):
    print("\n" + "=" * 70)
    print("CURRENT PASSENGER BOOKING MANIFEST")
    print("=" * 70)
    cursor.execute("""
        SELECT b.booking_id, p.name, p.passenger_type, t.train_code, t.origin || ' -> ' || t.destination, b.seat_number, t.fare
        FROM bookings b
        JOIN passengers p ON b.passenger_id = p.passenger_id
        JOIN trains t ON b.train_id = t.train_id
        ORDER BY b.booking_id;
    """)
    rows = cursor.fetchall()
    for row in rows:
        print(f"Booking #{row[0]:<2} | {row[1]:<15} ({row[2]:<7}) | {row[3]} ({row[4]}) | Seat {row[5]} | PHP {row[6]:.2f}")

def book_ticket(cursor, conn):
    print("\n--- BOOK A NEW TICKET ---")
    name = input("Enter Passenger Name: ").strip()
    contact = input("Enter Contact Number: ").strip()
    
    print("Types: 1. Regular | 2. Student | 3. Senior")
    type_choice = input("Select Type (1-3): ").strip()
    type_map = {"1": "Regular", "2": "Student", "3": "Senior"}
    p_type = type_map.get(type_choice, "Regular")

    cursor.execute("INSERT OR IGNORE INTO passengers (name, contact_number, passenger_type) VALUES (?, ?, ?);", 
                   (name, contact, p_type))
    cursor.execute("SELECT passenger_id FROM passengers WHERE contact_number = ?;", (contact,))
    passenger_id = cursor.fetchone()[0]

    view_trains(cursor)
    train_id = input("\nEnter Train ID to Book: ").strip()
    seat_num = input("Enter Seat Number: ").strip()

    try:
        cursor.execute("INSERT INTO bookings (passenger_id, train_id, seat_number) VALUES (?, ?, ?);",
                       (passenger_id, int(train_id), int(seat_num)))
        conn.commit()
        print("\n Ticket successfully booked!")
    except Exception as e:
        print(f"\n Error booking ticket: {e}")

def view_analytics(cursor):
    print("\n" + "=" * 65)
    print("ROUTE REVENUE & OCCUPANCY SUMMARY")
    print("=" * 65)
    cursor.execute("""
        SELECT t.train_code, t.origin, t.destination, COUNT(b.booking_id) AS total_passengers, COALESCE(SUM(t.fare), 0) AS total_revenue
        FROM trains t
        LEFT JOIN bookings b ON t.train_id = b.train_id
        GROUP BY t.train_id;
    """)
    for row in cursor.fetchall():
        print(f"Train: {row[0]} ({row[1]} to {row[2]}) | Booked: {row[3]} | Revenue: PHP {row[4]:.2f}")

def ask_return_to_menu():
    """Prompt the user whether to return to the menu or exit."""
    while True:
        choice = input("\nDo you want to go back to the menu? (y/n): ").strip().lower()
        if choice in ('y', 'yes'):
            return True
        elif choice in ('n', 'no'):
            return False
        else:
            print("Please enter 'y' for yes or 'n' for no.")

def main():
    conn = sqlite3.connect("train_system.db")
    cursor = conn.cursor()

    init_db(cursor)
    seed_data(cursor)
    conn.commit()

    while True:
        print("\n" + "=" * 35)
        print("  TRAIN TICKETING SYSTEM MENU")
        print("=" * 35)
        print("1. View Available Train Routes")
        print("2. View All Bookings (Manifest)")
        print("3. Book a Ticket")
        print("4. View Revenue & Occupancy Report")
        print("5. Exit")
        
        choice = input("Enter choice (1-5): ").strip()

        if choice == "1":
            view_trains(cursor)
        elif choice == "2":
            view_bookings(cursor)
        elif choice == "3":
            book_ticket(cursor, conn)
        elif choice == "4":
            view_analytics(cursor)
        elif choice == "5":
            print("\nExiting system. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please select 1-5.")

        if not ask_return_to_menu():
            print("\nExiting system. Goodbye!")
            break

    conn.close()

if __name__ == "__main__":
    main()