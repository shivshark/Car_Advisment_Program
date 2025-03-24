"""
app.py
------
Streamlit interface for the Car Advisor program.
Users can input their preferences and receive a recommended car.
"""

import streamlit as st
import cars_module as cm

def main():
    st.title("Car Advisor")
    st.write("Answer a few questions to get a car recommendation!")

    st.sidebar.header("User Preferences")
    
    # Get user inputs
    user_budget = st.sidebar.number_input("Budget (USD)", min_value=10000, max_value=300000, value=50000, step=1000)
    user_usage = st.sidebar.selectbox("Type of Car", ["commuter", "performance"])
    user_country = st.sidebar.selectbox("Country of Origin", ["usa", "germany", "japan"])
    user_seats = st.sidebar.slider("Number of Seats", min_value=2, max_value=7, value=5, step=1)

    # Recommend a car
    recommended_car = cm.recommend_car(
        budget=user_budget,
        usage=user_usage,
        country=user_country,
        seats=user_seats
    )
    
    st.subheader("Recommendation")
    if recommended_car:
        st.success(f"A good option for you to look at is the **{recommended_car}**!")
    else:
        st.error("Sorry, we couldn't find a car that matches your preferences.")

if __name__ == "__main__":
    main()