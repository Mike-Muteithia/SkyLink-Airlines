Writing

# Salama Angani Ticketing

Salama Angani Ticketing is a full-stack web application for airplane ticket bookings. It features a React frontend and a Python/Flask backend, enabling users to view available flights and book tickets.

## Architecture

- **Frontend:** React (Vite), Axios
- **Backend:** Python, Flask, Flask-SQLAlchemy
- **Database:** SQLite for local development and PostgreSQL for production

## Prerequisites

Ensure the following tools are installed before setting up the application:

- **Node.js:** v18 or later
- **Python:** 3.8 or later
- **WSL 2:** Ubuntu is recommended for local development on Windows.

## Local Setup Instructions

Follow the steps below to set up and run the application locally.

### 1\. Backend Setup

Navigate to the backend directory, create and activate a Python virtual environment, install the dependencies, and start the Flask server.

bash

```
cd backend

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the backend server
python3 app.py
```

The backend API will be available at:

`http://127.0.0.1:5000`

### 2\. Frontend Setup

Open a new terminal, navigate to the frontend directory, install the dependencies, and start the Vite development server.

bash

```
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend application will be available at:

`http://localhost:5173`

## API Documentation

The application exposes the following API endpoints:

| Endpoint | Method | Payload | Description |
| --- | --- | --- | --- |
| `/api/flights` | `GET` | None | Retrieves all available flights and their current seat counts. |
| `/api/bookings` | `POST` | `{"flight_id": 1, "passenger_name": "Mike"}` | Processes a flight booking, decrements the available seat count, and returns a Passenger Name Record (PNR). |

### Example API Requests

#### Retrieve Available Flights

http

```
GET /api/flights
```

Returns the available flights and their current seat counts.

#### Book a Flight

http

```
POST /api/bookings
Content-Type: application/json
```

Request body:

json

```
{
  "flight_id": 1,
  "passenger_name": "Mike"
}
```

This request attempts to book a seat on the specified flight for the passenger. Upon successful booking, the API decrements the available seat count and returns a PNR.

## Development Notes

- Run the backend and frontend in separate terminal sessions.
- Activate the Python virtual environment before running the backend.
- Ensure the backend server is running before making API requests from the frontend.
- Use SQLite for local development and configure PostgreSQL for production deployments.