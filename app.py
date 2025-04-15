"""
app.py
------
Final Car Advisor Project with Enhanced Comparison:
- Car Recommendation Tab: Uses static data from cars_module.py.
- Dynamic Car Search Tab: Uses CarQuery (Optional).
- Comparison Tab: Uses the Vehicle Databases API exclusively for models & trims:
  1) The user selects a make (from makes_list).
  2) We call the Vehicle Databases API to fetch all models for that make & year.
  3) We let the user pick one from the dropdown.
  4) We call the Vehicle Databases trim endpoint to fetch all trims for that chosen model.
  5) The user picks a trim, and we call the specs endpoint to retrieve data for comparison.
- Only vehicles with non-empty fuel_economy & horsepower data go into the final graph.
"""

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import cars_module as cm  # Used for static car recommendations
import urllib.parse

# Import API key from config.py (make sure config.py is in your .gitignore)
from config import VEHICLE_HISTORY_API_KEY

# ---------------------------
# API Endpoints
# ---------------------------
VEHICLE_BASE_URL = "https://api.vehicledatabases.com"
VEHICLE_SPECS_ENDPOINT = f"{VEHICLE_BASE_URL}/ymm-specs"
VEHICLE_OPTIONS_ENDPOINT = f"{VEHICLE_SPECS_ENDPOINT}/options/v2"

# ---------------------------
# Makes List (following your provided JSON formatting)
# ---------------------------
makes_list = [
    "Acura", "Audi", "BMW", "Buick", "Cadillac", "Chevrolet", "Chrysler",
    "Dodge", "Fiat", "Ford", "GMC", "Genesis", "Honda", "Hyundai", "Infiniti",
    "Jaguar", "Jeep", "KIA", "Land Rover", "Lexus", "Lincoln", "Mazda", "Mini",
    "Mercedes-Benz", "Mitsubishi", "Nissan", "Porsche", "RAM", "Smart", "Subaru",
    "Toyota", "Volkswagen", "Volvo"
]

