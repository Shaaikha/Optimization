from datetime import datetime
from sortedcontainers import SortedDict


# Helper function to create datetime objects easily
def create_datetime(date_str):
    # This function uses strptime from the datetime module to convert a date string into a datetime object.
    return datetime.strptime(date_str, "%Y-%m-%d %H:%M")


class Post:
    """Creating Class representing a social media post with datetime, content, and user attributes."""

    def __init__(self, postDatetime, postContent, postUser):
        self.postDatetime = postDatetime
        self.postContent = postContent
        self.postUser = postUser

    def __repr__(self):
        # Adding a function that summarizes the attributes for Post object
        return f"Post(datetime={self.postDatetime}, content='{self.postContent}', user='{self.postUser}')"


class PostManager:
    """Creating a Class that Manages posts through hash table with the post datetime as the key"""

    def __init__(self):
        # Creating a dictionary to store the data of the post
        self.posts_by_datetime = {}

    def add_post(self, post):
        # Adding a function that sdds a post to the hash table
        self.posts_by_datetime[post.postDatetime] = post

    def find_post_by_datetime(self, datetime):
        # Creating a function that finds a post by datetime. Returns the post or 'Post not found' if not present
        return self.posts_by_datetime.get(datetime, "Post not found")


from sortedcontainers import SortedDict


# Importing the sort dictionary from sortedcontainers


class PostManagerWithRange:
    """Adding a class that will be in charge of managing posts bySortedDict to generate efficient range queries"""

    def __init__(self):
        # Initializes the init constructor for storing data efficently
        self.sorted_posts = SortedDict()

    def add_post(self, post):
        # This function is created to add add a post to a sorted dictionary
        self.sorted_posts[post.postDatetime] = post

    def find_posts_in_range(self, start_datetime, end_datetime):
        # This function will retreive and get the posts depending on their specified datetime range
        range_indices = self.sorted_posts.irange(start_datetime, end_datetime)
        return [self.sorted_posts[datetime] for datetime in range_indices]


import heapq


class PostWithViews:
    """Creating a class for Wrapper class for Post to handle the max-heap by views"""

    def __init__(self, post, views):
        self.post = post
        self.views = -views  # Undo views for max-heap functionality

    def __lt__(self, other):
        # This function Ensure proper ordering in the heapq by views
        return self.views < other.views

    def __repr__(self):
        # Readable representation of the object for debugging and logging
        return f"{-self.views}, {self.post}"


class PostManagerWithPriority:
    """Creating a class that Manages posts with a priority queue to easily fetch the post with the most views"""

    def __init__(self):
        self.heap = []

    def add_post(self, post, views):
        # This function Adds a post with its views to the heap
        heapq.heappush(self.heap, PostWithViews(post, views))

    def get_most_viewed_post(self):
        # This function Retrieves the post with the most views
        if self.heap:
            return self.heap[0]  # Access the smallest item in the min-heap, which is the largest by views
        return "No posts available"


    class Intersection:
        """Class representing an intersection in the road network.

        Attributes:
            id (int): A unique identifier for the intersection.
            name (str): The name of the intersection.
        """

        def __init__(self, id, name):
            self.id = id  # Unique identifier for each intersection
            self.name = name  # Human-readable name for the intersection

        def __repr__(self):
            # Provides a string representation of the Intersection object, useful for debugging.
            return f"Intersection({self.id}, '{self.name}')"


class Road:
    """Class representing a road connecting two intersections.

    Attributes:
        id (int): A unique identifier for the road.
        name (str): The name of the road.
        length (float): The length of the road in kilometers.
    """

    def __init__(self, id, name, length):
        self.id = id  # Unique identifier for each road
        self.name = name  # Name of the road
        self.length = length  # Length of the road in kilometers

    def __repr__(self):
        # Provides a string representation of the Road object, useful for debugging.
        return f"Road(ID: {self.id}, Name: '{self.name}', Length: {self.length} km)"


