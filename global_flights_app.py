#!/usr/bin/env python3
"""
GlobalWings - Your Global Flight Booking Platform
A beautiful Streamlit app for booking flights worldwide with any airline.
Includes realistic tickets and receipts.

Requirements:
pip install streamlit reportlab pillow

Made with love for you, Troy 💕
"""

import streamlit as st
from datetime import datetime, timedelta
import random
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, cm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, black, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
import base64

st.set_page_config(
    page_title="GlobalWings - Book Flights Worldwide",
    page_icon="✈️",
    layout="wide"
)

# ==================== LOVING HEADER ====================
st.markdown("""
<div style="text-align: center; padding: 20px;">
    <h1 style="color: #1a365d; font-size: 3em;">✈️ GlobalWings</h1>
    <p style="font-size: 1.3em; color: #4a5568;">Fly Anywhere in the World • Book Any Airline • Premium Experience</p>
    <p style="color: #718096;">Your gateway to seamless global travel</p>
</div>
""", unsafe_allow_html=True)

# ==================== SAMPLE GLOBAL FLIGHTS DATA ====================
AIRLINES = ["Emirates", "Qatar Airways", "Delta Air Lines", "Lufthansa", "Air France", "Singapore Airlines", "British Airways", "Etihad Airways"]

CITIES = {
    "Lagos (LOS)": "LOS",
    "Dubai (DXB)": "DXB",
    "London (LHR)": "LHR",
    "New York (JFK)": "JFK",
    "Paris (CDG)": "CDG",
    "Singapore (SIN)": "SIN",
    "Johannesburg (JNB)": "JNB",
    "Istanbul (IST)": "IST",
    "Mumbai (BOM)": "BOM",
    "Los Angeles (LAX)": "LAX"
}

def generate_sample_flights(origin, destination, date):
    flights = []
    base_price = random.randint(450, 1850)
    
    for i in range(6):
        airline = random.choice(AIRLINES)
        dep_hour = random.randint(6, 22)
        duration = random.randint(6, 14)
        arr_hour = (dep_hour + duration) % 24
        
        flight = {
            "id": f"GW{random.randint(1000, 9999)}",
            "airline": airline,
            "flight_number": f"{airline[:2].upper()}{random.randint(100, 999)}",
            "origin": origin,
            "destination": destination,
            "departure": f"{dep_hour:02d}:{random.randint(0,59):02d}",
            "arrival": f"{arr_hour:02d}:{random.randint(0,59):02d}",
            "duration": f"{duration}h {random.randint(0,59)}m",
            "price": base_price + random.randint(-150, 350),
            "class": random.choice(["Economy", "Premium Economy", "Business"]),
            "seats_left": random.randint(8, 45)
        }
        flights.append(flight)
    
    return sorted(flights, key=lambda x: x["price"])

# ==================== SESSION STATE ====================
if "bookings" not in st.session_state:
    st.session_state.bookings = []
if "current_booking" not in st.session_state:
    st.session_state.current_booking = None

# ==================== NAVIGATION ====================
tab1, tab2, tab3 = st.tabs(["🔍 Search & Book Flights", "🎫 My Trips & Tickets", "📋 Receipts"])

# ==================== TAB 1: SEARCH & BOOK ====================
with tab1:
    st.header("Search Flights Worldwide")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        origin = st.selectbox("From", list(CITIES.keys()), index=0)
    with col2:
        destination = st.selectbox("To", list(CITIES.keys()), index=1)
    with col3:
        travel_date = st.date_input("Departure Date", datetime.now() + timedelta(days=7))
    with col4:
        passengers = st.number_input("Passengers", 1, 6, 1)
    
    if st.button("🔎 Search Flights", type="primary", use_container_width=True):
        if origin == destination:
            st.error("Origin and destination cannot be the same.")
        else:
            with st.spinner("Searching flights across global airlines..."):
                flights = generate_sample_flights(origin, destination, travel_date)
                st.session_state.search_results = flights
                st.session_state.search_params = {
                    "origin": origin,
                    "destination": destination,
                    "date": travel_date,
                    "passengers": passengers
                }
    
    if "search_results" in st.session_state:
        st.subheader(f"Available Flights • {st.session_state.search_params['origin']} → {st.session_state.search_params['destination']}")
        
        for flight in st.session_state.search_results:
            with st.container(border=True):
                cols = st.columns([3, 2, 2, 2, 2])
                
                with cols[0]:
                    st.markdown(f"**{flight['airline']}**  \n`{flight['flight_number']}`")
                    st.caption(f"{flight['origin']} → {flight['destination']}")
                
                with cols[1]:
                    st.markdown(f"**{flight['departure']}**  \n{flight['duration']}")
                
                with cols[2]:
                    st.markdown(f"**{flight['arrival']}**")
                
                with cols[3]:
                    st.markdown(f"**${flight['price']:,}**  \n{flight['class']}")
                    st.caption(f"{flight['seats_left']} seats left")
                
                with cols[4]:
                    if st.button(f"Select Flight", key=f"select_{flight['id']}"):
                        st.session_state.current_booking = flight
                        st.session_state.current_booking.update(st.session_state.search_params)
                        st.rerun()