# ---------------------------
# Custom CSS for Unique UI
# ---------------------------
st.markdown("""
<style>
body {
    background-color: #f9f9f9;
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
}
h1, h2, h3 {
    color: #333;
    text-align: center;
}
div.stButton > button {
    background-color: #007ACC;
    color: white;
    border: none;
    padding: 8px 16px;
    font-size: 16px;
    border-radius: 4px;
    transition: background-color 0.3s ease;
}
div.stButton > button:hover {
    background-color: #005f99;
}
.success-box {
    background-color: #d4edda;
    border: 1px solid #c3e6cb;
    border-radius: 5px;
    padding: 10px;
    margin: 10px 0;
    color: #155724;
    text-align: center;
}
.center-image {
    text-align: center;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Vehicle Databases Helper Functions
# ---------------------------

def get_vehicle_db_models(make: str, year: int) -> list[str]:
    """
    Calls an endpoint (hypothetical) that returns a list of models for the specified make & year.
    For example, if the real endpoint is:
    GET /ymm-specs/options/v2/model/{year}/{make}
    Then we parse the returned JSON for 'models' -> a list of model names.
    """
    make_lower = make.lower()
    url = f"{VEHICLE_OPTIONS_ENDPOINT}/model/{year}/{make_lower}"
    headers = {"x-AuthKey": VEHICLE_HISTORY_API_KEY}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        st.write("Vehicle DB Models response:", data)  # Debug
        # Suppose data = {"status":"success","data":{"models":[{"model_name":"XTS"},...]}}
        # We'll parse out the model_name.
        model_objects = data.get("data", {}).get("models", [])
        model_list = [m.get("model_name", "").strip() for m in model_objects if m.get("model_name")]
        model_list = list({m for m in model_list if m})  # remove duplicates, empty
        return sorted(model_list)
    else:
        st.error(f"Error retrieving Vehicle DB models. Code: {resp.status_code}")
        return []

def get_vehicle_trim_options(year: int, make: str, model: str) -> list[str]:
    """
    Calls: GET https://api.vehicledatabases.com/ymm-specs/options/v2/trim/{year}/{make}/{model}
    to get a list of trims. If no trims are found, fallback to [model].
    """
    make_lower = make.lower()
    model_encoded = urllib.parse.quote(model)
    url = f"{VEHICLE_OPTIONS_ENDPOINT}/trim/{year}/{make_lower}/{model_encoded}"
    headers = {"x-AuthKey": VEHICLE_HISTORY_API_KEY}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        st.write("Trim Options API Response:", data)  # Debug
        if data.get("status", "").lower() == "success":
            trims = data.get("trims") or data.get("data", {}).get("trims", [])
            if not trims:
                return [model]  # fallback
            return trims
        else:
            return [model]
    else:
        st.error(f"Error retrieving trim options. Code: {resp.status_code}")
        return [model]

def get_vehicle_history_specs(year: int, make: str, model: str, trim: str = "") -> dict:
    """
    Fetch final specs (fuel economy, horsepower, etc.).
    GET /ymm-specs/{year}/{make}/{model}/{trim}
    """
    model_encoded = urllib.parse.quote(model)
    trim_encoded = urllib.parse.quote(trim) if trim else "base"
    url = f"{VEHICLE_SPECS_ENDPOINT}/{year}/{make.lower()}/{model_encoded}/{trim_encoded}"
    headers = {"x-AuthKey": VEHICLE_HISTORY_API_KEY}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        if data.get("status", "").lower() == "success":
            return data.get("data", {})
    return {}

def parse_fuel_economy(fuel_str: str) -> float:
    """Given a string like '24 City / 32 Hwy', compute average."""
    try:
        parts = fuel_str.split('/')
        if len(parts) == 2:
            city = float(parts[0].strip().split()[0])
            hwy = float(parts[1].strip().split()[0])
            return (city + hwy) / 2
    except:
        pass
    return None

def parse_horsepower(hp_str: str) -> float:
    try:
        # e.g. "200 hp @ 6000 rpm" -> "200"
        return float(hp_str.split()[0])
    except:
        pass
    return None

# ---------------------------
# Car Recommendation (Static)
# ---------------------------
def car_recommendation_tab():
    st.markdown("<h2>Car Recommendation</h2>", unsafe_allow_html=True)
    with st.form("car_recommendation_form"):
        budget = st.number_input("Budget (USD)", min_value=10000, max_value=500000, value=50000, step=5000)
        usage = st.selectbox("Type of Car", ["commuter", "performance"])
        country = st.selectbox("Country of Origin", ["usa", "germany", "japan", "italy"])
        seats = st.slider("Number of Seats", min_value=2, max_value=7, value=5)
        submitted = st.form_submit_button("Enter")

    if st.button("Reset Form"):
        st.experimental_rerun()

    if submitted:
        recommended = cm.recommend_cars(budget, usage, country, seats, limit=2)
        st.markdown("<h3>Recommendation(s)</h3>", unsafe_allow_html=True)
        if not recommended:
            st.error("No suitable car found for these preferences.")
        else:
            for car_name in recommended:
                success_centered(f"A good option for you might be the <b>{car_name}</b>!")
                car_data = next((c for c in cm.CARS_DB if c["name"] == car_name), None)
                if car_data and "image_path" in car_data:
                    display_centered_image(car_data["image_path"], car_name)

# ---------------------------
# Dynamic Car Search (Optional usage of CarQuery)
# ---------------------------
def dynamic_search_tab():
    st.markdown("<h2>Dynamic Car Search</h2>", unsafe_allow_html=True)
    st.markdown("<p>(Optional) Use CarQuery to see basic model info. This is separate from the final Comparison tool.</p>", unsafe_allow_html=True)
    
    selected_make = st.selectbox("Car Make", options=makes_list, index=0)
    year = st.number_input("Year", min_value=1990, max_value=2023, value=2020, step=1)

    # If you prefer not to use CarQuery at all, comment out or remove the lines below:
    if st.button("Search Models via CarQuery"):
        # We do only a simple 'getCarQueryModels' call
        # purely for demonstration or debugging
        pass
    st.info("CarQuery usage is optional. The final Comparison tab uses Vehicle Databases only.")

# ---------------------------
# Comparison Tab (Fully Vehicle Databases)
# ---------------------------
def comparison_tab():
    st.markdown("<h2>Comparison (Vehicle Databases Only)</h2>", unsafe_allow_html=True)
    st.markdown("""
    <p>For each model you want to compare:
    1) Choose the Make (dropdown).
    2) Enter the Year.
    3) We'll fetch models from Vehicle Databases, and you pick one from the dropdown.
    4) We'll fetch trims from Vehicle Databases for that chosen model.
    5) We'll call the specs endpoint to get Average MPG & Horsepower for your graph.</p>
    """, unsafe_allow_html=True)

    def single_model_input(label: str):
        st.markdown(f"### {label}")
        make_val = st.selectbox(f"Make for {label}", options=makes_list, key=f"cmp_make_{label}")
        year_val = st.number_input(f"Year for {label}", min_value=1990, max_value=2023, value=2020, step=1, key=f"cmp_year_{label}")

        # Step 1: get models from vehicle DB
        model_list = get_vehicle_db_models(make_val, year_val)
        chosen_model = st.selectbox(
            f"Model for {label}",
            options=model_list if model_list else ["(No models found)"],
            key=f"cmp_model_{label}"
        )

        # Step 2: get trims from vehicle DB
        trim_list = ["(No model selected)"]
        if chosen_model and chosen_model != "(No models found)":
            trim_list = get_vehicle_trim_options(year_val, make_val, chosen_model)
        chosen_trim = st.selectbox(
            f"Trim for {label}",
            options=trim_list if trim_list else ["base"],
            key=f"cmp_trim_{label}"
        )
        return {"make": make_val, "year": year_val, "model": chosen_model, "trim": chosen_trim}

    # We allow up to 4 models
    model1 = single_model_input("Model 1")
    model2 = single_model_input("Model 2")
    model3 = single_model_input("Model 3 (Optional)")
    model4 = single_model_input("Model 4 (Optional)")  # Fixed indentation

    if st.button("Compare Models"):
        # Collect only valid entries
        entries = []
        for info in [model1, model2, model3, model4]:
            if info["make"] and info["model"] and info["model"] != "(No models found)" and info["model"] != "":
                entries.append(info)
        if len(entries) < 2:
            st.error("Please enter details for at least two valid models to compare.")
            return

        # Now fetch data from the specs
        data_list = []
        for ent in entries:
            make_api = ent["make"].lower()
            year_api = ent["year"]
            mod_api = ent["model"]
            trim_api = ent["trim"] if ent["trim"] != "(No model selected)" else "base"

            # Get specs
            specs_data = get_vehicle_history_specs(year_api, make_api, mod_api, trim_api)
            # parse
            fuel_str = specs_data.get("fuel", {}).get("fuel_economy", None)
            avg_mpg = parse_fuel_economy(fuel_str) if fuel_str else None
            hp_str = specs_data.get("engine", {}).get("horsepower", None)
            horsepower = parse_horsepower(hp_str) if hp_str else None

            if avg_mpg is not None and horsepower is not None:
                label = f"{ent['make']} {ent['model']} ({ent['year']}) - {ent['trim']}"
                data_list.append({
                    "Car": label,
                    "Avg MPG": avg_mpg,
                    "Engine HP": horsepower
                })

        if len(data_list) < 2:
            st.error("Not enough models with complete data to compare. Please try other models.")
            return

        # Build graphs
        df = pd.DataFrame(data_list)
        st.markdown("<h3 style='text-align:center;'>Average MPG</h3>", unsafe_allow_html=True)
        fig_mpg = px.bar(df, x="Car", y="Avg MPG", title="Average MPG Comparison", labels={"Avg MPG": "Average MPG"})
        st.plotly_chart(fig_mpg, use_container_width=True)

        st.markdown("<h3 style='text-align:center;'>Engine Horsepower</h3>", unsafe_allow_html=True)
        fig_hp = px.bar(df, x="Car", y="Engine HP", title="Engine HP Comparison", labels={"Engine HP": "Horsepower"})
        st.plotly_chart(fig_hp, use_container_width=True)

        # Build graphs
        df = pd.DataFrame(data_list)
        st.markdown("<h3 style='text-align:center;'>Average MPG</h3>", unsafe_allow_html=True)
        fig_mpg = px.bar(df, x="Car", y="Avg MPG", title="Average MPG Comparison", labels={"Avg MPG": "Average MPG"})
        st.plotly_chart(fig_mpg, use_container_width=True)

        st.markdown("<h3 style='text-align:center;'>Engine Horsepower</h3>", unsafe_allow_html=True)
        fig_hp = px.bar(df, x="Car", y="Engine HP", title="Engine HP Comparison", labels={"Engine HP": "Horsepower"})
        st.plotly_chart(fig_hp, use_container_width=True)

# ---------------------------
# Main App
# ---------------------------
def main():
    st.markdown("<h1 style='text-align: center;'>Car Advisor Project</h1>", unsafe_allow_html=True)
    st.markdown("""
    <p style='text-align:center;'>
    - Car Recommendation (static data) <br/>
    - Dynamic Car Search (CarQuery - optional) <br/>
    - Comparison (Vehicle Databases only!)
    </p>
    """, unsafe_allow_html=True)

    tab_list = ["Car Recommendation", "Dynamic Car Search", "Comparison"]
    tabs = st.tabs(tab_list)

    with tabs[0]:
        car_recommendation_tab()
    with tabs[1]:
        dynamic_search_tab()
    with tabs[2]:
        comparison_tab()

if __name__ == "__main__":
    main()
