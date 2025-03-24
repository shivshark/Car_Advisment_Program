# Car_Advisment_Program

Below is a simple, concise README for your GitHub repository. It covers the basics—what the project is, how to install and run it, and how the folder is structured—without extra frills.

⸻

Car Advisor

A Streamlit application that recommends up to two cars based on:
	•	Budget
	•	Type (commuter or performance)
	•	Country of Origin (USA, Germany, Japan, Italy)
	•	Number of Seats (2 to 7)

Features
	1.	Form Submission – Users must click Enter before results appear.
	2.	Reset – Revert inputs to default values (requires manual page refresh).
	3.	Images – Each car in the database has a local .jpg in images/, displayed in the app.

⸻

Installation
	1.	Clone this repository or download the ZIP.
	2.	Install Streamlit (if you haven’t already):

pip install streamlit


	3.	Verify that:
	•	app.py and cars_module.py live in the same folder.
	•	An images/ folder has matching .jpg files referenced by cars_module.py.

⸻

Usage
	1.	Open a terminal in the project folder.
	2.	Run:

streamlit run app.py


	3.	Navigate to the link shown (e.g. http://localhost:8501).
	4.	Fill out the sidebar form (budget, type, country, seats) and click Enter.
	5.	View up to two recommendations, each with an image (if available).
	6.	Optional: Click “Reset Form” to reset preferences, then refresh the page.

⸻

Folder Structure

Car_advisor/
├── app.py
├── cars_module.py
├── images/
│   ├── bmw_m4.jpg
│   ├── toyota_camry.jpg
│   └── ...
└── README.md



⸻

That’s it! You now have a straightforward Car Advisor project ready to share on GitHub.