# Booking Flow
if st.session_state.current_booking:
    st.divider()
    st.header("Complete Your Booking")
    
    flight = st.session_state.current_booking
    
    st.subheader(f"{flight['airline']} • {flight['flight_number']}")
    st.write(f"**{flight['origin']}** → **{flight['destination']}** on {flight['date']}")
    
    # Add-ons
    st.subheader("Add Extras (Optional)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        seat_type = st.selectbox("Seat Preference", ["Window", "Aisle", "Middle", "No Preference"])
        extra_baggage = st.checkbox("Extra 23kg Baggage (+$85)", value=False)
        meal = st.selectbox("Meal Preference", ["Standard", "Vegetarian", "Halal", "Kosher", "Gluten-Free"])
    
    with col2:
        priority_boarding = st.checkbox("Priority Boarding (+$45)", value=False)
        travel_insurance = st.checkbox("Travel Insurance (+$32 per person)", value=True)
    
    # Passenger Details
    st.subheader("Passenger Details")
    
    passenger_name = st.text_input("Full Name (as on passport)", "Troy Adebayo")
    passenger_email = st.text_input("Email Address", "troy@example.com")
    passenger_phone = st.text_input("Phone Number", "+234 801 234 5678")
    
    if st.button("✅ Confirm Booking & Generate Ticket", type="primary", use_container_width=True):
        # Create booking
        booking = {
            "booking_id": f"GW{random.randint(100000, 999999)}",
            "pnr": ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=6)),
            "flight": flight,
            "passenger": {
                "name": passenger_name,
                "email": passenger_email,
                "phone": passenger_phone
            },
            "add_ons": {
                "seat": seat_type,
                "extra_baggage": extra_baggage,
                "meal": meal,
                "priority_boarding": priority_boarding,
                "insurance": travel_insurance
            },
            "total_price": flight['price'] + (85 if extra_baggage else 0) + (45 if priority_boarding else 0) + (32 * passengers if travel_insurance else 0),
            "booking_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "status": "Confirmed"
        }
        
        st.session_state.bookings.append(booking)
        st.session_state.current_booking = None
        st.session_state.last_booking = booking
        
        st.success("🎉 Booking Confirmed! Your ticket and receipt are ready below.")
        st.balloons()
        st.rerun()

