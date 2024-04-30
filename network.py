import utility as utl
from data_structure import *
import math
from tqdm import tqdm
from get_snow_data import get_snow_data
import os


def add_connections(node, nodes):
    """
    Add connections between the given node and other nodes in the network.

    Parameters:
    - node: The node to add connections to.
    - nodes: A list of other nodes in the network.

    Returns:
    None
    """
    for other_node in nodes:
        if node != other_node:
            distance = calculate_distance(node.latitude, node.longitude, other_node.latitude, other_node.longitude)
            node.add_connection(other_node, distance)

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two points.

    Given longitudes and latitudes using the Haversine formula.

    Parameters
    ----------
    lat1 : float
        Latitude of the first point in decimal degrees.
    lon1 : float
        Longitude of the first point in decimal degrees.
    lat2 : float
        Latitude of the second point in decimal degrees.
    lon2 : float
        Longitude of the second point in decimal degrees.

    Returns
    -------
    float
        The great-circle distance between the two points in kilometers.
        Returns None if any of the inputs are not numbers (TypeError).

    """
    try:
        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)
        lat2 = math.radians(lat2)
        lon2 = math.radians(lon2)

        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        r = 6371.0

        # Calculate distance
        distance = r * c
        if distance == 0.0:
            return None
        return distance
    except TypeError:
        return None




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

    print(f"\nConnecting resorts...")
    for node in tqdm(nodes):
        network.add_node(node)
        for other_node in nodes:
            if node != other_node:
                distance = calculate_distance(node.latitude, node.longitude, other_node.latitude, other_node.longitude)
                node.add_connection(other_node, distance)
                node.normalized_snow_depth = (node.current_snow / max_snow_depth * 5) if node.current_snow is not None else None

    factors = ["snow_reliability", "apres_ski", "resort_size", "variety_of_runs", "cleanliness", "proportion_of_black_runs"]

    priorities = []
    for factor in factors:
        priority = utl.get_priority_input(f"Enter a priority for {factor} (0-1): ")
        priorities.append((factor, priority))

    distance = utl.get_distance_input("Enter a distance in kilometers: ")

    print("\nCalculating scores...")
    for node in tqdm(network.nodes):
        node.calculate_score(priorities, distance)

    print("\nTop resorts:")
    high_node = network.get_high_score()
    for node in high_node[::-1]:
        print(node.name, node.score)



if __name__ == "__main__":
    main()