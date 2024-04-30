Certainly! Here is the same content for the README in plain text format, which you can save as `README.txt`. Remember to insert your actual API key and complete the `[DATA_STRUCTURE_DESCRIPTION]` section.

```
Snow Resort Networking Project
==============================

Introduction
------------
This project aims to create a network of snow resorts with various data attributes such as snow conditions, resort size, variety of runs, and connection distances between resorts. Users can interact with this network through a command-line interface to discover the best resorts based on their preferences.

Prerequisites
-------------
Before running this project, ensure you have the following Python packages installed:
- tqdm
- requests


How to Run
----------
1. Clone the project repository to your local machine.
2. Make sure all required packages are installed using the command 'pip install -r requirements.txt'.
3. Run the main Python file using 'python main.py' in your command-line interface.
4. Follow the on-screen prompts to select a continent and other preferences.


User Interactions
-----------------

When the user runs the main program, they are presented with a series of interactions that allow them to explore and analyze different snow resorts based on various factors. The interactions proceed as follows:

1. Select Continent: 
   - The user is presented with a list of continents (Africa, Antarctica, Asia, Europe, North America, Oceania, South America).
   - The user is prompted to enter a continent from the list.

2. Set Priorities:
   - The user is asked to set priorities (between 0 and 1) for various factors that might affect their choice of snow resort. These factors include snow reliability, après-ski, resort size, variety of runs, cleanliness, and proportion of black runs.

3. Input Maximum Distance:
   - The user can specify a maximum connection distance between resorts, which is considered when generating the scores for each resort.

4. Explore Individual Resorts:
   - The user can select a number corresponding to one of the top 5 resorts to learn more about it.
   - If the user enters 'q', the program will cease displaying resort details.

5. Restart or Quit:
    - After exploring the top resorts, the user is given the option to restart the process and explore another continent or set of preferences, or to end the program.

Each interaction is designed to guide the user through the process smoothly, with input validation to ensure that the user's selections are within expected parameters. If an invalid input is given, the program prompts the user to try again with a valid option.

This interface allows the user to customize the search for their ideal snow resort experience according to their individual preferences and the current snow conditions.
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