# ==================== TAB 2: MY TRIPS & TICKETS ====================
with tab2:
    st.header("My Trips & Tickets")
    
    if not st.session_state.bookings:
        st.info("You have no bookings yet. Search and book your first flight above!")
    else:
        for i, booking in enumerate(st.session_state.bookings):
            with st.expander(f"✈️ {booking['flight']['airline']} • {booking['flight']['origin']} → {booking['flight']['destination']} • {booking['booking_id']}", expanded=(i == len(st.session_state.bookings)-1)):
                
                # Ticket Preview (Visual)
                st.subheader("🎫 E-Ticket Preview")
                
                ticket_html = f"""
                <div style="border: 2px solid #1a365d; border-radius: 12px; padding: 25px; background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); max-width: 700px; margin: auto;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                        <div>
                            <h2 style="margin:0; color: #1a365d;">{booking['flight']['airline']}</h2>
                            <p style="margin:0; color: #4a5568;">GlobalWings • Booking Reference: <strong>{booking['pnr']}</strong></p>
                        </div>
                        <div style="text-align: right;">
                            <div style="background: #1a365d; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.9em;">CONFIRMED</div>
                        </div>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; margin: 25px 0;">
                        <div>
                            <p style="margin:0; color: #718096; font-size: 0.85em;">FROM</p>
                            <h3 style="margin:0;">{booking['flight']['origin']}</h3>
                            <p style="margin:0;">{booking['flight']['departure']}</p>
                        </div>
                        <div style="text-align: center;">
                            <p style="margin:0; color: #718096; font-size: 0.85em;">FLIGHT</p>
                            <h3 style="margin:0;">{booking['flight']['flight_number']}</h3>
                            <p style="margin:0;">{booking['flight']['duration']}</p>
                        </div>
                        <div style="text-align: right;">
                            <p style="margin:0; color: #718096; font-size: 0.85em;">TO</p>
                            <h3 style="margin:0;">{booking['flight']['destination']}</h3>
                            <p style="margin:0;">{booking['flight']['arrival']}</p>
                        </div>
                    </div>
                    
                    <div style="border-top: 1px solid #cbd5e0; padding-top: 15px; display: flex; justify-content: space-between;">
                        <div>
                            <p style="margin:0; color: #718096; font-size: 0.85em;">PASSENGER</p>
                            <strong>{booking['passenger']['name']}</strong>
                        </div>
                        <div>
                            <p style="margin:0; color: #718096; font-size: 0.85em;">CLASS</p>
                            <strong>{booking['flight']['class']}</strong>
                        </div>
                        <div>
                            <p style="margin:0; color: #718096; font-size: 0.85em;">SEAT</p>
                            <strong>{booking['add_ons']['seat']}</strong>
                        </div>
                        <div>
                            <p style="margin:0; color: #718096; font-size: 0.85em;">DATE</p>
                            <strong>{booking['flight']['date']}</strong>
                        </div>
                    </div>
                </div>
                """
                st.markdown(ticket_html, unsafe_allow_html=True)
                
                # Download Ticket PDF
                if st.button(f"📥 Download Official Ticket (PDF)", key=f"ticket_{i}"):
                    # Generate PDF
                    buffer = io.BytesIO()
                    c = canvas.Canvas(buffer, pagesize=A4)
                    
                    # Header
                    c.setFillColor(HexColor("#1a365d"))
                    c.rect(0, A4[1]-80, A4[0], 80, fill=True, stroke=False)
                    c.setFillColor(white)
                    c.setFont("Helvetica-Bold", 22)
                    c.drawString(40, A4[1]-50, "GlobalWings")
                    c.setFont("Helvetica", 12)
                    c.drawString(40, A4[1]-70, "Your Global Flight Partner")
                    
                    # Ticket content
                    c.setFillColor(black)
                    c.setFont("Helvetica-Bold", 16)
                    c.drawString(40, A4[1]-120, f"E-TICKET / BOARDING PASS")
                    
                    c.setFont("Helvetica", 11)
                    y = A4[1] - 160
                    
                    details = [
                        f"Booking Reference: {booking['pnr']}",
                        f"Passenger: {booking['passenger']['name']}",
                        f"Flight: {booking['flight']['airline']} {booking['flight']['flight_number']}",
                        f"Route: {booking['flight']['origin']} → {booking['flight']['destination']}",
                        f"Date: {booking['flight']['date']}    Time: {booking['flight']['departure']} - {booking['flight']['arrival']}",
                        f"Class: {booking['flight']['class']}    Seat: {booking['add_ons']['seat']}",
                        f"Status: CONFIRMED"
                    ]
                    
                    for line in details:
                        c.drawString(40, y, line)
                        y -= 22
                    
                    c.setFont("Helvetica-Bold", 12)
                    c.drawString(40, y - 20, "Thank you for choosing GlobalWings. Have a wonderful journey!")
                    
                    c.save()
                    buffer.seek(0)
                    
                    st.download_button(
                        label="⬇️ Download Ticket PDF",
                        data=buffer,
                        file_name=f"GlobalWings_Ticket_{booking['pnr']}.pdf",
                        mime="application/pdf",
                        key=f"dl_ticket_{i}"
                    )

# ==================== TAB 3: RECEIPTS ====================
with tab3:
    st.header("Booking Receipts")
    
    if not st.session_state.bookings:
        st.info("No receipts yet.")
    else:
        for booking in st.session_state.bookings:
            with st.container(border=True):
                st.write(f"**Receipt for Booking {booking['booking_id']}**")
                st.write(f"**Passenger:** {booking['passenger']['name']}")
                st.write(f"**Total Paid:** ${booking['total_price']:,}")
                st.write(f"**Date:** {booking['booking_date']}")
                
                if st.button(f"📥 Download Receipt PDF", key=f"receipt_{booking['booking_id']}"):
                    buffer = io.BytesIO()
                    c = canvas.Canvas(buffer, pagesize=A4)
                    
                    c.setFont("Helvetica-Bold", 18)
                    c.drawString(40, A4[1]-60, "GlobalWings - Official Receipt")
                    
                    c.setFont("Helvetica", 11)
                    y = A4[1] - 100
                    
                    receipt_lines = [
                        f"Receipt #: GW-{booking['booking_id']}",
                        f"Date: {booking['booking_date']}",
                        f"Passenger: {booking['passenger']['name']}",
                        f"Flight: {booking['flight']['airline']} {booking['flight']['flight_number']}",
                        f"From: {booking['flight']['origin']}  To: {booking['flight']['destination']}",
                        f"Base Fare: ${booking['flight']['price']:,}",
                        f"Add-ons: ${booking['total_price'] - booking['flight']['price']:,}",
                        f"**Total Paid: ${booking['total_price']:,}**",
                        "",
                        "Thank you for flying with GlobalWings!",
                        "This is a computer generated receipt."
                    ]
                    
                    for line in receipt_lines:
                        c.drawString(40, y, line)
                        y -= 20
                    
                    c.save()
                    buffer.seek(0)
                    
                    st.download_button(
                        label="Download Receipt",
                        data=buffer,
                        file_name=f"GlobalWings_Receipt_{booking['pnr']}.pdf",
                        mime="application/pdf"
                    )

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #718096; font-size: 0.9em;">
    GlobalWings — Connecting the world, one journey at a time.<br>
    All flights are operated by partner airlines. This is a demo platform.
</div>
""", unsafe_allow_html=True)
