import streamlit as st
import folium
from shapely.geometry import Point
from st_folium import folium_static
import pandas as pd
import numpy as np

# FUNCTION TO CREATE CONCENTRIC CIRCLES
def create_circles(lat, lon, radius_list):
    circles = []
    for radius in radius_list:
        circle = folium.Circle(
            radius=radius * 1000,
            location=[lat, lon],
            color='blue',
            fill=True,
            fill_opacity=0.4
        )
        circles.append(circle)
    return circles

# FUNCTION TO GENERATE SYNTHETIC PLACE DATA
def generate_synthetic_places(lat, lon, radius_list):
    places_data = {}
    for radius in radius_list:
        num_places = np.random.randint(5, 15)  # Random number of places
        places = []
        for _ in range(num_places):
            place_lat = lat + np.random.uniform(-0.1, 0.1)
            place_lon = lon + np.random.uniform(-0.1, 0.1)
            place_name = f"Place {radius}-{_}"
            distance = np.random.uniform(0, radius)
            places.append((place_name, round(distance, 2), (place_lat, place_lon)))
        places_data[radius] = places
    return places_data

# FUNCTION TO DISPLAY PLACES
def display_places_with_style(places_data):
    for radius, places in places_data.items():
        places.sort(key=lambda x: x[1])
        st.subheader(f"Places within {radius} km radius")
        for place, distance, _ in places:
            st.write(f"- {place} ({distance} km)")

# STREAMLIT APP LAYOUT
st.title("Synthetic Geofencing Visualization")

# Sidebar for input controls
with st.sidebar:
    st.title("Input Controls")
    lat = st.number_input('Latitude', value=16.56467, format="%.5f")
    lon = st.number_input('Longitude', value=78.11582, format="%.5f")
    radius_input = st.text_input('Enter radii (in km) separated by commas', '5,15,30,50')

radius_list = [int(r.strip()) for r in radius_input.split(',')]

# Generate synthetic places data
places_data = generate_synthetic_places(lat, lon, radius_list)

# Initialize map
m = folium.Map(location=[lat, lon], zoom_start=10)

# Create and add circles to the map
circles = create_circles(lat, lon, radius_list)
for circle in circles:
    circle.add_to(m)

# Add circle markers for each place
for radius, places in places_data.items():
    for place, distance, (place_lat, place_lon) in places:
        folium.CircleMarker(
            location=[place_lat, place_lon],
            radius=3,  # Small fixed radius for the marker
            color='green',  # Fixed color for synthetic data
            fill=True,
            fill_color='green',
            fill_opacity=0.7,
            popup=f"{place} ({distance} km)"
        ).add_to(m)

# Display the map
folium_static(m)

# Display the places
display_places_with_style(places_data)

# Generate synthetic data CSV for download
df_to_export = pd.DataFrame(columns=['Place Name', 'Distance (km)', 'Latitude', 'Longitude'])
for radius, places in places_data.items():
    for place, distance, (place_lat, place_lon) in places:
        df_to_export = df_to_export.append({'Place Name': place, 'Distance (km)': distance, 'Latitude': place_lat, 'Longitude': place_lon}, ignore_index=True)

# Button to download CSV
st.download_button(
    label="Download Synthetic Data CSV",
    data=df_to_export.to_csv(index=False).encode('utf-8'),
    file_name='synthetic_geofenced_places.csv',
    mime='text/csv'
)
