import sqlite3
from werkzeug.security import generate_password_hash

DATABASE_NAME = 'flight_ticketing.db'

def init_db():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Table 1: Flights
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flights (
            flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
            flight_number TEXT UNIQUE NOT NULL,
            airline_name TEXT NOT NULL,
            departure_city TEXT NOT NULL,
            destination_city TEXT NOT NULL,
            departure_date DATE NOT NULL,
            departure_time TIME NOT NULL,
            arrival_time TIME NOT NULL,
            travel_class TEXT NOT NULL,
            ticket_price REAL NOT NULL,
            total_seats INTEGER NOT NULL,
            available_seats INTEGER NOT NULL
        )
    ''')

    # Table 2: Passengers
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passengers (
            passenger_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            identification_number TEXT NOT NULL
        )
    ''')

    # Table 3: Bookings
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_reference TEXT UNIQUE NOT NULL,
            passenger_id INTEGER NOT NULL,
            flight_id INTEGER NOT NULL,
            number_of_passengers INTEGER NOT NULL,
            travel_class TEXT NOT NULL,
            total_cost REAL NOT NULL,
            booking_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            booking_status TEXT NOT NULL CHECK(booking_status IN ('Pending', 'Confirmed', 'Cancelled')),
            FOREIGN KEY (passenger_id) REFERENCES passengers (passenger_id),
            FOREIGN KEY (flight_id) REFERENCES flights (flight_id)
        )
    ''')

    # Table 4: Administrators
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS administrators (
            admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')

    # Table 5: Contact Messages
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contact_messages (
            message_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            submission_date DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print("Database tables initialized successfully.")

def seed_data():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Check if admin exists; if not, create one securely
    cursor.execute("SELECT * FROM administrators WHERE username = 'admin'")
    if not cursor.fetchone():
        hashed_pw = generate_password_hash('admin123')
        cursor.execute("INSERT INTO administrators (username, password_hash) VALUES (?, ?)", ('admin', hashed_pw))
        print("Default admin account created (username: admin, password: admin123).")

    # Insert sample flights if the flights table is empty
    cursor.execute("SELECT COUNT(*) FROM flights")
    if cursor.fetchone()[0] == 0:
        sample_flights = [
            ('SL101', 'SkyLink Airlines', 'Nairobi (NBO)', 'Mombasa (MBA)', '2026-11-12', '08:00 AM', '09:15 AM', 'Economy', 8500.00, 100, 100),
            ('SL205', 'SkyLink Airlines', 'Nairobi (NBO)', 'Kisumu (KIS)', '2026-11-12', '10:30 AM', '11:25 AM', 'Economy', 6500.00, 80, 80),
            ('SL310', 'SkyLink Airlines', 'Mombasa (MBA)', 'Nairobi (NBO)', '2026-11-13', '02:00 PM', '03:15 PM', 'Economy', 9000.00, 100, 100)
        ]
        cursor.executemany('''
            INSERT INTO flights (
                flight_number, airline_name, departure_city, destination_city, 
                departure_date, departure_time, arrival_time, travel_class, 
                ticket_price, total_seats, available_seats
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_flights)
        print("Sample flights inserted.")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    seed_data()