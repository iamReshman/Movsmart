import streamlit as st
import folium
from streamlit_folium import st_folium
import json
import os
from PIL import Image

# Set up page configuration
st.set_page_config(layout="wide")
st.title("🚌 Movsmart - Bus Tracker & Seat Management")

# File paths
DATA_FILE = os.path.join(os.path.expanduser("~"), "bus_data.json")
SEAT_IMAGES = {
    "vacant": "https://example.com/vacant_seat_image.png",  # Replace with actual image URL or local path
    "occupied": "https://example.com/occupied_seat_image.png"  # Replace with actual image URL or local path
}

# Function to load bus data
def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except:
        return {"latitude": 0, "longitude": 0, "seats": [False, False, False]}

data = load_data()

# Function to calculate occupied seats and total seats
def calculate_seat_statistics(seats):
    total_seats = len(seats)
    occupied = sum(seats)
    vacant = total_seats - occupied
    return total_seats, occupied, vacant

# Display seat count statistics
total_seats, occupied, vacant = calculate_seat_statistics(data["seats"])
st.sidebar.subheader("Seat Statistics")
st.sidebar.markdown(f"**Total Seats:** {total_seats}")
st.sidebar.markdown(f"**Occupied Seats:** {occupied}")
st.sidebar.markdown(f"**Vacant Seats:** {vacant}")

# Seat layout display (using images for a better visual representation)
st.subheader("Seat Layout")
cols = st.columns(len(data["seats"]))
for idx, status in enumerate(data["seats"]):
    seat_status = "vacant" if not status else "occupied"
    seat_image = SEAT_IMAGES[seat_status]
    cols[idx].image(seat_image, caption=f"Seat {idx + 1}", width=100)

# Display Map with Bus Location
st.subheader("🗺️ Bus Location")
m = folium.Map(location=[data['latitude'], data['longitude']], zoom_start=17)
folium.Marker([data['latitude'], data['longitude']], tooltip="Bus Location").add_to(m)
st_folium(m, width=700)

# Optional: Add a refresh button for manual data update
if st.button("Refresh"):
    data = load_data()
    st.experimental_rerun()

# Stylish text and description
st.markdown("""
    ### About this App
    **Movsmart** is a real-time bus location and seat occupancy tracking app.
    - View live bus location on the map.
    - See the current seat occupancy status with a visual layout.
    - Get detailed statistics on occupied and vacant seats.
""")

# Footer or Commercial Info
st.markdown("""
    <hr>
    <footer>
        <p style="text-align:center;">Powered by Movsmart. Contact us at info@movsmart.com</p>
    </footer>
""", unsafe_allow_html=True)

