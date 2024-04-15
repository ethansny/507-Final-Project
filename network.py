import utility as utl
import math
import time
from multiprocessing import Process
from tqdm import tqdm

class Network:
    def __init__(self):
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)

    def get_node(self, name):
        for node in self.nodes:
            if node.name == name:
                return node
        return None


    def get_high_score(self):
        high_score = 0
        high_node = []
        for node in self.nodes:
            if node.score != 0:
                if node.score >= high_score and node.score is not None:
                    high_score = node.score
                    high_node.append(node)
        return high_node

class Node:
    def __init__(self):
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

    def add_connection(self, node, distance):
        self.connections[node] = distance

    def calculate_score(self, priority=1, priority2=1, priority3=1, priority4=1, priority5=1, priority6=1, max_distance=100):
        score = 0
        num_factors = 0
        if self.snow_reliability is not None:
            score += (self.snow_reliability * priority)
            num_factors += 1
        if self.apres_ski is not None:
            score += (self.apres_ski * priority2)
            num_factors += 1
        if self.resort_size is not None:
            score += (self.resort_size * priority3)
            num_factors += 1
        if self.variety_of_runs is not None:
            score += (self.variety_of_runs * priority4)
            num_factors += 1
        if self.cleanliness is not None:
            score += (self.cleanliness * priority5)
            num_factors += 1
        if self.propotion_of_black_runs is not None:
            score += (self.propotion_of_black_runs * priority6)
            num_factors += 1
        for other_node, distance in self.connections.items():
            if distance is not None and distance < max_distance:
                score += other_node.score
                num_factors += 1
        if score == 0:
            return 0
        self.score = score / num_factors


def calculate_distance(lat1, lon1, lat2, lon2):
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

        return distance
    except TypeError:
        return None


def get_priority_input(prompt):
    while True:
        try:
            value = float(input(prompt))
            if 0 <= value <= 1:
                return value
            else:
                print("Please enter a value between 0 and 1.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_distance_input(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value >= 0:
                return value
            else:
                print("Please enter a positive value.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def calculate_proportion_of_black_runs(node):
    try:
        return 5 * (node.black_runs / (node.green_runs + node.blue_runs + node.black_runs))
    except:
        return None



def main():
    network = Network()
    
    resorts = utl.read_csv_to_dicts("resortworldwide.csv")
    nodes = []
    print("List of continents: Africa, Antarctica, Asia, Europe, North America, Oceania, South America")
    while True:
        continent = input("Enter a continent from the above list: ")
        if continent in ["Africa", "Antarctica", "Asia", "Europe", "North America", "Oceania", "South America"]:
            break
        else:
            print("Invalid continent. Please try again.")

    for resort in resorts:
        if resort["Continent"] == continent:
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
            node.snow_reliability = utl.to_int(utl.r_c_w_p(resort["Snow reliability "]))
            node.apres_ski = utl.to_int(utl.r_c_w_p(resort["Après-ski "]))
            node.resort_size = utl.to_int(utl.r_c_w_p(resort["Ski resort size "]))
            node.variety_of_runs = utl.to_int(utl.r_c_w_p(resort["Slope offering, variety of runs "]))
            node.cleanliness = utl.to_int(utl.r_c_w_p(resort["Cleanliness and hygiene "]))
            node.green_runs = utl.to_int(resort["Easy"])
            node.blue_runs = utl.to_int(resort["Intermediate "])
            node.black_runs = utl.to_int(resort["Difficult"])
            node.propotion_of_black_runs = calculate_proportion_of_black_runs(node)
            nodes.append(node)

    for node in tqdm(nodes):
        network.add_node(node)
        for other_node in nodes:
            if node != other_node:
                distance = calculate_distance(node.latitude, node.longitude, other_node.latitude, other_node.longitude)
                node.add_connection(other_node, distance)

    priority = get_priority_input("Enter a priority for snow reliability (0-1): ")
    priority2 = get_priority_input("Enter a priority for apres ski (0-1): ")
    priority3 = get_priority_input("Enter a priority for resort size (0-1): ")
    priority4 = get_priority_input("Enter a priority for variety of runs (0-1): ")
    priority5 = get_priority_input("Enter a priority for cleanliness (0-1): ")
    priority6 = get_priority_input("Enter a priority for proportion of black runs (0-1): ")
    distance = get_distance_input("Enter a distance in kilometers: ")


    for node in tqdm(network.nodes):
        node.calculate_score(priority, priority2, priority3, priority4, priority5, priority6, distance)

    high_node = network.get_high_score()
    for node in high_node[::-1]:
        print(node.name, node.score)



if __name__ == "__main__":
    main()