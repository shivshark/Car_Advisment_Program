
Car Advisor Project

Welcome to the Car Advisor Project – a fun Streamlit application that helps you recommend cars, search for models, and compare vehicles side-by-side on horsepower and average MPG!

Overview

This project was built for a midterm assignment, showcasing:
	1.	Car Recommendation (using a local static database in cars_module.py).
	2.	Dynamic Search (optional CarQuery demo).
	3.	Comparison Tool (powered entirely by the Vehicle Databases API).

The star of the show is the Comparison Tab, where you can pick your dream cars by year, make, model, and trim, then see how they stack up in real-time charts.

Features
	1.	Car Recommendation (Static)
	•	Input budget, usage (commuter vs. performance), country of origin, and seating.
	•	The app returns possible matches from a local CARS_DB.
	2.	Comparison (Vehicle Databases)
	•	Fetch all models and trims from the Vehicle Databases API for each selected make/year.
	•	Compare up to four vehicles at once on horsepower and average MPG.
	•	Slick bar charts to visualize the differences (and brag about your car of choice!).
	3.	Dynamic Search (Optional)
	•	A small placeholder tab demonstrating CarQuery integration (for debugging or additional fun).
	•	Not required for the final usage if you just want the main comparison.

Getting Started
	1.	Clone or Download this repository:

git clone https://github.com/YourUsername/car-advisor.git
cd car-advisor


	2.	Install Dependencies
This project uses Python 3, Streamlit, requests, and plotly.

pip install streamlit requests plotly

(Add any other dependencies you need, e.g. pandas.)

	3.	Create a config.py for Your API Key
	•	Inside the project directory, make a config.py with:

VEHICLE_HISTORY_API_KEY = "YOUR_API_KEY"


	•	Keep this file out of version control (add it to .gitignore) so you don’t leak keys.

	4.	Run the App

streamlit run app.py

Open the displayed local URL in your browser, and you’re off!

How to Use
	1.	Car Recommendation
	•	Go to the “Car Recommendation (Static)” tab.
	•	Input budget, usage type, country, and seating.
	•	Click “Enter” for suggestions from our local CARS_DB.
	2.	Comparison Tool
	•	Head to the “Comparison” tab.
	•	Select the year, make, model, and trim (all from the Vehicle Databases API).
	•	Compare up to four cars at once!
	•	You’ll see bar charts for Average MPG and Engine Horsepower if the data is available.
	3.	Dynamic Search (Optional)
	•	A separate demonstration tab if you want to see how CarQuery might be integrated.
	•	Not essential for the main functionality—just a sandbox for exploring extra APIs.

Troubleshooting
	•	Missing Data
If a selected car has incomplete data (like no HP or MPG), it might get excluded from the charts. Try another trim or a different year.
	•	API Rate Limits (429)
We implemented caching and a single-form approach to minimize calls, but if you hit the limit, consider slowing down or upgrading your Vehicle Databases plan.
	•	Key Errors
Make sure config.py is in the same folder as app.py and that VEHICLE_HISTORY_API_KEY is spelled correctly.

Contributing

Pull requests and suggestions are welcome! If you find issues or have ideas for new features (like advanced fuzzy searching or more data points), open an issue or PR.

License

This project is for educational and demonstration purposes; no formal license is included. Feel free to adapt or expand for your own use.

⸻

Have fun exploring cars!
We hope this Car Advisor Project helps you compare dream rides and discover which set of wheels best fits your style.
