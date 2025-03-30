"""
app.py
------
Final Car Advisor Project:
- Uses a static car database to recommend up to two cars.
- Uses the CarQuery API for dynamic car search.
- Contains two tabs: "Car Recommendation" and "Dynamic Car Search".
- Centers titles, headings, recommendation messages, and images.
- Uses form-based input for queries.
"""

import streamlit as st
import requests
import os
import cars_module as cm

# CarQuery API base URL (no API key required)
CARQUERY_BASE_URL = "https://www.carqueryapi.com/api/0.3/"

def get_car_query_trims(make: str, year: int, model: str = "") -> list[dict]:
    """
    Fetches trim data from the CarQuery API for a given make and year.
    If a model string is provided, it filters the results by checking if the model
    string is a substring of the trim's model_name or model_trim fields.
    Returns a list of trim dictionaries.
    """
    params = {
        "cmd": "getTrims",
        "make": make,
        "year": year,
        "jsonp": 0,
    }
    # Add a User-Agent header to mimic a browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
    }
    response = requests.get(CARQUERY_BASE_URL, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        trims = data.get("Trims", [])
        if model.strip():
            model_lower = model.lower().strip()
            filtered_trims = [
                t for t in trims 
                if model_lower in t.get("model_name", "").lower() or 
                   model_lower in t.get("model_trim", "").lower()
            ]
            return filtered_trims
        else:
            return trims
    else:
        st.error(f"Error fetching data from CarQuery API: {response.status_code}")
        return []

def display_centered_image(image_path: str, caption: str, width: int = 450):
    """
    Displays an image using HTML to ensure it's centered.
    """
    st.markdown(f"""
    <div style="text-align:center; margin: 10px 0;">
      <img src="{image_path}" alt="{caption}" style="max-width:{width}px; margin:auto; display:block;" />
      <p style="font-style: italic; color: #666;">{caption}</p>
    </div>
    """, unsafe_allow_html=True)

def success_centered(message: str):
    """
    Displays a success-like message box with centered text using custom HTML.
    """
    st.markdown(f"""
    <div style="background-color:#d4edda; border:1px solid #c3e6cb; 
                border-radius:5px; padding:10px; margin:10px 0; 
                color:#155724; text-align:center;">
        {message}
    </div>
    """, unsafe_allow_html=True)

def car_recommendation_tab():
    st.markdown("<h2 style='text-align:center;'>Car Recommendation</h2>", unsafe_allow_html=True)
    with st.form("car_recommendation_form"):
        budget = st.number_input("Budget (USD)", min_value=10000, max_value=500000, value=50000, step=5000)
        usage = st.selectbox("Type of Car", ["commuter", "performance"])
        country = st.selectbox("Country of Origin", ["usa", "germany", "japan", "italy"])
        seats = st.slider("Number of Seats", min_value=2, max_value=7, value=5)
        submitted = st.form_submit_button("Enter")
    
    if st.button("Reset Form"):
        st.experimental_rerun()  # Reloads the app for reset
    
    if submitted:
        recommended = cm.recommend_cars(budget, usage, country, seats, limit=2)
        st.markdown("<h3 style='text-align:center;'>Recommendation(s)</h3>", unsafe_allow_html=True)
        if not recommended:
            st.error("No suitable car found for these preferences.")
        else:
            for car_name in recommended:
                success_centered(f"A good option for you might be the <b>{car_name}</b>!")
                car_data = next((c for c in cm.CARS_DB if c["name"] == car_name), None)
                if car_data and "image_path" in car_data:
                    display_centered_image(car_data["image_path"], car_name)

def dynamic_search_tab():
    st.markdown("<h2 style='text-align:center;'>Dynamic Car Search</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Enter the car's make, year, and optionally a model keyword to fetch car trim data from the CarQuery API.</p>", unsafe_allow_html=True)
    with st.form("dynamic_search_form"):
        make = st.text_input("Car Make (lowercase, niceName)", value="bmw")
        year = st.number_input("Year", min_value=1990, max_value=2023, value=2020, step=1)
        model = st.text_input("Car Model (optional, keyword search)", value="")
        submitted = st.form_submit_button("Search")
    
    if submitted:
        trims = get_car_query_trims(make, year, model)
        st.markdown("<h3 style='text-align:center;'>Search Results</h3>", unsafe_allow_html=True)
        if not trims:
            st.error("No results found for these criteria.")
        else:
            # Display extended details for each trim
            for trim in trims:
                st.markdown(f"**{trim.get('model_name', 'N/A')} {trim.get('model_trim', '')} ({trim.get('model_year', 'N/A')})**")
                st.markdown(f"- **Body Type:** {trim.get('model_body', 'N/A')}")
                st.markdown(f"- **Engine:** {trim.get('model_engine_cc', 'N/A')} cc {trim.get('model_engine_type', 'N/A')} with {trim.get('model_engine_cyl', 'N/A')} cylinders")
                st.markdown(f"- **Power:** {trim.get('model_engine_power_ps', 'N/A')} PS at {trim.get('model_engine_power_rpm', 'N/A')} rpm")
                st.markdown(f"- **Torque:** {trim.get('model_engine_torque_nm', 'N/A')} Nm at {trim.get('model_engine_torque_rpm', 'N/A')} rpm")
                st.markdown(f"- **Transmission:** {trim.get('model_transmission_type', 'N/A')}")
                st.markdown(f"- **Top Speed:** {trim.get('model_top_speed_kph', 'N/A')} kph")
                st.markdown(f"- **Doors:** {trim.get('model_doors', 'N/A')}, **Seats:** {trim.get('model_seats', 'N/A')}")
                st.markdown("---")

def main():
    st.markdown("<h1 style='text-align: center;'>Car Advisor Project</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>A midterm project that recommends cars (static) and performs dynamic searches using the CarQuery API.</p>", unsafe_allow_html=True)
    tabs = st.tabs(["Car Recommendation", "Dynamic Car Search"])
    with tabs[0]:
        car_recommendation_tab()
    with tabs[1]:
        dynamic_search_tab()

if __name__ == "__main__":
    main()