class Graph:
    """Graph class to represent the network of intersections and roads.

    Attributes:
        adjacency_list (dict): A dictionary where keys are Intersection objects and values are lists
                               of tuples (Intersection, Road) representing connections to neighboring intersections.
    """

    def __init__(self):
        self.adjacency_list = {}  # Initializes an empty dictionary to store adjacency list.

    def add_vertex(self, vertex):
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []  # Initializes an empty list to store vertices.

    def add_edge(self, frm, to, length):
        # Ensure to include a road name when creating the Road instance.
        road_name = f"Road from {frm} to {to}"
        if frm not in self.adjacency_list:
            self.adjacency_list[frm] = []
        if to not in self.adjacency_list:
            self.adjacency_list[to] = []
        self.adjacency_list[frm].append((to, Road(frm, road_name, length)))
        self.adjacency_list[to].append((frm, Road(to, road_name, length)))  # Assuming bidirectional for simplicity

    def add_intersection(self, intersection):
        """Adds an intersection to the graph if it is not already present."""
        if intersection not in self.adjacency_list:
            self.adjacency_list[intersection] = []  # Adds intersection with an empty list of connected roads.

    def add_road(self, start, end, road):
        """Adds a road between two intersections."""
        self.adjacency_list[start].append((end, road))  # Adds end intersection and road to start's list.
        self.adjacency_list[end].append(
            (start, road))  # Adds start intersection and road to end's list (bidirectional).

    def display(self):
        """Prints a representation of the graph showing all connections."""
        for intersection, roads in self.adjacency_list.items():
            print(f"{intersection}:")
            for neighbor, road in roads:
                print(f"  -> to {neighbor} via {road}")


# Code for Part 2: Nearest Neighbor Heuristic for Package Distribution
# Function to calculate the shortest distance between two points a and b.
# Each point is represented as a tuple (x-coordinate, y-coordinate).
def distance(a, b):
    # Calculate the square root of the sum of the squared differences of the coordinates.
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


# Function to find the nearest neighbor route for package delivery starting from a given location.
def find_nearest_neighbor(start, houses):
    # Initialize the route with the start location.
    route = [start]
    # Set the current location as the start location.
    current = start

    # Continue until there are no more houses to visit.
    while houses:
        # Find the house nearest to the current location by comparing distances.
        next_house = min(houses, key=lambda x: distance(current, x))
        # Append the nearest house to the route.
        route.append(next_house)
        # Remove the visited house from the list of houses to prevent revisiting.
        houses.remove(next_house)
        # Update the current location to the newly visited house.
        current = next_house

    # Return the completed route that includes all visited houses.
    return route


# Import the heapq module to use the heap queue algorithm, also known as the priority queue algorithm.
import heapq


# Define the Dijkstra's algorithm function to find the shortest paths from a start vertex to all other vertices in a graph.
def dijkstra(graph, start):
    # Initialize a dictionary to store the shortest distance from the start vertex to each other vertex.
    # Set all distances to infinity as default, except the start vertex which is set to zero.
    distances = {vertex: float('infinity') for vertex in graph.adjacency_list}
    distances[start] = 0

    # Create a priority queue and add the start vertex with a distance of 0.
    priority_queue = [(0, start)]

    # Continue processing as long as there are vertices in the priority queue.
    while priority_queue:
        # Remove and return the vertex with the smallest distance from the priority queue.
        current_distance, current_vertex = heapq.heappop(priority_queue)

        # Iterate over each neighbor connected to the current vertex.
        for neighbor, road in graph.adjacency_list[current_vertex]:
            # Calculate the distance to this neighbor by adding the current distance to the length of the connecting road.
            distance = current_distance + road.length
            # If the calculated distance is less than the previously recorded distance in the distances dictionary,
            # update the distance for this neighbor.
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                # Add the neighbor to the priority queue with the new distance.
                heapq.heappush(priority_queue, (distance, neighbor))

    # Return the dictionary containing the shortest distances from the start vertex to each vertex in the graph.
    return distances

