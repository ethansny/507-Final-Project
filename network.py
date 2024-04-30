import utility as utl
from data_structure import *
import math
from tqdm import tqdm
from get_snow_data import get_snow_data
import os




def main():
    network = Network()

    cache_file = "cache.json"

    try:
        # Try to open the cache file
        cache = utl.read_json(cache_file)
        file_time = os.path.getmtime(cache_file)

        # This would be production code, but if it has been more than three days
        # since the cache was last updated it take a very long time for it to run

        # if (time.time() - file_time) / (24 * 60 * 60) > 3:
        #     cache = {}


    except FileNotFoundError:
        # If the file is not found, create an empty cache
        cache = {}

    resorts = utl.read_csv_to_dicts("resortworldwide.csv")
    while True:
        nodes = []
        print("List of continents: Africa, Antarctica, Asia, Europe, North America, Oceania, South America")

        while True:
            continent = input("Enter a continent from the above list: ")
            if continent.lower().strip() in ["africa", "asia", "europe", "north america", "oceania", "south America"]:
                break
            else:
                print("Invalid continent. Please try again.")

        resorts_in_continent = [resort for resort in resorts if resort["Continent"] == continent]

        print(f"Found {len(resorts_in_continent)} resorts in {continent}. \n Getting snow data...")

        for resort in tqdm(resorts_in_continent):
            node = Node.from_resort(resort, cache=cache)
            nodes.append(node)

        utl.write_json(cache_file, cache)

        max_snow_depth = max([node.current_snow for node in nodes if node.current_snow is not None])

        print(f"\nAdding Nodes...")
        for node in tqdm(nodes):
            node.normalized_snow_depth = (node.current_snow / max_snow_depth * 5) if node.current_snow is not None else None
            network.add_node(node)

        print(f"\nConnecting resorts...")
        for node in tqdm(nodes):
            network.add_connections(node)


        factors = ["snow_reliability", "apres_ski", "resort_size", "variety_of_runs", "cleanliness", "proportion_of_black_runs"]

        priorities = []
        for factor in factors:
            priority = utl.get_priority_input(f"Enter a priority for {factor} (0-1): ")
            priorities.append((factor, priority))

        distance = utl.get_distance_input("Enter a distance in kilometers: ")

        print("\nCalculating scores...")
        for node in tqdm(network.nodes):
            node.calculate_score(priorities, distance)


        print("\nTop 5 resorts:")
        top_resorts = network.get_high_score()[-5:][::-1]  # Get the last 5 resorts and reverse the order

        for i, node in enumerate(top_resorts, start=1):
            print(f"{i}. {node.name} - Score: {node.score}")
        while True:
            resort_choice = input("\nPlease enter the number of the resort you want to learn more about, or 'q' to quit: ")

            if resort_choice.lower() == 'q':
                break

            try:
                chosen_resort = top_resorts[int(resort_choice) - 1]
                chosen_resort.describe()
            except (IndexError, ValueError):
                print("Invalid choice. Please try again.")

        restart = input("\nWould you like to restart? (y/n): ")
        if restart.lower() != 'y':
            break

if __name__ == "__main__":
    main()