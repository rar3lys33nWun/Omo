#!/usr/bin/env python3
"""
GlobalWings - Premium Global Flight Booking Platform
Clean native ticket previews + realistic airline-branded PDF tickets

Requirements:
pip install streamlit reportlab

Made with love for you, Troy 💕
"""

import streamlit as st
from datetime import datetime, timedelta
import random
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, black, white
import io

st.set_page_config(
    page_title="GlobalWings • Book Any Airline",
    page_icon="✈️",
    layout="wide"
)

# Header
st.markdown("""
<div style="text-align: center; padding: 8px 0 18px 0;">
    <h1 style="color: #0f172a; font-size: 2.5em; margin:0;">✈️ GlobalWings</h1>
    <p style="color: #475569; margin: 4px 0 0 0;">Fly the World • Book Any Airline Worldwide</p>
</div>
""", unsafe_allow_html=True)

# Airline branding
AIRLINE_STYLES = {
    "Air France": {"primary": "#002157", "tagline": "France is in the Air"},
    "Emirates": {"primary": "#d71a21", "tagline": "Fly Better"},
    "Qatar Airways": {"primary": "#5c0a1e", "tagline": "Going Places Together"},
    "Delta Air Lines": {"primary": "#003366", "tagline": "Keep Climbing"},
    "Lufthansa": {"primary": "#002d5d", "tagline": "Say Yes to the World"},
    "Singapore Airlines": {"primary": "#003366", "tagline": "A Great Way to Fly"},
    "British Airways": {"primary": "#003087", "tagline": "To Fly. To Serve."},
    "Etihad Airways": {"primary": "#003366", "tagline": "The World's Leading Airline"}
}

def get_style(airline):
    return AIRLINE_STYLES.get(airline, {"primary": "#0f172a", "tagline": "Your Journey Begins Here"})

AIRLINES = list(AIRLINE_STYLES.keys())
CITIES = ["Lagos (LOS)", "Dubai (DXB)", "London (LHR)", "New York (JFK)", "Paris (CDG)", 
          "Singapore (SIN)", "Johannesburg (JNB)", "Istanbul (IST)", "Mumbai (BOM)", "Los Angeles (LAX)"]

def generate_flights(origin, destination):
    flights = []
    base = random.randint(520, 1650)
    for _ in range(5):
        airline = random.choice(AIRLINES)
        dep = f"{random.randint(5,23):02d}:{random.randint(0,59):02d}"
        dur = random.randint(5, 14)
        arr_hour = (int(dep[:2]) + dur) % 24
        arr = f"{arr_hour:02d}:{random.randint(0,59):02d}"
        flights.append({
            "id": f"GW{random.randint(10000,99999)}",
            "airline": airline,
            "flight_number": f"{airline[:2].upper()}{random.randint(100,999)}",
            "origin": origin, "destination": destination,
            "departure": dep, "arrival": arr,
            "duration": f"{dur}h {random.randint(10,55)}m",
            "price": base + random.randint(-90, 220),
            "class": random.choice(["Economy", "Premium Economy", "Business"]),
            "seats_left": random.randint(5, 35)
        })
    return sorted(flights, key=lambda x: x["price"])

if "bookings" not in st.session_state:
    st.session_state.bookings = []
if "current_booking" not in st.session_state:
    st.session_state.current_booking = None

tab1, tab2, tab3 = st.tabs(["🔍 Search & Book", "🎫 My Tickets", "🧾 Receipts"])

