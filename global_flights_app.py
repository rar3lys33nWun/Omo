#!/usr/bin/env python3
"""
GlobalWings - Your Global Flight Booking Platform
Clean, professional ticket preview + realistic PDF tickets & receipts.

Requirements:
pip install streamlit reportlab

Made with love for you, Troy 💕
"""

import streamlit as st
from datetime import datetime, timedelta
import random
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, cm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, black, white
import io

st.set_page_config(
    page_title="GlobalWings - Book Flights Worldwide",
    page_icon="✈️",
    layout="wide"
)

# ==================== HEADER ====================
st.markdown("""
<div style="text-align: center; padding: 15px 0 25px 0;">
    <h1 style="color: #0f172a; font-size: 2.8em; margin-bottom: 5px;">✈️ GlobalWings</h1>
    <p style="font-size: 1.15em; color: #475569;">Fly the World • Book Any Airline • Premium Experience</p>
</div>
""", unsafe_allow_html=True)

# ==================== DATA ====================
AIRLINES = ["Emirates", "Qatar Airways", "Delta Air Lines", "Lufthansa", "Air France", "Singapore Airlines", "British Airways", "Etihad Airways"]

CITIES = ["Lagos (LOS)", "Dubai (DXB)", "London (LHR)", "New York (JFK)", "Paris (CDG)", 
          "Singapore (SIN)", "Johannesburg (JNB)", "Istanbul (IST)", "Mumbai (BOM)", "Los Angeles (LAX)"]

def generate_sample_flights(origin, destination, date):
    flights = []
    base_price = random.randint(480, 1750)
    for _ in range(5):
        airline = random.choice(AIRLINES)
        dep_hour = random.randint(5, 23)
        duration = random.randint(5, 15)
        arr_hour = (dep_hour + duration) % 24
        flight = {
            "id": f"GW{random.randint(10000, 99999)}",
            "airline": airline,
            "flight_number": f"{airline[:2].upper()}{random.randint(100, 999)}",
            "origin": origin,
            "destination": destination,
            "departure": f"{dep_hour:02d}:{random.randint(0,59):02d}",
            "arrival": f"{arr_hour:02d}:{random.randint(0,59):02d}",
            "duration": f"{duration}h {random.randint(10,55)}m",
            "price": base_price + random.randint(-120, 280),
            "class": random.choice(["Economy", "Premium Economy", "Business"]),
            "seats_left": random.randint(7, 42)
        }
        flights.append(flight)
    return sorted(flights, key=lambda x: x["price"])

# ==================== SESSION ====================
if "bookings" not in st.session_state:
    st.session_state.bookings = []
if "current_booking" not in st.session_state:
    st.session_state.current_booking = None

# ==================== TABS ====================
tab1, tab2, tab3 = st.tabs(["🔍 Search & Book", "🎫 My Trips & Tickets", "🧾 Receipts"])

# ==================== TAB 1: SEARCH ====================
with tab1:
    st.header("Search Flights Across the World")
    
    c1, c2, c3, c4 = st.columns([2.2, 2.2, 1.8, 1.3])
    with c1:
        origin = st.selectbox("From", CITIES, index=0)
    with c2:
        destination = st.selectbox("To", CITIES, index=1)
    with c3:
        travel_date = st.date_input("Date", datetime.now() + timedelta(days=10))
    with c4:
        passengers = st.number_input("Passengers", 1, 5, 1)

    if st.button("Search Flights", type="primary", use_container_width=True):
        if origin == destination:
            st.error("Please choose different cities.")
        else:
            with st.spinner("Searching global airlines..."):
                st.session_state.search_results = generate_sample_flights(origin, destination, travel_date)
                st.session_state.search_params = {"origin": origin, "destination": destination, "date": travel_date}

    if "search_results" in st.session_state:
        st.subheader(f"Flights from {st.session_state.search_params['origin']} to {st.session_state.search_params['destination']}")
        
        for flight in st.session_state.search_results:
            with st.container(border=True):
                col1, col2, col3, col4 = st.columns([3.5, 2, 2, 2.5])
                
                with col1:
                    st.markdown(f"**{flight['airline']}**  \n`{flight['flight_number']}`")
                with col2:
                    st.markdown(f"**{flight['departure']}** → **{flight['arrival']}**  \n{flight['duration']}")
                with col3:
                    st.markdown(f"**${flight['price']:,}**  \n{flight['class']}")
                    st.caption(f"{flight['seats_left']} seats left")
                with col4:
                    if st.button("Select & Book", key=flight['id'], use_container_width=True):
                        st.session_state.current_booking = flight.copy()
                        st.session_state.current_booking.update(st.session_state.search_params)
                        st.rerun()