# Initialize the PostManager
post_manager = PostManager()

# Test Case 1: Single Post Retrieval
def test_single_post_retrieval():
    dt = create_datetime("2024-04-01 12:00")
    post = Post(dt, "Hello, world!", "Alice")
    post_manager.add_post(post)
    print("Test Case 1 - Single Post Retrieval:", post_manager.find_post_by_datetime(dt))

# Test Case 2: Post Not Found
def test_post_not_found():
    dt = create_datetime("2025-01-01 00:00")
    print("Test Case 2 - Post Not Found:", post_manager.find_post_by_datetime(dt))

# Test Case 3: Multiple Posts, Same DateTime
def test_multiple_posts_same_datetime():
    dt = create_datetime("2024-04-01 12:00")
    post1 = Post(dt, "First post", "Bob")
    post2 = Post(dt, "Second post", "Carol")
    post_manager.add_post(post1)  # Add first post
    post_manager.add_post(post2)  # Intentionally overwrite with second post
    print("Test Case 3 - Multiple Posts, Same DateTime:", post_manager.find_post_by_datetime(dt))

# Test Case 4: Post Update Test
def test_post_update():
    dt = create_datetime("2024-04-01 12:00")
    original_post = Post(dt, "Original post", "Dave")
    updated_post = Post(dt, "Updated post", "Eve")
    post_manager.add_post(original_post)
    post_manager.add_post(updated_post)  # Update with new content
    print("Test Case 4 - Post Update Test:", post_manager.find_post_by_datetime(dt))

# Test Case 5: Retrieval After Deletion
def test_retrieval_after_deletion():
    dt = create_datetime("2024-06-15 18:30")
    post = Post(dt, "This will be deleted", "Frank")
    post_manager.add_post(post)
    del post_manager.posts_by_datetime[dt]  # Manually delete the post
    print("Test Case 5 - Retrieval After Deletion:", post_manager.find_post_by_datetime(dt))

# Run all test cases
test_single_post_retrieval()
test_post_not_found()
test_multiple_posts_same_datetime()
test_post_update()
test_retrieval_after_deletion()

# Instantiate PostManagerWithRange
post_manager = PostManagerWithRange()

# Add posts with Arabic names written in English
posts = [
    Post(create_datetime("2022-10-01 10:00"), "Good morning!", "Ali"),
    Post(create_datetime("2022-10-01 10:15"), "Coffee time", "Rashed"),
    Post(create_datetime("2022-10-01 10:30"), "Time for work", "Jameela"),
    Post(create_datetime("2022-10-01 10:45"), "Meeting time", "Mohamed"),
    Post(create_datetime("2022-10-01 11:00"), "Lunch break", "Sarah")
]

for post in posts:
    post_manager.add_post(post)

# Test cases
def test_single_post_retrieval():
    result = post_manager.find_posts_in_range(create_datetime("2022-10-01 10:30"), create_datetime("2022-10-01 10:30"))
    print("Single Post Retrieval Test:", result)

def test_multiple_posts_in_range():
    result = post_manager.find_posts_in_range(create_datetime("2022-10-01 10:15"), create_datetime("2022-10-01 10:45"))
    print("Multiple Posts in Range Test:", result)

def test_boundary_test():
    result = post_manager.find_posts_in_range(create_datetime("2022-10-01 10:00"), create_datetime("2022-10-01 10:45"))
    print("Boundary Test:", result)

def test_no_posts_in_range():
    result = post_manager.find_posts_in_range(create_datetime("2022-10-02 10:00"), create_datetime("2022-10-02 11:00"))
    print("No Posts in Range Test:", result)

def test_overlapping_dates():
    result = post_manager.find_posts_in_range(create_datetime("2022-10-01 10:30"), create_datetime("2022-10-01 10:30"))
    print("Overlapping Dates Test:", result)

