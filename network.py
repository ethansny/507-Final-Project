import utility as utl
from data_structure import *
from tqdm import tqdm
import os

def choose_continent():
    """
    Prompts the user to choose a continent from a list of continents and returns the chosen continent.

    Returns:
        str: The chosen continent.

    """
    continents = ["africa", "antarctica", "asia", "europe", "north america", "oceania", "south america"]
    print("List of continents: " + ", ".join([continent.title() for continent in continents]))
    while True:
        continent = input("Enter a continent from the above list: ").lower().strip()
        if continent in continents:
            return continent
        else:
            print("Invalid continent. Please try again.")

def get_path_choice():
    """
    Prompts the user to choose between getting recommendations or searching for a resort by name.

    Returns:
        str: The user's choice (either '1' or '2').

    """
    while True:
        path_choice = input("\nWould you like to (1) get recommendations or (2) search for a resort by name? Enter 1 or 2: ")
        if path_choice in ['1', '2']:
            return path_choice
        else:
            print("Invalid choice. Please try again.")

def select_resort(top_resorts):
    """
    Prompts the user to select a resort from a list of top resorts.

    Args:
        top_resorts (list): A list of top resorts.

    Returns:
        chosen_resort (str): The chosen resort from the list of top resorts.
        None: If the user chooses to quit.

    Raises:
        IndexError: If the user enters an invalid resort number.
        ValueError: If the user enters an invalid input.

    """
    while True:
        resort_choice = input("\nPlease enter the number of the resort you want to learn more about, or 'q' to quit: ")
        if resort_choice.lower() == 'q':
            return None
        try:
            chosen_resort = top_resorts[int(resort_choice) - 1]
            return chosen_resort
        except (IndexError, ValueError):
            print("Invalid choice. Please try again.")

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
        continent = choose_continent()
        # print("List of continents: Africa, Antarctica, Asia, Europe, North America, Oceania, South America")

        # while True:
        #     continent = input("Enter a continent from the above list: ")
        #     if continent.lower().strip() in ["africa", "asia", "europe", "north america", "oceania", "south America"]:
        #         break
        #     else:
        #         print("Invalid continent. Please try again.")

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
        path_choice = get_path_choice()


        path_choice = input("\nWould you like to (1) get recommendations or (2) search for a resort by name? Enter 1 or 2: ")

        if path_choice == '1':
            factors = ["snow_reliability", "apres_ski", "resort_size", "variety_of_runs", "cleanliness", "proportion_of_black_runs"]
            print("\nYour choices for these factors will be used to recommed the best resorts for you given your priorities.")
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
        elif path_choice == '2':
            resort_name = input("Enter the name of the resort you are looking for: ")
            result = network.search_resort(resort_name)
            if result is None:
                print(f"No resort found with the name {resort_name}.")
            else:
                result.describe()


        restart = input("\nWould you like to restart? (y/n): ")
        if restart.lower() != 'y':
            break

if __name__ == "__main__":
    main()