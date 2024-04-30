import utility as utl
from get_snow_data import get_snow_data
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
    def __init__(self):
        __slots__ = ('name', 'score', 'connections', 'url', 'km_freeride', 'continent', 'country', 'state_province', 
                'snow_reliability', 'apres_ski', 'latitude', 'longitude', 'resort_size', 'variety_of_runs', 
                'cleanliness', 'green_runs', 'blue_runs', 'black_runs', 'propotion_of_black_runs', 
                'normalized_snow_depth')
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

    def calculate_proportion_of_black_runs(self):
        """
        Calculate the proportion of black runs for a given node.

        Parameters:
        node (Node): The node object containing the number of black, green, and blue runs.

        Returns:
        float: The proportion of black runs, calculated as 5 times the ratio of black runs to the total number of runs.

        Raises:
        None

        """
        try:
            return 5 * (self.black_runs / (self.green_runs + self.blue_runs + self.black_runs))
        except:
            return None

    @classmethod
    def from_resort(cls, resort, cache):
        node = cls()
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
        node.propotion_of_black_runs = node.calculate_proportion_of_black_runs()
        try:
            node.current_snow = cache[node.name]
        except:
            node.current_snow = get_snow_data(node.name)
            cache[node.name] = node.current_snow
        return node
    


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