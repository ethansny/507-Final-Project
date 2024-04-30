Snow Resort Networking Project
==============================

Introduction
------------
This project aims to create a network of snow resorts with various data attributes such as snow conditions, resort size, variety of runs, and connection distances between resorts. Users can interact with this network through a command-line interface to discover the best resorts based on their preferences.

Prerequisites
-------------
Before running this project, ensure you have the following Python packages installed:
- utility
- math
- tqdm
- requests
- json
- os
- time

Additionally, you will need an API key to access the snow data:
- Obtained from RapidAPI: [API_KEY_HERE]

How to Run
----------
1. Clone the project repository to your local machine.
2. Make sure all required packages are installed using the command 'pip install -r requirements.txt'.
3. Run the main Python file using 'python main.py' in your command-line interface.
4. Follow the on-screen prompts to select a continent and other preferences.

User Interactions
-----------------
- Users will start by selecting a continent from the provided list.
- The program will then retrieve resorts within the selected continent and gather snow data.
- Users will be asked to provide priorities for various resort attributes.
- Users can also specify a maximum connection distance to consider between resorts.
- Finally, the program calculates scores for each resort based on user inputs and displays the top resorts.
- The user can then view different resort details or view attributes about another node
Network Structure
-----------------
- Nodes: Each node represents a ski resort with attributes like snow reliability, resort size, and run variety.
- Edges: Distances calculated between every pair of resorts based on geographical coordinates (latitude and longitude).


Data Sources
------------
Resorts data is sourced from a CSV file 'resortworldwide.csv', and snow conditions are fetched using the ski-resort-forecast API.

  - resortsworldwide.csv sourced via Kaggle
	- https://www.kaggle.com/datasets/migueldefrutos/ski-resorts-world-wide
  - Current snow data is accessed using ski-resort-forecast.p.rapidapi.com
	- Data cached to reduce API called. Updates are set to occur after the data is 3 days old, this is disabled due to rate limiting

Detailed information on the origin of the data and caching strategy is available in 'DataSources.txt'
