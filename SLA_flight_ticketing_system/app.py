from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from flask_socketio import SocketIO, emit
import sqlite3
from werkzeug.security import check_password_hash
import uuid
import datetime
import re

app = Flask(__name__)
# Secret key is required for session management and flash messages
app.config['SECRET_KEY'] = 'skylink_super_secret_key_change_in_production'
socketio = SocketIO(app, cors_allowed_origins="*")
# Note: Remove your old app.secret_key assignment if you use app.config

DATABASE = 'flight_ticketing.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # Allows dictionary-like access to rows
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# --- PUBLIC ROUTES ---

@app.route('/')
def index():
    db = get_db()
    # Fetch up to 6 upcoming flights that have available seats
    cur = db.execute('''
        SELECT * FROM flights 
        WHERE available_seats > 0 
        ORDER BY departure_date ASC, departure_time ASC 
        LIMIT 6
    ''')
    upcoming_flights = cur.fetchall()
    return render_template('index.html', upcoming_flights=upcoming_flights)

@app.route('/search', methods=['GET', 'POST'])
def search_flights():
    db = get_db()
    flights = []
    
    if request.method == 'POST':
        departure = request.form.get('departure_city')
        destination = request.form.get('destination_city')
        date = request.form.get('departure_date')
        
        # Prevent identical origin and destination
        if departure == destination:
            flash("Departure and destination cannot be the same.", "error")
        else:
            cur = db.execute('''
                SELECT * FROM flights 
                WHERE departure_city LIKE ? AND destination_city LIKE ? AND departure_date = ? AND available_seats > 0
                ORDER BY departure_date ASC, departure_time ASC
            ''', ('%'+departure+'%', '%'+destination+'%', date))
            flights = cur.fetchall()
            if not flights:
                flash("No flights found matching your criteria.", "info")
    else:
        # GET request: By default, display the complete schedule of available flights
        cur = db.execute('''
            SELECT * FROM flights 
            WHERE available_seats > 0 
            ORDER BY departure_date ASC, departure_time ASC
        ''')
        flights = cur.fetchall()
                
    return render_template('search_flights.html', flights=flights)

@app.route('/book/<int:flight_id>', methods=['GET', 'POST'])
def book_flight(flight_id):
    db = get_db()
    flight = db.execute('SELECT * FROM flights WHERE flight_id = ?', (flight_id,)).fetchone()
    
    if not flight:
        flash("Flight not found.", "error")
        return redirect(url_for('search_flights'))
        
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        id_number = request.form.get('id_number')
        num_passengers = int(request.form.get('num_passengers', 1))
        
        # Server-side validation
        if num_passengers <= 0 or num_passengers > flight['available_seats']:
            flash("Invalid number of passengers or insufficient seats available.", "error")
            return render_template('booking.html', flight=flight)
            
        total_cost = num_passengers * flight['ticket_price']
        booking_ref = f"SLK-{str(uuid.uuid4())[:6].upper()}"
        
        try:
            # Transaction to ensure data integrity
            db.execute('BEGIN TRANSACTION')
            
            # 1. Insert Passenger
            cur = db.execute('''
                INSERT INTO passengers (full_name, email, phone, identification_number) 
                VALUES (?, ?, ?, ?)
            ''', (full_name, email, phone, id_number))
            passenger_id = cur.lastrowid
            
            # 2. Insert Booking
            db.execute('''
                INSERT INTO bookings (booking_reference, passenger_id, flight_id, number_of_passengers, travel_class, total_cost, booking_status)
                VALUES (?, ?, ?, ?, ?, ?, 'Confirmed')
            ''', (booking_ref, passenger_id, flight_id, num_passengers, flight['travel_class'], total_cost))
            
            # 3. Update Seat Availability
            db.execute('''
                UPDATE flights SET available_seats = available_seats - ? WHERE flight_id = ?
            ''', (num_passengers, flight_id))
            
            db.execute('COMMIT')
            return redirect(url_for('booking_confirmation', ref=booking_ref))
            
        except sqlite3.Error as e:
            db.execute('ROLLBACK')
            flash("An error occurred during booking. Please try again.", "error")
            
    return render_template('booking.html', flight=flight)

@app.route('/confirmation/<ref>')
def booking_confirmation(ref):
    db = get_db()
    booking = db.execute('''
        SELECT b.*, p.full_name, p.email, f.flight_number, f.departure_city, f.destination_city, f.departure_date, f.departure_time
        FROM bookings b
        JOIN passengers p ON b.passenger_id = p.passenger_id
        JOIN flights f ON b.flight_id = f.flight_id
        WHERE b.booking_reference = ?
    ''', (ref,)).fetchone()
    
    if not booking:
        flash("Booking not found.", "error")
        return redirect(url_for('index'))
        
    return render_template('booking_confirmation.html', booking=booking)

