import streamlit as st
import pandas as pd
import pydeck as pdk

# Page title
st.title("This page is available to all admins")

# Ensure the user is logged in with a role
if "role" in st.session_state and st.session_state.role:
    st.markdown(f"You are currently logged in with the role of {st.session_state.role}.")
else:
    st.error("You are not logged in. Please log in to access this page.")

# Load dataset
file_path = "simulated_waste_bins.csv"
try:
    chart_data = pd.read_csv(file_path)

    # Validate required columns
    if not {"location_lat", "location_lon"}.issubset(chart_data.columns):
        st.error("The dataset does not contain the required 'location_lat' and 'location_lon' columns.")
    else:
        # Pydeck visualization
        st.pydeck_chart(
            pdk.Deck(
                map_style=None,
                initial_view_state=pdk.ViewState(
                    latitude=chart_data["location_lat"].mean(),
                    longitude=chart_data["location_lon"].mean(),
                    zoom=11,
                    pitch=50,
                ),
                layers=[
                    pdk.Layer(
                        "HexagonLayer",
                        data=chart_data,
                        get_position="[location_lon, location_lat]",
                        radius=200,
                        elevation_scale=4,
                        elevation_range=[0, 1000],
                        pickable=True,
                        extruded=True,
                    ),
                    pdk.Layer(
                        "ScatterplotLayer",
                        data=chart_data,
                        get_position="[location_lon, location_lat]",
                        get_color="[200, 30, 0, 160]",
                        get_radius=200,
                    ),
                ],
            )
        )
except FileNotFoundError:
    st.error("The dataset file 'simulated_waste_bins.csv' was not found.")
except Exception as e:
    st.error(f"An error occurred while loading the dataset: {e}")
