import utility as utl
import math
from tqdm import tqdm
from get_snow_data import get_snow_data
import time
import os

class Network:
    """
    A class to represent a network.

    ...

    Attributes
    ----------
    nodes : list
        a list of nodes in the network

    Methods
    -------
    add_node(node):
        Adds a node to the network.
    get_node(name):
        Returns a node with the specified name from the network.
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for the network object.

        ...

        Attributes
        ----------
        nodes : list
            an empty list of nodes in the network
        """
        self.nodes = []

    def add_node(self, node):
        """
        Adds a node to the network.

        Parameters
        ----------
        node : Node
            a node to be added to the network
        """
        self.nodes.append(node)

    def get_node(self, name):
        """
        Returns a node with the specified name from the network.

        Parameters
        ----------
        name : str
            name of the node to be returned

        Returns
        -------
        Node
            a node with the specified name from the network
        None
            if no node with the specified name is found in the network
        """
        for node in self.nodes:
            if node.name == name:
                return node
        return None


    def get_high_score(self):
        """
        Returns nodes with the highest score in the network.

        This method iterates over all nodes in the network, and if a node's score is not zero and is greater than or equal to the current highest score, 
        it updates the highest score and adds the node to the list of nodes with the highest score.

        Returns
        -------
        list
            a list of nodes with the highest score in the network. If no nodes have a score greater than zero, an empty list is returned.
        """
        high_score = 0
        high_node = []
        for node in self.nodes:
            if node.score != 0:
                if node.score >= high_score and node.score is not None:
                    high_score = node.score
                    high_node.append(node)
        return high_node

class Node:
    """
    A class to represent a node in a network.

    ...

    Attributes
    ----------
    name : str
        name of the node
    score : int
        score of the node
    connections : dict
        a dictionary of connections to other nodes, with the nodes as keys and the distances as values
    url : str
        url of the node
    km_freeride : float
        kilometers of freeride of the node
    continent : str
        continent of the node
    country : str
        country of the node
    state_province : str
        state or province of the node
    snow_reliability : float
        snow reliability of the node
    apres_ski : float
        apres ski of the node
    latitude : float
        latitude of the node
    longitude : float
        longitude of the node
    resort_size : float
        resort size of the node
    variety_of_runs : float
        variety of runs of the node
    cleanliness : float
        cleanliness of the node
    green_runs : float
        green runs of the node
    blue_runs : float
        blue runs of the node
    black_runs : float
        black runs of the node
    propotion_of_black_runs : float
        proportion of black runs of the node

    Methods
    -------
    add_connection(node, distance):
        Adds a connection to another node with a specified distance.
    """
    class Network:
        __slots__ = ('name', 'score', 'connections', 'url', 'km_freeride', 'continent', 'country', 'state_province', 
                     'snow_reliability', 'apres_ski', 'latitude', 'longitude', 'resort_size', 'variety_of_runs', 
                     'cleanliness', 'green_runs', 'blue_runs', 'black_runs', 'propotion_of_black_runs', 
                     'normalized_snow_depth')

        def __init__(self):
            """
            Constructs all the necessary attributes for the node object.
            """
            self.name = None
            self.score = 0
            self.connections = {}
            self.url = None
            self.km_freeride = None
            self.continent = None
            self.country = None
            self.state_province = None
            self.snow_reliability = None
            self.apres_ski = None
            self.latitude = None
            self.longitude = None
            self.resort_size = None
            self.variety_of_runs = None
            self.cleanliness = None
            self.green_runs = None
            self.blue_runs = None
            self.black_runs = None
            self.propotion_of_black_runs = None
            self.normalized_snow_depth = None

    def add_connection(self, node, distance):
        """
        Adds a connection to another node with a specified distance.

        Parameters
        ----------
        node : Node
            a node to connect to
        distance : float
            distance to the node
        """
        self.connections[node] = distance

    def calculate_score(self, factors, max_distance=100):
        """
        Calculates the score of the node based on the specified factors and their priorities.

        Parameters
        ----------
        factors : list of tuples
            a list of tuples where each tuple contains a factor (as a string) and its priority (as a float)
        max_distance : float
            the maximum distance for connections to be considered in the score calculation

        Returns
        -------
        None
        """
        score = 0
        num_factors = 0
        if self.normalized_snow_depth is not None:
            score += self.normalized_snow_depth
            num_factors += 1

        for factor, priority in factors:
            factor_value = getattr(self, factor, None)
            if factor_value is not None:
                score += factor_value * priority
                num_factors += 1
        if max_distance > 0:
            for other_node, distance in self.connections.items():
                if distance is not None and distance < max_distance and distance != 0 and other_node.score != 0:
                    score += other_node.score
                    num_factors += 1
        if score == 0:
            return 0
        if num_factors < 2:
            return 0
        self.score = score / num_factors


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



def calculate_proportion_of_black_runs(node):
    try:
        return 5 * (node.black_runs / (node.green_runs + node.blue_runs + node.black_runs))
    except:
        return None

def add_connections(node, nodes):
    for other_node in nodes:
        if node != other_node:
            distance = calculate_distance(node.latitude, node.longitude, other_node.latitude, other_node.longitude)
            node.add_connection(other_node, distance)

def main():
    network = Network()

    cache_file = "cache.json"

    try:
        # Try to open the cache file
        cache = utl.read_json(cache_file)
        file_time = os.path.getmtime(cache_file)
        if (time.time() - file_time) / (24 * 60 * 60) > 3:
            cache = {}
    except FileNotFoundError:
        # If the file is not found, create an empty cache
        cache = {}

    resorts = utl.read_csv_to_dicts("resortworldwide.csv")
    nodes = []
    print("List of continents: Africa, Antarctica, Asia, Europe, North America, Oceania, South America")
    while True:
        continent = input("Enter a continent from the above list: ")
        if continent in ["Africa", "Asia", "Europe", "North America", "Oceania", "South America"]:
            break
        else:
            print("Invalid continent. Please try again.")
    resorts_in_continent = [resort for resort in resorts if resort["Continent"] == continent]
    print(f"Found {len(resorts_in_continent)} resorts in {continent}. \n Getting snow data...")

    for resort in tqdm(resorts_in_continent):
        node = Node()
        node.name = resort["NameResort"]
        node.url = resort["URL"]
        node.stars = utl.to_int(resort["Stars"])
        node.km_freeride = utl.to_int(resort["Km Freeride"])
        node.latitude = utl.to_float(resort["latitude"])
        node.longitude = utl.to_float(resort["longitude"])
        node.score = 0
        node.connections = {}
        node.continent = resort["Continent"]
        node.snow_reliability = utl.to_int(utl.clean_string(resort["Snow reliability "]))
        node.apres_ski = utl.to_int(utl.clean_string(resort["Après-ski "]))
        node.resort_size = utl.to_int(utl.clean_string(resort["Ski resort size "]))
        node.variety_of_runs = utl.to_int(utl.clean_string(resort["Slope offering, variety of runs "]))
        node.cleanliness = utl.to_int(utl.clean_string(resort["Cleanliness and hygiene "]))
        node.green_runs = utl.to_int(resort["Easy"])
        node.blue_runs = utl.to_int(resort["Intermediate "])
        node.black_runs = utl.to_int(resort["Difficult"])
        node.propotion_of_black_runs = calculate_proportion_of_black_runs(node)
        try:
            node.current_snow = cache[node.name]
        except:
            node.current_snow = get_snow_data(node.name)
            cache[node.name] = node.current_snow
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