@app.route('/my_bookings', methods=['GET', 'POST'])
def my_bookings():
    db = get_db()
    booking = None
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'search':
            ref = request.form.get('booking_reference')
            email = request.form.get('email')
            booking = db.execute('''
                SELECT b.*, p.email, f.departure_city, f.destination_city, f.departure_date 
                FROM bookings b
                JOIN passengers p ON b.passenger_id = p.passenger_id
                JOIN flights f ON b.flight_id = f.flight_id
                WHERE b.booking_reference = ? AND p.email = ?
            ''', (ref, email)).fetchone()
            
            if not booking:
                flash("No booking found with those details.", "error")
                
        elif action == 'cancel':
            booking_id = request.form.get('booking_id')
            flight_id = request.form.get('flight_id')
            num_passengers = int(request.form.get('num_passengers'))
            
            try:
                db.execute('BEGIN TRANSACTION')
                db.execute("UPDATE bookings SET booking_status = 'Cancelled' WHERE booking_id = ?", (booking_id,))
                db.execute("UPDATE flights SET available_seats = available_seats + ? WHERE flight_id = ?", (num_passengers, flight_id))
                db.execute('COMMIT')
                flash("Booking successfully cancelled. Seats have been released.", "success")
            except sqlite3.Error:
                db.execute('ROLLBACK')
                flash("Failed to cancel booking.", "error")
            return redirect(url_for('index'))
            
    return render_template('my_bookings.html', booking=booking)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        db = get_db()
        name = request.form.get('customer_name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        db.execute('''
            INSERT INTO contact_messages (customer_name, email, subject, message)
            VALUES (?, ?, ?, ?)
        ''', (name, email, subject, message))
        db.commit()
        flash("Message sent successfully!", "success")
        return redirect(url_for('contact'))
    return render_template('contact.html')

# --- ADMIN ROUTES ---

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        db = get_db()
        
        admin = db.execute('SELECT * FROM administrators WHERE username = ?', (username,)).fetchone()
        
        if admin and check_password_hash(admin['password_hash'], password):
            session['admin_id'] = admin['admin_id']
            session['username'] = admin['username']
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid credentials.", "error")
            
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))
        
    db = get_db()
    flights = db.execute('SELECT * FROM flights').fetchall()
    bookings_count = db.execute('SELECT COUNT(*) FROM bookings').fetchone()[0]
    
    return render_template('admin/dashboard.html', flights=flights, total_bookings=bookings_count)

# --- MISSING ADMIN FLIGHT CRUD ROUTES ---

@app.route('/admin/flight/add', methods=['GET', 'POST'])
def add_flight():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))
        
    if request.method == 'POST':
        db = get_db()
        flight_number = request.form.get('flight_number')
        airline_name = request.form.get('airline_name')
        departure_city = request.form.get('departure_city')
        destination_city = request.form.get('destination_city')
        departure_date = request.form.get('departure_date')
        departure_time = request.form.get('departure_time')
        arrival_time = request.form.get('arrival_time')
        travel_class = request.form.get('travel_class')
        ticket_price = float(request.form.get('ticket_price'))
        total_seats = int(request.form.get('total_seats'))
        
        try:
            db.execute('''
                INSERT INTO flights (flight_number, airline_name, departure_city, destination_city, departure_date, departure_time, arrival_time, travel_class, ticket_price, total_seats, available_seats)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (flight_number, airline_name, departure_city, destination_city, departure_date, departure_time, arrival_time, travel_class, ticket_price, total_seats, total_seats))
            db.commit()
            flash("Flight added successfully.", "success")
            return redirect(url_for('admin_dashboard'))
        except sqlite3.IntegrityError:
            flash("Flight number already exists.", "error")
            
    return render_template('admin/add_flight.html')

@app.route('/admin/flight/edit/<int:flight_id>', methods=['GET', 'POST'])
def edit_flight(flight_id):
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))
        
    db = get_db()
    flight = db.execute('SELECT * FROM flights WHERE flight_id = ?', (flight_id,)).fetchone()
    
    if request.method == 'POST':
        departure_date = request.form.get('departure_date')
        departure_time = request.form.get('departure_time')
        arrival_time = request.form.get('arrival_time')
        ticket_price = float(request.form.get('ticket_price'))
        
        db.execute('''
            UPDATE flights 
            SET departure_date = ?, departure_time = ?, arrival_time = ?, ticket_price = ?
            WHERE flight_id = ?
        ''', (departure_date, departure_time, arrival_time, ticket_price, flight_id))
        db.commit()
        flash("Flight updated successfully.", "success")
        return redirect(url_for('admin_dashboard'))
        
    return render_template('admin/edit_flight.html', flight=flight)

@app.route('/admin/flight/delete/<int:flight_id>', methods=['POST'])
def delete_flight(flight_id):
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))
        
    db = get_db()
    # Check if bookings exist for this flight to prevent orphaned data
    bookings = db.execute('SELECT COUNT(*) FROM bookings WHERE flight_id = ?', (flight_id,)).fetchone()[0]
    
    if bookings > 0:
        flash("Cannot delete flight. Existing bookings depend on this record.", "error")
    else:
        db.execute('DELETE FROM flights WHERE flight_id = ?', (flight_id,))
        db.commit()
        flash("Flight deleted successfully.", "success")
        
    return redirect(url_for('admin_dashboard'))

# --- MISSING ADMIN BOOKING MANAGEMENT ROUTE ---