# Running all test cases
test_single_post_retrieval()
test_multiple_posts_in_range()
test_boundary_test()
test_no_posts_in_range()
test_overlapping_dates()

# Initialize the PostManagerWithPriority
post_manager = PostManagerWithPriority()

# Test Case 1: Add a single post and retrieve it
post_manager.add_post("Post 1: Introduction to Python", 250)
print("Test Case 1:", post_manager.get_most_viewed_post())  # Expected Output: "250, Post 1: Introduction to Python"

# Test Case 2: Add multiple posts and retrieve the most viewed
post_manager.add_post("Post 2: Advanced Python", 150)
post_manager.add_post("Post 3: Python Tips and Tricks", 300)
print("Test Case 2:", post_manager.get_most_viewed_post())  # Expected Output: "300, Post 3: Python Tips and Tricks"

# Test Case 3: Add a post with zero views and verify the most viewed doesn't change
post_manager.add_post("Post 4: New Python Features", 0)
print("Test Case 3:", post_manager.get_most_viewed_post())  # Expected Output: "300, Post 3: Python Tips and Tricks"

# Test Case 4: Check retrieval when no posts are available (Empty heap)
post_manager = PostManagerWithPriority()  # Reinitialize to clear the heap
print("Test Case 4:", post_manager.get_most_viewed_post())  # Expected Output: "No posts available"

# Test Case 5: Add posts with decreasing views and verify correct ordering
post_manager.add_post("Post 5: Python Decorators", 200)
post_manager.add_post("Post 6: Understanding Generators", 100)
post_manager.add_post("Post 7: Lambda Functions in Python", 50)
print("Test Case 5:", post_manager.get_most_viewed_post())  # Expected Output: "200, Post 5: Python Decorators"

# Test cases for Part 1: Testing Graph Representation





# Test cases for Part 2: Testing Nearest Neighbor Heuristic
def test_nearest_neighbor_heuristic():
    # Test Case 1: Single House Delivery
    start = (0, 0)
    houses = [(2, 2)]
    print("Test Case 1: Single House Delivery", find_nearest_neighbor(start, houses[:]))

    # Test Case 2: Multiple Houses in Line
    start = (0, 0)
    houses = [(10, 10), (20, 20), (30, 30)]
    print("Test Case 2: Multiple Houses in Line", find_nearest_neighbor(start, houses[:]))

    # Test Case 3: Cluster of Houses
    start = (0, 0)
    houses = [(5, 5), (5, 6), (6, 5), (6, 6)]
    print("Test Case 3: Cluster of Houses", find_nearest_neighbor(start, houses[:]))

    # Test Case 4: No Houses
    start = (0, 0)
    houses = []
    print("Test Case 4: No Houses", find_nearest_neighbor(start, houses[:]))

    # Test Case 5: Multiple Houses in a Complex Pattern
    start = (0, 0)
    houses = [(1, 1), (10, 1), (1, 10), (10, 10)]
    print("Test Case 5: Multiple Houses in a Complex Pattern", find_nearest_neighbor(start, houses[:]))

test_nearest_neighbor_heuristic()

def create_graph_and_test():
    # Test Case 1: Basic Linear Graph
    graph = Graph()
    for i in range(5):
        graph.add_vertex(i)
    for i in range(4):
        graph.add_edge(i, i + 1, i + 1)
    print("Test Case 1: Basic Linear Graph", dijkstra(graph, 0))

    # Test Case 2: Star Shaped Graph
    graph = Graph()
    graph.add_vertex(0)
    for i in range(1, 5):
        graph.add_vertex(i)
        graph.add_edge(0, i, 1)
    print("Test Case 2: Star Shaped Graph", dijkstra(graph, 0))


    # Test Case 3: Complete Graph
    graph = Graph()
    for i in range(4):
        graph.add_vertex(i)
    for i in range(3):
        for j in range(i + 1, 4):
            graph.add_edge(i, j, 1)
    print("Test Case 3: Complete Graph", dijkstra(graph, 0))

