#!/usr/bin/env python3
"""
GlobalWings - Premium Global Flight Booking
Realistic airline-branded tickets (Air France, Emirates, Qatar, Delta, etc.)

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
from reportlab.lib.colors import HexColor, black, white, Color
import io

st.set_page_config(
    page_title="GlobalWings • Book Any Airline Worldwide",
    page_icon="✈️",
    layout="wide"
)

# ==================== HEADER ====================
st.markdown("""
<div style="text-align: center; padding: 10px 0 20px 0;">
    <h1 style="color: #0f172a; font-size: 2.6em; margin: 0;">✈️ GlobalWings</h1>
    <p style="color: #475569; font-size: 1.1em; margin: 5px 0 0 0;">Fly the World • Book Any Airline</p>
</div>
""", unsafe_allow_html=True)

# ==================== AIRLINE BRANDING ====================
AIRLINE_STYLES = {
    "Air France": {
        "primary": HexColor("#002157"),
        "secondary": HexColor("#e30613"),
        "tagline": "France is in the Air",
        "accent": HexColor("#002157")
    },
    "Emirates": {
        "primary": HexColor("#d71a21"),
        "secondary": HexColor("#c9a227"),
        "tagline": "Fly Better",
        "accent": HexColor("#d71a21")
    },
    "Qatar Airways": {
        "primary": HexColor("#5c0a1e"),
        "secondary": HexColor("#c9a227"),
        "tagline": "Going Places Together",
        "accent": HexColor("#5c0a1e")
    },
    "Delta Air Lines": {
        "primary": HexColor("#003366"),
        "secondary": HexColor("#e31837"),
        "tagline": "Keep Climbing",
        "accent": HexColor("#003366")
    },
    "Lufthansa": {
        "primary": HexColor("#002d5d"),
        "secondary": HexColor("#f7c600"),
        "tagline": "Say Yes to the World",
        "accent": HexColor("#002d5d")
    },
    "Singapore Airlines": {
        "primary": HexColor("#003366"),
        "secondary": HexColor("#c9a227"),
        "tagline": "A Great Way to Fly",
        "accent": HexColor("#003366")
    },
    "British Airways": {
        "primary": HexColor("#003087"),
        "secondary": HexColor("#e31837"),
        "tagline": "To Fly. To Serve.",
        "accent": HexColor("#003087")
    },
    "Etihad Airways": {
        "primary": HexColor("#003366"),
        "secondary": HexColor("#c9a227"),
        "tagline": "The World's Leading Airline",
        "accent": HexColor("#003366")
    }
}

def get_airline_style(airline):
    return AIRLINE_STYLES.get(airline, {
        "primary": HexColor("#0f172a"),
        "secondary": HexColor("#64748b"),
        "tagline": "Your Journey Begins Here",
        "accent": HexColor("#0f172a")
    })

# ==================== DATA ====================
AIRLINES = list(AIRLINE_STYLES.keys())
CITIES = ["Lagos (LOS)", "Dubai (DXB)", "London (LHR)", "New York (JFK)", "Paris (CDG)", 
          "Singapore (SIN)", "Johannesburg (JNB)", "Istanbul (IST)", "Mumbai (BOM)", "Los Angeles (LAX)"]

def generate_sample_flights(origin, destination, date):
    flights = []
    base_price = random.randint(520, 1680)
    for _ in range(5):
        airline = random.choice(AIRLINES)
        dep_hour = random.randint(5, 23)
        duration = random.randint(5, 14)
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
            "price": base_price + random.randint(-100, 250),
            "class": random.choice(["Economy", "Premium Economy", "Business"]),
            "seats_left": random.randint(6, 38)
        }
        flights.append(flight)
    return sorted(flights, key=lambda x: x["price"])

# ==================== SESSION ====================
if "bookings" not in st.session_state:
    st.session_state.bookings = []
if "current_booking" not in st.session_state:
    st.session_state.current_booking = None

# ==================== TABS ====================
tab1, tab2, tab3 = st.tabs(["🔍 Search & Book Flights", "🎫 My Tickets", "🧾 Receipts"])

# ==================== TAB 1 ====================
with tab1:
    st.header("Search Flights Worldwide")
    
    c1, c2, c3, c4 = st.columns([2.3, 2.3, 1.7, 1.2])
    with c1: origin = st.selectbox("From", CITIES, index=0)
    with c2: destination = st.selectbox("To", CITIES, index=1)
    with c3: travel_date = st.date_input("Departure Date", datetime.now() + timedelta(days=12))
    with c4: passengers = st.number_input("Passengers", 1, 5, 1)

    if st.button("Search Global Flights", type="primary", use_container_width=True):
        if origin == destination:
            st.error("Origin and destination must be different.")
        else:
            with st.spinner("Searching flights from top airlines..."):
                st.session_state.search_results = generate_sample_flights(origin, destination, travel_date)
                st.session_state.search_params = {"origin": origin, "destination": destination, "date": travel_date}

    if "search_results" in st.session_state:
        st.subheader(f"Available Flights • {st.session_state.search_params['origin']} → {st.session_state.search_params['destination']}")
        
        for flight in st.session_state.search_results:
            style = get_airline_style(flight['airline'])
            with st.container(border=True):
                col1, col2, col3, col4 = st.columns([3.2, 2.2, 2, 2.6])
                with col1:
                    st.markdown(f"**{flight['airline']}**  \n`{flight['flight_number']}`")
                with col2:
                    st.markdown(f"**{flight['departure']}** → **{flight['arrival']}**  \n{flight['duration']}")
                with col3:
                    st.markdown(f"**${flight['price']:,}**  \n{flight['class']}")
                    st.caption(f"{flight['seats_left']} seats left")
                with col4:
                    if st.button("Book this Flight", key=flight['id'], use_container_width=True):
                        st.session_state.current_booking = flight.copy()
                        st.session_state.current_booking.update(st.session_state.search_params)
                        st.rerun()

# ==================== BOOKING ====================
if st.session_state.current_booking:
    st.divider()
    flight = st.session_state.current_booking
    style = get_airline_style(flight['airline'])
    
    st.header("Complete Your Booking")
    st.subheader(f"{flight['airline']} • {flight['flight_number']}")
    st.write(f"**{flight['origin']}** → **{flight['destination']}** on {flight['date']}")

    st.markdown("### Select Add-ons")
    col1, col2 = st.columns(2)
    with col1:
        seat = st.selectbox("Seat Preference", ["Window", "Aisle", "No Preference"])
        baggage = st.checkbox(f"Extra Baggage 23kg (+$89)")
        meal = st.selectbox("Special Meal", ["Standard", "Vegetarian", "Halal", "Kosher", "Gluten-Free"])
    with col2:
        priority = st.checkbox("Priority Boarding (+$49)")
        insurance = st.checkbox("Travel Insurance (+$35 per person)", value=True)

    st.markdown("### Passenger Information")
    name = st.text_input("Full Name (as on passport)", value="Troy Adebayo")
    email = st.text_input("Email Address", value="troy@example.com")
    phone = st.text_input("Phone Number", value="+234 803 555 0123")

    if st.button("✅ Confirm Booking & Generate Ticket", type="primary", use_container_width=True):
        total = flight['price']
        if baggage: total += 89
        if priority: total += 49
        if insurance: total += 35 * 1

        booking = {
            "booking_id": f"GW{random.randint(100000, 999999)}",
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
        st.success("🎉 Booking Confirmed! Your airline-branded ticket is ready.")
        st.balloons()
        st.rerun()

# ==================== TAB 2: MY TICKETS ====================
with tab2:
    st.header("My Tickets")
    
    if not st.session_state.bookings:
        st.info("You have no tickets yet. Book your first flight in the Search tab.")
    else:
        for booking in st.session_state.bookings:
            style = get_airline_style(booking['flight']['airline'])
            
            with st.expander(f"✈️ {booking['flight']['airline']} • {booking['flight']['origin']} → {booking['flight']['destination']} • {booking['pnr']}", expanded=True):
                
                # === CLEAN TICKET PREVIEW ===
                st.subheader("🎫 E-Ticket Preview")
                
                with st.container(border=True):
                    # Airline header
                    st.markdown(f"""
                    <div style="background-color: #0f172a; color: white; padding: 12px 20px; border-radius: 8px 8px 0 0; margin-bottom: 0;">
                        <h3 style="margin:0; color: white;">{booking['flight']['airline']}</h3>
                        <p style="margin:0; color: #94a3b8; font-size: 0.9em;">{style['tagline']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Main ticket content
                    st.markdown(f"""
                    <div style="border: 2px solid #0f172a; border-top: none; border-radius: 0 0 8px 8px; padding: 20px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                            <div>
                                <span style="background-color: #22c55e; color: white; padding: 4px 14px; border-radius: 20px; font-size: 0.85em; font-weight: 600;">CONFIRMED</span>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 0.85em; color: #64748b;">PNR</div>
                                <div style="font-weight: 700; font-size: 1.1em;">{booking['pnr']}</div>
                            </div>
                        </div>
                        
                        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin-bottom: 20px;">
                            <div>
                                <div style="font-size: 0.8em; color: #64748b;">FROM</div>
                                <div style="font-weight: 700; font-size: 1.15em;">{booking['flight']['origin']}</div>
                                <div>{booking['flight']['departure']}</div>
                            </div>
                            <div style="text-align: center;">
                                <div style="font-size: 0.8em; color: #64748b;">FLIGHT</div>
                                <div style="font-weight: 700;">{booking['flight']['flight_number']}</div>
                                <div style="font-size: 0.9em;">{booking['flight']['duration']}</div>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 0.8em; color: #64748b;">TO</div>
                                <div style="font-weight: 700; font-size: 1.15em;">{booking['flight']['destination']}</div>
                                <div>{booking['flight']['arrival']}</div>
                            </div>
                        </div>
                        
                        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 10px; border-top: 1px solid #e2e8f0; padding-top: 15px;">
                            <div>
                                <div style="font-size: 0.75em; color: #64748b;">PASSENGER</div>
                                <div style="font-weight: 600;">{booking['passenger']['name']}</div>
                            </div>
                            <div>
                                <div style="font-size: 0.75em; color: #64748b;">CLASS</div>
                                <div style="font-weight: 600;">{booking['flight']['class']}</div>
                            </div>
                            <div>
                                <div style="font-size: 0.75em; color: #64748b;">SEAT</div>
                                <div style="font-weight: 600;">{booking['add_ons']['seat']}</div>
                            </div>
                            <div>
                                <div style="font-size: 0.75em; color: #64748b;">DATE</div>
                                <div style="font-weight: 600;">{booking['flight']['date']}</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # Download realistic PDF
                if st.button(f"📥 Download {booking['flight']['airline']} Style Ticket (PDF)", key=f"pdf_{booking['pnr']}"):
                    buffer = io.BytesIO()
                    c = canvas.Canvas(buffer, pagesize=A4)
                    style = get_airline_style(booking['flight']['airline'])
                    
                    # Airline header bar
                    c.setFillColor(style['primary'])
                    c.rect(0, A4[1]-85, A4[0], 85, fill=True, stroke=False)
                    
                    c.setFillColor(white)
                    c.setFont("Helvetica-Bold", 22)
                    c.drawString(35, A4[1]-45, booking['flight']['airline'])
                    c.setFont("Helvetica", 10)
                    c.drawString(35, A4[1]-62, style['tagline'])
                    
                    # Title
                    c.setFillColor(black)
                    c.setFont("Helvetica-Bold", 13)
                    c.drawString(35, A4[1]-110, "E-TICKET / BOARDING PASS")
                    
                    # Main details
                    c.setFont("Helvetica", 10)
                    y = A4[1] - 140
                    
                    details = [
                        f"Booking Reference (PNR): {booking['pnr']}",
                        f"Passenger Name: {booking['passenger']['name']}",
                        f"Flight: {booking['flight']['airline']} {booking['flight']['flight_number']}",
                        f"Route: {booking['flight']['origin']}  →  {booking['flight']['destination']}",
                        f"Date: {booking['flight']['date']}     Departure: {booking['flight']['departure']} - {booking['flight']['arrival']}",
                        f"Class: {booking['flight']['class']}     Seat: {booking['add_ons']['seat']}",
                        f"Status: CONFIRMED"
                    ]
                    
                    for line in details:
                        c.drawString(35, y, line)
                        y -= 17
                    
                    # Barcode simulation
                    c.setStrokeColor(HexColor("#333333"))
                    c.setLineWidth(0.8)
                    barcode_y = 120
                    for i in range(60):
                        if random.random() > 0.5:
                            c.line(35 + i*4, barcode_y, 35 + i*4, barcode_y + 35)
                    
                    c.setFont("Helvetica", 8)
                    c.drawCentredString(A4[0]/2, barcode_y - 15, booking['pnr'])
                    
                    # Footer
                    c.setFont("Helvetica-Oblique", 9)
                    c.drawString(35, 55, f"Thank you for flying with {booking['flight']['airline']}. Safe travels!")
                    
                    c.save()
                    buffer.seek(0)
                    
                    st.download_button(
                        label="Download Airline-Branded Ticket",
                        data=buffer,
                        file_name=f"{booking['flight']['airline'].replace(' ', '')}_Ticket_{booking['pnr']}.pdf",
                        mime="application/pdf"
                    )

# ==================== TAB 3: RECEIPTS ====================
with tab3:
    st.header("Receipts")
    if not st.session_state.bookings:
        st.info("No receipts yet.")
    else:
        for booking in st.session_state.bookings:
            with st.container(border=True):
                st.write(f"**Receipt #{booking['booking_id']}**")
                st.write(f"Passenger: {booking['passenger']['name']}")
                st.write(f"Total: **${booking['total_price']:,}**")
                
                if st.button(f"Download Receipt PDF", key=f"rcpt_{booking['pnr']}"):
                    buffer = io.BytesIO()
                    c = canvas.Canvas(buffer, pagesize=A4)
                    c.setFont("Helvetica-Bold", 16)
                    c.drawString(40, A4[1]-55, "GlobalWings - Official Receipt")
                    c.setFont("Helvetica", 10)
                    y = A4[1]-85
                    for line in [
                        f"Receipt No: {booking['booking_id']}",
                        f"Issued: {booking['date']}",
                        f"Passenger: {booking['passenger']['name']}",
                        f"Flight: {booking['flight']['airline']} {booking['flight']['flight_number']}",
                        f"Base Fare: ${booking['flight']['price']:,}",
                        f"Add-ons: ${booking['total_price'] - booking['flight']['price']:,}",
                        f"TOTAL PAID: ${booking['total_price']:,}"
                    ]:
                        c.drawString(40, y, line)
                        y -= 16
                    c.setFont("Helvetica-Oblique", 8)
                    c.drawString(40, 50, "This is a computer-generated receipt. Thank you for choosing GlobalWings.")
                    c.save()
                    buffer.seek(0)
                    st.download_button("Download Receipt", buffer, file_name=f"Receipt_{booking['pnr']}.pdf")

st.markdown("---")
st.caption("GlobalWings — Book any airline in the world. This is a demo with realistic sample data.")