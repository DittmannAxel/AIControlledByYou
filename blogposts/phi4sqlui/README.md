Repository Title: “Phi-4 SLM and Keep Your Data Local”

Introduction:
This repository complements a blog post discussing how to leverage a local environment and tools—such as a SLM endpoint for this case Phi-4, a database, and custom chart rendering—to keep sensitive data local and secure. The code demonstrates how to query a database with AI-generated SQL, visualize dynamic factory-floor sensor data, and incrementally update a live chart without expsoing your data to external sources - suitable for Defense, National Security. As I tested the new Phi-4 I used a cloud based hosting, because it was more suitable, but: an SLM can also be executed local. Again, by using a local environment, you maintain full control over your data and operations.

Files Overview:

1.	data_generator.py
Description:
Continuously inserts simulated factory sensor data (e.g., motor RPM, temperature, humidity) into a local PostgreSQL database. This script produces a steady stream of random values and timestamps, providing a data source for testing and visualizing live updates.

2.	create_table.py 
Description:
Initializes the sensor_data table within the PostgreSQL database, ensuring the necessary schema exists before data insertion begins. It’s a simple setup step to prepare the environment.

3.	llm_query.py
Description:
Communicates with the local LLM endpoint to transform a user’s natural language request into a valid SQL statement. It cleans and extracts only the SQL string from the model’s response, ensuring no extra formatting. By querying the schema, it can map terms like “rpm” to actual database fields (e.g., motor_rpm).

4.	db_schema.py
Description:
Fetches and returns the schema information from the local PostgreSQL database. The code retrieves all tables and their columns, providing context to the LLM so it can generate more accurate SQL queries based on available columns.

5.	app.py
Description:
A Flask-based web server that:
	•	Provides /init_query for translating user queries into SQL via the LLM.
	•	Offers /run_query to execute the generated SQL and return the latest data.
	•	Serves the frontend index.html page.
This file ties together the database, LLM-generated queries, and the frontend visualization.
	
6.	index.html
Description:
The frontend page that lets you:
	•	Enter a user query and initialize the SQL via /init_query.
	•	Periodically fetch new data from /run_query.
	•	Display dynamic data on a chart that updates over time.
It includes input fields, buttons, and a canvas for rendering a custom chart, as well as textareas to show the generated SQL and the returned JSON data.

7.	static/js/chart.js, chartjs-adapter-date-fns.js (if hosted locally)
Description:
If previously used, these would be Chart.js and adapter libraries hosted locally. However, if replaced by a custom script, these may not be present. If they are, they provide time-based charting capabilities without external CDNs.

Overall, this repository serves as a standalone demonstration of how to keep your operations local—querying locally, visualizing locally, and relying on a local LLM model. It ensures data privacy and control, fitting nicely as a supplemental resource for the related blog post.

1. env_example.txt
   Descritpion:
   Fill in your values and rename it to .env -> to store your secrets

2. requirenments.txt
    Descritpion:
    use pip install -r requirements.txt