# ==================== BOOKING FORM ====================
if st.session_state.current_booking:
    st.divider()
    flight = st.session_state.current_booking
    st.header("Complete Your Booking")
    
    st.subheader(f"{flight['airline']} • {flight['flight_number']}")
    st.write(f"**{flight['origin']}** → **{flight['destination']}** • {flight['date']}")
    
    # Add-ons
    st.markdown("### Add Extras")
    col_a, col_b = st.columns(2)
    with col_a:
        seat = st.selectbox("Seat Preference", ["Window", "Aisle", "No Preference"])
        baggage = st.checkbox("Extra 23kg Baggage (+$89)")
        meal = st.selectbox("Meal", ["Standard", "Vegetarian", "Halal", "Kosher"])
    with col_b:
        priority = st.checkbox("Priority Boarding (+$49)")
        insurance = st.checkbox("Travel Insurance (+$35/person)", value=True)

    # Passenger Info
    st.markdown("### Passenger Details")
    name = st.text_input("Full Name (as on passport)", value="Troy Adebayo")
    email = st.text_input("Email", value="troy@example.com")
    phone = st.text_input("Phone", value="+234 803 555 0123")

    if st.button("✅ Confirm & Generate Ticket", type="primary", use_container_width=True):
        total = flight['price']
        if baggage: total += 89
        if priority: total += 49
        if insurance: total += 35 * passengers

        booking = {
            "booking_id": f"GW{random.randint(100000,999999)}",
            "pnr": ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=6)),
            "flight": flight,
            "passenger": {"name": name, "email": email, "phone": phone},
            "add_ons": {"seat": seat, "baggage": baggage, "meal": meal, "priority": priority, "insurance": insurance},
            "total_price": total,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "status": "Confirmed"
        }
        st.session_state.bookings.append(booking)
        st.session_state.last_booking = booking
        st.session_state.current_booking = None
        st.success("Booking Confirmed! Your ticket is ready below.")
        st.balloons()
        st.rerun()