with tab1:
    st.header("Search Flights Worldwide")
    c1, c2, c3, c4 = st.columns([2.2, 2.2, 1.8, 1.3])
    with c1: origin = st.selectbox("From", CITIES, index=0)
    with c2: destination = st.selectbox("To", CITIES, index=1)
    with c3: date = st.date_input("Date", datetime.now() + timedelta(days=14))
    with c4: pax = st.number_input("Passengers", 1, 5, 1)

    if st.button("Search Flights", type="primary", use_container_width=True):
        if origin == destination:
            st.error("Choose different cities.")
        else:
            st.session_state.results = generate_flights(origin, destination)
            st.session_state.params = {"origin": origin, "destination": destination, "date": date}

    if "results" in st.session_state:
        st.subheader(f"Flights • {st.session_state.params['origin']} → {st.session_state.params['destination']}")
        for f in st.session_state.results:
            with st.container(border=True):
                col1, col2, col3, col4 = st.columns([3.3, 2.2, 2, 2.5])
                with col1:
                    st.markdown(f"**{f['airline']}**  \n`{f['flight_number']}`")
                with col2:
                    st.markdown(f"**{f['departure']}** → **{f['arrival']}**  \n{f['duration']}")
                with col3:
                    st.markdown(f"**${f['price']:,}**  \n{f['class']}")
                    st.caption(f"{f['seats_left']} seats left")
                with col4:
                    if st.button("Book", key=f['id'], use_container_width=True):
                        st.session_state.current_booking = f.copy()
                        st.session_state.current_booking.update(st.session_state.params)
                        st.rerun()

if st.session_state.current_booking:
    st.divider()
    f = st.session_state.current_booking
    st.header("Complete Booking")
    st.subheader(f"{f['airline']} • {f['flight_number']}")
    st.write(f"**{f['origin']}** → **{f['destination']}** • {f['date']}")

    st.markdown("### Add Extras")
    col1, col2 = st.columns(2)
    with col1:
        seat = st.selectbox("Seat", ["Window", "Aisle", "No Preference"])
        baggage = st.checkbox("Extra 23kg Baggage (+$89)")
        meal = st.selectbox("Meal", ["Standard", "Vegetarian", "Halal", "Kosher"])
    with col2:
        priority = st.checkbox("Priority Boarding (+$49)")
        insurance = st.checkbox("Travel Insurance (+$35/person)", value=True)

    st.markdown("### Passenger Details")
    name = st.text_input("Full Name", value="Troy Adebayo")
    email = st.text_input("Email", value="troy@example.com")
    phone = st.text_input("Phone", value="+234 803 555 0123")

    if st.button("✅ Confirm & Generate Ticket", type="primary", use_container_width=True):
        total = f['price'] + (89 if baggage else 0) + (49 if priority else 0) + (35 if insurance else 0)
        booking = {
            "booking_id": f"GW{random.randint(100000,999999)}",
            "pnr": ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=6)),
            "flight": f,
            "passenger": {"name": name, "email": email, "phone": phone},
            "add_ons": {"seat": seat, "baggage": baggage, "meal": meal, "priority": priority, "insurance": insurance},
            "total_price": total,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "status": "Confirmed"
        }
        st.session_state.bookings.append(booking)
        st.session_state.last_booking = booking
        st.session_state.current_booking = None
        st.success("Booking Confirmed! Your ticket is ready.")
        st.balloons()
        st.rerun()

