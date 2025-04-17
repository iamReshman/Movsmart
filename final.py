import streamlit as st
import folium
from streamlit_folium import st_folium
import json
import os  # to check file existence
import time

st.set_page_config(layout="wide")
DATA_FILE = './bus_data.json'  # Default path for JSON file

st.title("🚌 Movsmart - Live Bus Tracker")

def load_data():
    if not os.path.exists(DATA_FILE):
        # Create default data if the file doesn't exist
        default_data = {
            "latitude": 37.7749,
            "longitude": -122.4194,
            "seats": [False, True, False]
        }
        with open(DATA_FILE, 'w') as f:
            json.dump(default_data, f)
        return default_data
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return {"latitude": 0, "longitude": 0, "seats": [False, False, False]}

# Sidebar inputs for pickup/destination
with st.sidebar:
    st.header("📍 Route Selector")
    pickup = st.text_input("Enter Pickup Location")
    destination = st.text_input("Enter Destination")
    run_button = st.button("Run Route")

# Data load and session state
data = load_data()

# Display map
m = folium.Map(location=[data['latitude'], data['longitude']], zoom_start=17)
folium.Marker(
    [data['latitude'], data['longitude']],
    tooltip="Bus Location",
    icon=folium.Icon(color='blue', icon='info-sign')
).add_to(m)
folium.CircleMarker(
    location=[data['latitude'], data['longitude']],
    radius=50,
    color='blue',
    fill=True,
    fill_color='blue',
    fill_opacity=0.3,
    popup=f"Bus Location\nLat: {data['latitude']}\nLon: {data['longitude']}"
).add_to(m)

# Display map
st_folium(m, width=700, height=500)

# Handle route run button
if run_button:
    st.success(f"🛣️ Route set from **{pickup}** to **{destination}**")

# Display seat occupancy
st.subheader("🪑 Seat Occupancy")
cols = st.columns(len(data["seats"]))
for idx, status in enumerate(data["seats"]):
    color = "green" if not status else "red"
    label = "Vacant" if not status else "Occupied"
    icon = "✅" if not status else "❌"
    cols[idx].markdown(
        f"### Seat {idx + 1} {icon}\n- **Status:** <span style='color:{color}'>{label}</span>",
        unsafe_allow_html=True
    )

# Optional manual refresh button
refresh_button = st.button("Refresh")
if refresh_button:
    st.session_state.last_refresh = time.time()  # Manually trigger refresh via session_state

# Session state logic for auto-refresh (optional)
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = time.time()

# Check if 5 seconds have passed
if time.time() - st.session_state.last_refresh > 5:
    st.session_state.last_refresh = time.time()  # Update time
    st.experimental_rerun()  # Re-run the script to simulate auto-refresh