@app.route('/admin/bookings', methods=['GET'])
def admin_bookings():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))
        
    db = get_db()
    search_query = request.args.get('search', '')
    
    if search_query:
        bookings = db.execute('''
            SELECT b.*, p.full_name, p.email, f.flight_number, f.departure_date
            FROM bookings b
            JOIN passengers p ON b.passenger_id = p.passenger_id
            JOIN flights f ON b.flight_id = f.flight_id
            WHERE b.booking_reference LIKE ? OR f.flight_number LIKE ?
            ORDER BY b.booking_date DESC
        ''', ('%'+search_query+'%', '%'+search_query+'%')).fetchall()
    else:
        bookings = db.execute('''
            SELECT b.*, p.full_name, p.email, f.flight_number, f.departure_date
            FROM bookings b
            JOIN passengers p ON b.passenger_id = p.passenger_id
            JOIN flights f ON b.flight_id = f.flight_id
            ORDER BY b.booking_date DESC
        ''').fetchall()
        
    return render_template('admin/bookings.html', bookings=bookings, search_query=search_query)

# --- CHATBOT SOCKETIO LOGIC ---
# --- CHATBOT SOCKETIO LOGIC ---
@socketio.on('user_message')
def handle_user_message(data):
    user_text = data.get('message', '').lower()
    bot_response = "I'm sorry, I didn't understand that. You can ask me about our destinations, baggage policy, or how to book a flight."

    # 1. Static Rules
    if 'hello' in user_text or 'hi' in user_text:
        bot_response = "Hello! Welcome to SkyLink Airlines. How can I assist you with your travel plans today?"
    elif 'destination' in user_text or 'where do you fly' in user_text:
        bot_response = "SkyLink currently serves major regional hubs including Nairobi (NBO), Mombasa (MBA), and Kisumu (KIS)."
    elif 'baggage' in user_text or 'luggage' in user_text:
        bot_response = "Economy class includes 1 checked bag (23kg) and 1 carry-on. Business class includes 2 checked bags (32kg each)."
    
    # 2. Dynamic Database Queries (Flight Availability)
    elif 'flight' in user_text or 'available' in user_text:
        db = get_db()
        
        # Map month names to SQLite date format numbers
        months = {
            'january': '01', 'february': '02', 'march': '03', 'april': '04', 
            'may': '05', 'june': '06', 'july': '07', 'august': '08', 
            'september': '09', 'october': '10', 'november': '11', 'december': '12'
        }
        
        found_month = next((num for name, num in months.items() if name in user_text), None)
        date_match = re.search(r'\d{4}-\d{2}-\d{2}', user_text)

        # Scenario A: User asks for a specific date (e.g., "flights on 2026-11-15")
        if date_match:
            search_date = date_match.group(0)
            cur = db.execute("SELECT * FROM flights WHERE departure_date = ? AND available_seats > 0 LIMIT 5", (search_date,))
            flights = cur.fetchall()
            if flights:
                bot_response = f"<strong>Flights on {search_date}:</strong><br>"
                for f in flights:
                    bot_response += f"&bull; {f['airline_name']} {f['flight_number']} ({f['departure_city']} to {f['destination_city']}) at {f['departure_time']}<br>"
            else:
                bot_response = f"I couldn't find any flights on {search_date}."
                
        # Scenario B: User asks for a specific month (e.g., "flights in november")
        elif found_month:
            cur = db.execute(f"SELECT * FROM flights WHERE departure_date LIKE '%-{found_month}-%' AND available_seats > 0 ORDER BY departure_date ASC LIMIT 5")
            flights = cur.fetchall()
            if flights:
                month_name = [name.capitalize() for name, num in months.items() if num == found_month][0]
                bot_response = f"<strong>Flights in {month_name}:</strong><br>"
                for f in flights:
                    bot_response += f"&bull; {f['flight_number']} ({f['departure_city']} to {f['destination_city']}) on {f['departure_date']}<br>"
            else:
                bot_response = f"I couldn't find any flights scheduled for that month."
                
        # Scenario C: General availability ("What flights are available?")
        else:
            cur = db.execute("SELECT * FROM flights WHERE available_seats > 0 ORDER BY departure_date ASC LIMIT 5")
            flights = cur.fetchall()
            if flights:
                bot_response = "<strong>Here are our next available flights:</strong><br>"
                for f in flights:
                    bot_response += f"&bull; {f['flight_number']} ({f['departure_city']} to {f['destination_city']}) on {f['departure_date']}<br>"
                bot_response += "<em>Visit the Search page to see our full catalog!</em>"
            else:
                bot_response = "We currently have no available flights."

    elif 'book' in user_text or 'reservation' in user_text:
        bot_response = "You can book a flight directly from our Home page. Just enter your origin, destination, and travel dates!"
    elif 'contact' in user_text or 'help' in user_text:
        bot_response = "You can reach our support team at support@skylinkairlines.com or call +254 700 000 000."

    # Send the response back to the specific client
    emit('bot_response', {'message': bot_response})

if __name__ == '__main__':
    socketio.run(app, debug=True)