with tab2:
    st.header("My Tickets")
    if not st.session_state.bookings:
        st.info("No tickets yet. Book your first flight above.")
    else:
        for booking in st.session_state.bookings:
            style = get_style(booking['flight']['airline'])
            with st.expander(f"✈️ {booking['flight']['airline']} • {booking['flight']['origin']} → {booking['flight']['destination']} • {booking['pnr']}", expanded=True):
                
                # CLEAN NATIVE TICKET PREVIEW
                st.subheader("🎫 E-Ticket Preview")
                
                with st.container(border=True):
                    # Airline header
                    st.markdown(f"""
                    <div style="background: {style['primary']}; color: white; padding: 14px 20px; border-radius: 10px 10px 0 0; margin-bottom: 0;">
                        <h3 style="margin:0; color:white;">{booking['flight']['airline']}</h3>
                        <p style="margin:0; color:#cbd5e1; font-size:0.9em;">{style['tagline']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Main content
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.metric("From", booking['flight']['origin'], booking['flight']['departure'])
                    with c2:
                        st.metric("Flight", booking['flight']['flight_number'], booking['flight']['duration'])
                    with c3:
                        st.metric("To", booking['flight']['destination'], booking['flight']['arrival'])
                    
                    st.divider()
                    
                    p1, p2, p3, p4 = st.columns(4)
                    with p1:
                        st.write("**Passenger**")
                        st.write(booking['passenger']['name'])
                    with p2:
                        st.write("**Class**")
                        st.write(booking['flight']['class'])
                    with p3:
                        st.write("**Seat**")
                        st.write(booking['add_ons']['seat'])
                    with p4:
                        st.write("**Date**")
                        st.write(booking['flight']['date'])
                    
                    st.success("CONFIRMED", icon="✅")

                # Download PDF
                if st.button(f"📥 Download {booking['flight']['airline']} Ticket (PDF)", key=f"pdf_{booking['pnr']}"):
                    buffer = io.BytesIO()
                    c = canvas.Canvas(buffer, pagesize=A4)
                    style = get_style(booking['flight']['airline'])
                    
                    # Header
                    c.setFillColor(HexColor(style['primary']))
                    c.rect(0, A4[1]-80, A4[0], 80, fill=True, stroke=False)
                    c.setFillColor(white)
                    c.setFont("Helvetica-Bold", 20)
                    c.drawString(35, A4[1]-42, booking['flight']['airline'])
                    c.setFont("Helvetica", 9)
                    c.drawString(35, A4[1]-58, style['tagline'])
                    
                    # Title
                    c.setFillColor(black)
                    c.setFont("Helvetica-Bold", 12)
                    c.drawString(35, A4[1]-105, "E-TICKET / BOARDING PASS")
                    
                    # Details
                    c.setFont("Helvetica", 10)
                    y = A4[1] - 130
                    for line in [
                        f"PNR: {booking['pnr']}",
                        f"Passenger: {booking['passenger']['name']}",
                        f"Flight: {booking['flight']['airline']} {booking['flight']['flight_number']}",
                        f"Route: {booking['flight']['origin']} → {booking['flight']['destination']}",
                        f"Date: {booking['flight']['date']}   {booking['flight']['departure']} - {booking['flight']['arrival']}",
                        f"Class: {booking['flight']['class']}   Seat: {booking['add_ons']['seat']}",
                        f"Status: CONFIRMED"
                    ]:
                        c.drawString(35, y, line)
                        y -= 16
                    
                    # Barcode simulation
                    c.setStrokeColor(HexColor("#444444"))
                    c.setLineWidth(0.7)
                    for i in range(55):
                        if random.random() > 0.45:
                            c.line(35 + i*5, 95, 35 + i*5, 130)
                    c.setFont("Helvetica", 8)
                    c.drawCentredString(A4[0]/2, 80, booking['pnr'])
                    
                    c.setFont("Helvetica-Oblique", 8)
                    c.drawString(35, 45, f"Thank you for flying with {booking['flight']['airline']}. Safe travels!")
                    c.save()
                    buffer.seek(0)
                    
                    st.download_button("Download Ticket", buffer, 
                                       file_name=f"{booking['flight']['airline'].replace(' ','')}_Ticket_{booking['pnr']}.pdf",
                                       mime="application/pdf")

with tab3:
    st.header("Receipts")
    if not st.session_state.bookings:
        st.info("No receipts yet.")
    else:
        for b in st.session_state.bookings:
            with st.container(border=True):
                st.write(f"**Receipt #{b['booking_id']}** • {b['passenger']['name']}")
                st.write(f"Total Paid: **${b['total_price']:,}**")
                if st.button(f"Download Receipt", key=f"rc_{b['pnr']}"):
                    buffer = io.BytesIO()
                    c = canvas.Canvas(buffer, pagesize=A4)
                    c.setFont("Helvetica-Bold", 14)
                    c.drawString(40, A4[1]-55, "GlobalWings - Receipt")
                    c.setFont("Helvetica", 10)
                    y = A4[1]-80
                    for line in [
                        f"Receipt No: {b['booking_id']}",
                        f"Date: {b['date']}",
                        f"Passenger: {b['passenger']['name']}",
                        f"Flight: {b['flight']['airline']} {b['flight']['flight_number']}",
                        f"Total Paid: ${b['total_price']:,}"
                    ]:
                        c.drawString(40, y, line)
                        y -= 15
                    c.setFont("Helvetica-Oblique", 8)
                    c.drawString(40, 50, "Thank you for choosing GlobalWings.")
                    c.save()
                    buffer.seek(0)
                    st.download_button("Download Receipt", buffer, file_name=f"Receipt_{b['pnr']}.pdf")

st.markdown("---")
st.caption("GlobalWings — Book any airline in the world. Demo with realistic sample data.")