create_graph_and_test()

def test_dijkstras_algorithm():
    # Create a graph instance
    graph = Graph()

    # Add vertices to the graph
    vertices = ['A', 'B', 'C', 'D']
    for vertex in vertices:
        graph.add_vertex(vertex)

    # Add edges between vertices with weights (lengths)
    graph.add_edge('A', 'B', 1)
    graph.add_edge('B', 'C', 2)
    graph.add_edge('A', 'C', 4)
    graph.add_edge('C', 'D', 1)
    graph.add_edge('B', 'D', 5)

    # Apply Dijkstra's algorithm starting from vertex 'A'
    shortest_paths = dijkstra(graph, 'A')

    # Print the shortest paths from start vertex 'A' to all other vertices
    print("Shortest paths from vertex 'A':", shortest_paths)

# Execute the test case
test_dijkstras_algorithm()

def test_dijkstras_star_graph():
    graph = Graph()

    # Central vertex and other vertices
    vertices = ['A', 'B', 'C', 'D', 'E']
    for vertex in vertices:
        graph.add_vertex(vertex)

    # Adding edges from central vertex 'A' to all other vertices with varying weights
    graph.add_edge('A', 'B', 3)
    graph.add_edge('A', 'C', 5)
    graph.add_edge('A', 'D', 1)
    graph.add_edge('A', 'E', 2)

    # Apply Dijkstra's algorithm starting from vertex 'A'
    shortest_paths = dijkstra(graph, 'A')

    # Print the shortest paths from start vertex 'A'
    print("Shortest paths from vertex 'A':", shortest_paths)

# Execute the star graph test case
test_dijkstras_star_graph()



def test_dijkstras_linear_graph_reversed():
    graph = Graph()

    # Create a linear chain of vertices
    vertices = ['A', 'B', 'C', 'D']
    for vertex in vertices:
        graph.add_vertex(vertex)

    # Add edges to form a linear path with increasing weights
    graph.add_edge('A', 'B', 1)
    graph.add_edge('B', 'C', 2)
    graph.add_edge('C', 'D', 3)

    # Apply Dijkstra's algorithm starting from vertex 'D'
    shortest_paths = dijkstra(graph, 'D')

    # Print the shortest paths from start vertex 'D'
    print("Shortest paths from vertex 'D':", shortest_paths)

# Execute the linear graph reverse path test case
test_dijkstras_linear_graph_reversed()

# Test cases for Part 1: Testing Graph Representation


class Intersection:
    """Class representing an intersection in the road network.

    Attributes:
        id (int): A unique identifier for the intersection.
        name (str): The name of the intersection.
    """

    def __init__(self, id, name):
        self.id = id  # Unique identifier for each intersection
        self.name = name  # Human-readable name for the intersection

    def __repr__(self):
        # Provides a string representation of the Intersection object, useful for debugging.
        return f"Intersection({self.id}, '{self.name}')"


class Road:
    """Class representing a road connecting two intersections.

    Attributes:
        id (int): A unique identifier for the road.
        name (str): The name of the road.
        length (float): The length of the road in kilometers.
    """

    def __init__(self, id, name, length):
        self.id = id  # Unique identifier for each road
        self.name = name  # Name of the road
        self.length = length  # Length of the road in kilometers

    def __repr__(self):
        # Provides a string representation of the Road object, useful for debugging.
        return f"Road(ID: {self.id}, Name: '{self.name}', Length: {self.length} km)"


