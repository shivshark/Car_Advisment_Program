"""
app.py
------
A Streamlit application that:
1) Uses a form & 'Enter' button to display recommendations only after submission.
2) Allows up to two recommendations with images.
3) Has a 'Reset Form' button that sets session state to default (refresh/re-run needed).
"""

import streamlit as st
import cars_module as cm

def find_car_data(car_name: str):
    """Helper function to get the full dictionary for a given car name."""
    for c in cm.CARS_DB:
        if c["name"] == car_name:
            return c
    return None

def reset_defaults():
    """
    Reset session state values to default.
    The user must manually refresh or re-run the app to see these new defaults.
    """
    st.session_state["user_budget"] = 50000
    st.session_state["user_usage"] = "commuter"
    st.session_state["user_country"] = "usa"
    st.session_state["user_seats"] = 5

def main():
    st.title("Car Advisor")
    st.write("Use the sidebar form to enter your preferences, then click 'Enter' to see your recommendations.")

    # ----- SESSION DEFAULTS -----
    if "user_budget" not in st.session_state:
        st.session_state["user_budget"] = 50000
    if "user_usage" not in st.session_state:
        st.session_state["user_usage"] = "commuter"
    if "user_country" not in st.session_state:
        st.session_state["user_country"] = "usa"
    if "user_seats" not in st.session_state:
        st.session_state["user_seats"] = 5

    # ----- SIDEBAR FORM -----
    st.sidebar.header("Car Preferences")

    with st.sidebar.form("car_form"):
        st.session_state["user_budget"] = st.number_input(
            "Budget (USD)",
            min_value=10000,
            max_value=500000,
            value=st.session_state["user_budget"],
            step=5000
        )

        usage_options = ["commuter", "performance"]
        if st.session_state["user_usage"] not in usage_options:
            st.session_state["user_usage"] = "commuter"
        st.session_state["user_usage"] = st.selectbox(
            "Type of Car",
            usage_options,
            index=usage_options.index(st.session_state["user_usage"])
        )

        country_options = ["usa", "germany", "japan", "italy"]
        if st.session_state["user_country"] not in country_options:
            st.session_state["user_country"] = "usa"
        st.session_state["user_country"] = st.selectbox(
            "Country of Origin",
            country_options,
            index=country_options.index(st.session_state["user_country"])
        )

        st.session_state["user_seats"] = st.slider(
            "Number of Seats",
            min_value=2,
            max_value=7,
            value=st.session_state["user_seats"]
        )

        # The user must click this to submit the form
        submitted = st.form_submit_button("Enter")

    # ----- RESET BUTTON -----
    if st.sidebar.button("Reset Form"):
        reset_defaults()
        st.info("Form reset to defaults. Please refresh or rerun the app to see changes.")

    # ----- SHOW RECOMMENDATIONS IF SUBMITTED -----
    if submitted:
        recommended_cars = cm.recommend_cars(
            budget=st.session_state["user_budget"],
            usage=st.session_state["user_usage"],
            country=st.session_state["user_country"],
            seats=st.session_state["user_seats"],
            limit=2
        )

        st.subheader("Recommendation(s)")
        if not recommended_cars:
            st.error("No suitable car found for these preferences.")
        else:
            # Always display the first recommendation
            st.success(f"A good option for you might be the **{recommended_cars[0]}**!")
            car_data = find_car_data(recommended_cars[0])
            if car_data and "image_path" in car_data:
                st.image(car_data["image_path"], width=450, caption=recommended_cars[0])

            # If there's a second recommended car, show it too
            if len(recommended_cars) > 1:
                st.success(f"Another great choice might be the **{recommended_cars[1]}**!")
                car_data2 = find_car_data(recommended_cars[1])
                if car_data2 and "image_path" in car_data2:
                    st.image(car_data2["image_path"], width=450, caption=recommended_cars[1])

if __name__ == "__main__":
    main()