# ==================== TAB 2: MY TRIPS ====================
with tab2:
    st.header("My Trips & Tickets")
    
    if not st.session_state.bookings:
        st.info("No bookings yet. Go to the Search tab to book your first flight.")
    else:
        for booking in st.session_state.bookings:
            with st.expander(f"✈️ {booking['flight']['airline']} • {booking['flight']['origin']} → {booking['flight']['destination']} • {booking['pnr']}", expanded=True):
                
                # === CLEAN TICKET PREVIEW (Native Streamlit) ===
                st.subheader("🎫 E-Ticket Preview")
                
                with st.container(border=True):
                    # Header
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"### {booking['flight']['airline']}")
                        st.caption(f"GlobalWings • PNR: **{booking['pnr']}**")
                    with col2:
                        st.success("CONFIRMED", icon="✅")

                    st.divider()

                    # Flight details
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.metric("From", booking['flight']['origin'], booking['flight']['departure'])
                    with c2:
                        st.metric("Flight", booking['flight']['flight_number'], booking['flight']['duration'])
                    with c3:
                        st.metric("To", booking['flight']['destination'], booking['flight']['arrival'])

                    st.divider()

                    # Passenger & details
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

                # Download PDF Ticket
                if st.button(f"📥 Download Official Ticket PDF", key=f"pdf_{booking['pnr']}"):
                    buffer = io.BytesIO()
                    c = canvas.Canvas(buffer, pagesize=A4)
                    
                    # Header bar
                    c.setFillColor(HexColor("#0f172a"))
                    c.rect(0, A4[1]-70, A4[0], 70, fill=True, stroke=False)
                    c.setFillColor(white)
                    c.setFont("Helvetica-Bold", 20)
                    c.drawString(40, A4[1]-45, "GlobalWings")
                    c.setFont("Helvetica", 10)
                    c.drawString(40, A4[1]-62, "Your Global Flight Partner")

                    # Content
                    c.setFillColor(black)
                    c.setFont("Helvetica-Bold", 14)
                    c.drawString(40, A4[1]-100, "E-TICKET / BOARDING PASS")
                    
                    c.setFont("Helvetica", 11)
                    y = A4[1] - 130
                    lines = [
                        f"Booking Reference (PNR): {booking['pnr']}",
                        f"Passenger: {booking['passenger']['name']}",
                        f"Flight: {booking['flight']['airline']} {booking['flight']['flight_number']}",
                        f"Route: {booking['flight']['origin']}  →  {booking['flight']['destination']}",
                        f"Date: {booking['flight']['date']}    Departure: {booking['flight']['departure']}",
                        f"Class: {booking['flight']['class']}    Seat: {booking['add_ons']['seat']}",
                        f"Status: CONFIRMED"
                    ]
                    for line in lines:
                        c.drawString(40, y, line)
                        y -= 18
                    
                    c.setFont("Helvetica-Oblique", 10)
                    c.drawString(40, 80, "Thank you for choosing GlobalWings. Safe travels!")
                    c.save()
                    buffer.seek(0)
                    
                    st.download_button("Download Ticket PDF", buffer, 
                                       file_name=f"GlobalWings_Ticket_{booking['pnr']}.pdf", 
                                       mime="application/pdf")

# ==================== TAB 3: RECEIPTS ====================
with tab3:
    st.header("Receipts")
    if not st.session_state.bookings:
        st.info("No receipts yet.")
    else:
        for booking in st.session_state.bookings:
            with st.container(border=True):
                st.write(f"**Receipt for {booking['booking_id']}**")
                st.write(f"Passenger: {booking['passenger']['name']}")
                st.write(f"Total Paid: **${booking['total_price']:,}**")
                
                if st.button(f"Download Receipt PDF", key=f"receipt_{booking['pnr']}"):
                    buffer = io.BytesIO()
                    c = canvas.Canvas(buffer, pagesize=A4)
                    c.setFont("Helvetica-Bold", 16)
                    c.drawString(40, A4[1]-60, "GlobalWings - Payment Receipt")
                    c.setFont("Helvetica", 11)
                    y = A4[1]-95
                    for line in [
                        f"Receipt No: {booking['booking_id']}",
                        f"Date: {booking['date']}",
                        f"Passenger: {booking['passenger']['name']}",
                        f"Flight: {booking['flight']['airline']} {booking['flight']['flight_number']}",
                        f"Base Fare: ${booking['flight']['price']:,}",
                        f"Add-ons Total: ${booking['total_price'] - booking['flight']['price']:,}",
                        f"TOTAL PAID: ${booking['total_price']:,}"
                    ]:
                        c.drawString(40, y, line)
                        y -= 18
                    c.setFont("Helvetica-Oblique", 9)
                    c.drawString(40, 60, "This is a computer-generated receipt from GlobalWings.")
                    c.save()
                    buffer.seek(0)
                    st.download_button("Download Receipt", buffer, 
                                       file_name=f"GlobalWings_Receipt_{booking['pnr']}.pdf")

st.markdown("---")
st.caption("GlobalWings — Connecting the world. This is a demo platform with sample data.")