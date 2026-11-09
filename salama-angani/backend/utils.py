import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def generate_pdf_ticket(booking, flight):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Header
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, 750, "Salama Angani E-Ticket")
    
    # Passenger & Booking Details
    c.setFont("Helvetica", 14)
    c.drawString(50, 700, f"Passenger Name: {booking.passenger_name}")
    c.drawString(50, 675, f"Booking Reference (PNR): {booking.booking_reference}")
    
    # Flight Details
    c.drawString(50, 625, f"Flight Number: {flight.flight_number}")
    c.drawString(50, 600, f"Route: {flight.origin} to {flight.destination}")
    c.drawString(50, 575, f"Price Paid: ${flight.base_price:.2f}")
    
    # Footer
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, 500, "Thank you for flying with Salama Angani. Have a safe flight!")
    
    c.save()
    buffer.seek(0)
    return buffer