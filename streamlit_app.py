

 
import streamlit as st
import json
import os

# Streamlit page setup
st.set_page_config(layout="wide")
st.title("🚌 Movsmart – Live Bus Seat Availability")

# Load data
DATA_FILE = "bus_data.json"

def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except:
        # Default dummy data for 50 seats
        return {
            "latitude": 12.9716,
            "longitude": 77.5946,
            "seats": [False] * 50
        }

data = load_data()
seats = data["seats"]

# Count stats
total_seats = len(seats)
occupied_count = sum(seats)
vacant_count = total_seats - occupied_count

# Dashboard summary
st.markdown(f"### 🧾 Total Seats: `{total_seats}`")
st.markdown(f"### ✅ Vacant: `{vacant_count}` | ❌ Occupied: `{occupied_count}`")
st.markdown("---")

# URLs for seat images (replace with your own hosted images if needed)
occupied_img = "https://i.imgur.com/5J1y8bk.png"  # red seat
vacant_img = "https://i.imgur.com/y9v3R8D.png"    # green seat

# Show seat status with images
st.subheader("🪑 Seat Map")

# Arrange in 5 columns
cols = st.columns(5)

for i, status in enumerate(seats):
    with cols[i % 5]:
        img_url = occupied_img if status else vacant_img
        label = f"Seat {i+1}\n{'Occupied ❌' if status else 'Vacant ✅'}"
        st.image(img_url, caption=label, use_column_width=True)




