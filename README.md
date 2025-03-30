# Car Advisor Project

Car Advisor is a Streamlit-based midterm project that helps users discover car recommendations and search for detailed trim information using dynamic data from the CarQuery API. The app also includes a Dealer Network tab that displays nearby dealerships carrying specific models.

## Features

- **Static Car Recommendation:**  
  Uses a local, static car database to recommend up to two cars based on user preferences (budget, type, country, and seat count). Recommendations include images and key details.

- **Dynamic Car Search:**  
  Leverages the CarQuery API to fetch car trim data dynamically. Users can enter a car make, year, and a partial model keyword to perform a flexible search that returns detailed trim information (body type, engine specs, transmission, top speed, etc.).

- **Dealer Network:**  
  Displays a static dealer network with information about dealerships (name, location, available models, and dealer images).

- **User-Friendly UI:**  
  The app uses form-based inputs, centered text, and custom HTML for a polished look. It’s divided into three tabs for easy navigation.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-username/Car_Advisor.git
   cd Car_Advisor

	2.	Install Dependencies:
Ensure you have Python 3.7+ installed. Then, install the required packages:

pip install streamlit requests


	3.	Project Folder Structure:

Car_Advisor/
├── app.py
├── cars_module.py
└── images/
    ├── ford_explorer.jpg
    ├── bmw_m4.jpg
    ├── honda_civic.jpg
    ├── corvette.jpg
    ├── porsche_911.jpg
    ├── toyota_camry.jpg
    ├── honda_odyssey.jpg
    ├── chevy_suburban.jpg
    ├── tesla_modelx.jpg
    ├── audi_r8.jpg
    ├── lamborghini_huracan.jpg
    ├── ferrari_488.jpg
    ├── maserati_quattroporte.jpg
    ├── nissan_gtr.jpg
    ├── toyota_highlander.jpg
    ├── dodge_charger.jpg
    ├── dealer1.jpg
    ├── dealer2.jpg
    └── dealer3.jpg

Note: Make sure the image filenames exactly match those referenced in the code.

Running the App
	1.	Set Up Environment Variables (Optional):
If you need to use an API key for any dynamic API calls (like Edmunds, if available), set it as an environment variable. For example, on Unix-based systems:

export EDMUNDS_API_KEY="your_api_key_here"

(This project uses the CarQuery API which is free for basic usage and does not require an API key.)

	2.	Run the Application:
In your terminal, execute:

streamlit run app.py


	3.	Usage:
	•	Car Recommendation Tab: Enter your car preferences and click Enter to view static recommendations.
	•	Dynamic Car Search Tab: Enter a car make, year, and model keyword (e.g., “750i” or “3 series”) and click Search to fetch detailed trim information from the CarQuery API.
	•	Dealer Network Tab: Enter a car model (and optionally a location) to see which dealers (from a static dataset) carry the model you’re interested in.

Future Enhancements
	•	API Integration:
Replace or supplement the static dealer data with a dynamic API if available.
	•	Enhanced UI/UX:
Refine the design with custom CSS or additional Streamlit components.
	•	Additional Filters:
Extend the search functionality to include more filters (e.g., fuel type, horsepower, color).

License

This project is provided under the MIT License.

⸻

Enjoy exploring your next car with the Car Advisor Project!

---