class Graph:
    """Graph class to represent the network of intersections and roads.

    Attributes:
        adjacency_list (dict): A dictionary where keys are Intersection objects and values are lists
                               of tuples (Intersection, Road) representing connections to neighboring intersections.
    """

    def __init__(self):
        self.adjacency_list = {}  # Initializes an empty dictionary to store adjacency list.

    def add_vertex(self, vertex):
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []  # Initializes an empty list to store vertices.

    def add_edge(self, frm, to, length):
        # Ensure to include a road name when creating the Road instance.
        road_name = f"Road from {frm} to {to}"
        if frm not in self.adjacency_list:
            self.adjacency_list[frm] = []
        if to not in self.adjacency_list:
            self.adjacency_list[to] = []
        self.adjacency_list[frm].append((to, Road(frm, road_name, length)))
        self.adjacency_list[to].append((frm, Road(to, road_name, length)))  # Assuming bidirectional for simplicity

    def add_intersection(self, intersection):
        """Adds an intersection to the graph if it is not already present."""
        if intersection not in self.adjacency_list:
            self.adjacency_list[intersection] = []  # Adds intersection with an empty list of connected roads.

    def add_road(self, start, end, road):
        """Adds a road between two intersections."""
        self.adjacency_list[start].append((end, road))  # Adds end intersection and road to start's list.
        self.adjacency_list[end].append(
            (start, road))  # Adds start intersection and road to end's list (bidirectional).

    def display(self):
        """Prints a representation of the graph showing all connections."""
        for intersection, roads in self.adjacency_list.items():
            print(f"{intersection}:")
            for neighbor, road in roads:
                print(f"  -> to {neighbor} via {road}")


# Test cases for Part 1: Testing Graph Representation


def test_uae_road_network():
    graph = Graph()
    intersections = [
        Intersection(1, "Dubai Marina"),
        Intersection(2, "JBR"),
        Intersection(3, "Downtown Dubai"),
        Intersection(4, "Business Bay")
    ]

    roads = [
        Road(1, "Sheikh Zayed Road", 2.0),
        Road(2, "Al Khail Road", 5.0),
        Road(3, "Sheikh Mohammed bin Rashid Blvd", 1.5),
        Road(4, "Hessa Street", 3.5)
    ]

    for intersection in intersections:
        graph.add_intersection(intersection)

    graph.add_road(intersections[0], intersections[1], roads[0])
    graph.add_road(intersections[1], intersections[2], roads[1])
    graph.add_road(intersections[2], intersections[3], roads[2])
    graph.add_road(intersections[3], intersections[0], roads[3])

    graph.display()

test_uae_road_network()

def test_graph_operations():
    graph = Graph()

    # Test Case 1: Add Single Intersection and Display
    intersection1 = Intersection(1, "Main Street")
    graph.add_intersection(intersection1)
    print("Test Case 1: Add Single Intersection and Display")
    graph.display()

    # Test Case 2: Add Multiple Intersections and Single Road
    intersection2 = Intersection(2, "Second Street")
    graph.add_intersection(intersection2)
    road1 = Road(101, "Connector Road", 1.5)
    graph.add_road(intersection1, intersection2, road1)
    print("\nTest Case 2: Add Multiple Intersections and Single Road")
    graph.display()

    # Test Case 3: Add Road to Non-existent Intersections
    intersection3 = Intersection(3, "Third Street")
    road2 = Road(102, "Third Connector", 2.0)
    print("\nTest Case 3: Attempt to Add Road to Non-existent Intersection")
    try:
        graph.add_road(intersection2, intersection3, road2)  # Only intersection2 is added
    except KeyError as e:
        print("Caught an error as expected when adding a road to a non-existent intersection:", e)
    graph.display()

    # Test Case 4: Complex Network Creation
    graph.add_intersection(intersection3)
    graph.add_road(intersection2, intersection3, road2)
    print("\nTest Case 4: Complex Network Creation")
    graph.display()

    # Test Case 5: Repeated Addition of Same Intersection and Road
    graph.add_intersection(intersection1)  # Try to add intersection1 again
    graph.add_road(intersection1, intersection2, road1)  # Try to add road1 again
    print("\nTest Case 5: Repeated Addition of Same Intersection and Road")
    graph.display()

# Execute the test cases
test_graph_operations()