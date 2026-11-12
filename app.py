import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt


# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="Smart Route Finder",
    page_icon="🗺️",
    layout="wide"
)


# --------------------------------
# INITIAL GRAPH
# --------------------------------

if "graph" not in st.session_state:

    st.session_state.graph = {
        "College": {
            "Library": 2,
            "Market": 6
        },

        "Library": {
            "College": 2,
            "Market": 3,
            "Hospital": 7
        },

        "Market": {
            "College": 6,
            "Library": 3,
            "Hospital": 2
        },

        "Hospital": {
            "Library": 7,
            "Market": 2
        }
    }


graph = st.session_state.graph


# --------------------------------
# DIJKSTRA ALGORITHM
# --------------------------------

def dijkstra(graph, start, destination):

    distances = {}

    for place in graph:
        distances[place] = float("inf")

    distances[start] = 0

    previous = {}

    unvisited = list(graph.keys())

    while unvisited:

        current = min(
            unvisited,
            key=lambda place: distances[place]
        )

        if distances[current] == float("inf"):
            break

        if current == destination:
            break

        unvisited.remove(current)

        for neighbor, distance in graph[current].items():

            if neighbor in unvisited:

                new_distance = distances[current] + distance

                if new_distance < distances[neighbor]:

                    distances[neighbor] = new_distance

                    previous[neighbor] = current

    # Check whether a route exists

    if distances[destination] == float("inf"):
        return None, float("inf")

    # Find shortest route

    route = []

    current = destination

    while current != start:

        route.append(current)

        current = previous[current]

    route.append(start)

    route.reverse()

    return route, distances[destination]


# --------------------------------
# WEBSITE HEADER
# --------------------------------

st.title("🗺️ Smart Route Finder")

st.subheader("Find the Shortest Route Using Dijkstra's Algorithm")

st.write(
    "This application finds the shortest distance "
    "between two locations using Dijkstra's Algorithm."
)

st.divider()


# --------------------------------
# SIDEBAR - ADD LOCATIONS
# --------------------------------

st.sidebar.header("Manage Locations")

with st.sidebar.form("location_form"):

    new_location = st.text_input(
        "Enter New Location"
    )

    add_location = st.form_submit_button(
        "Add Location"
    )

    if add_location:

        new_location = new_location.strip()

        if not new_location:
            st.sidebar.error("Enter a location name.")

        elif new_location in graph:
            st.sidebar.warning("Location already exists.")

        else:
            graph[new_location] = {}

            st.sidebar.success(
                "Location added successfully!"
            )

            st.rerun()


# --------------------------------
# SIDEBAR - ADD ROADS
# --------------------------------

st.sidebar.header("Add Roads")

locations = list(graph.keys())

if len(locations) >= 2:

    with st.sidebar.form("road_form"):

        place1 = st.selectbox(
            "First Location",
            locations
        )

        place2 = st.selectbox(
            "Second Location",
            [place for place in locations if place != place1]
        )

        distance = st.number_input(
            "Distance in KM",
            min_value=0.1,
            value=1.0
        )

        add_road = st.form_submit_button(
            "Add Road"
        )

        if add_road:

            graph[place1][place2] = distance

            graph[place2][place1] = distance

            st.sidebar.success(
                "Road added successfully!"
            )

            st.rerun()

else:
    st.sidebar.info("Add at least two locations first.")


# --------------------------------
# DISPLAY LOCATIONS
# --------------------------------

st.header("Available Locations")

locations = list(graph.keys())

st.write(", ".join(locations))

st.divider()


# --------------------------------
# SELECT START AND DESTINATION
# --------------------------------

st.header("Find Your Shortest Route")

col1, col2 = st.columns(2)

with col1:

    start = st.selectbox(
        "Starting Location",
        locations
    )

with col2:

    destination = st.selectbox(
        "Destination",
        locations
    )


# --------------------------------
# FIND SHORTEST ROUTE
# --------------------------------

if st.button("Find Shortest Route"):

    if start == destination:

        st.info("Starting location and destination are the same.")

        route = [start]
        distance = 0

    else:

        route, distance = dijkstra(
            graph,
            start,
            destination
        )

    if route is None:

        st.error("No route found between these locations.")

    else:

        st.success("Shortest Route Found!")

        # Display result

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Total Distance",
                str(distance) + " KM"
            )

        with col2:

            st.metric(
                "Number of Locations",
                len(route)
            )

        st.subheader("Shortest Route")

        st.write(" ➜ ".join(route))

        # --------------------------------
        # GRAPH VISUALIZATION
        # --------------------------------

        st.subheader("Graph Visualization")

        G = nx.Graph()

        for place in graph:

            G.add_node(place)

        for place1 in graph:

            for place2, weight in graph[place1].items():

                if not G.has_edge(place1, place2):

                    G.add_edge(
                        place1,
                        place2,
                        weight=weight
                    )

        pos = nx.spring_layout(
            G,
            seed=42
        )

        fig, ax = plt.subplots(figsize=(10, 6))

        # Draw all nodes

        nx.draw_networkx_nodes(
            G,
            pos,
            node_color="lightblue",
            node_size=2000,
            ax=ax
        )

        # Draw all edges

        nx.draw_networkx_edges(
            G,
            pos,
            edge_color="gray",
            width=2,
            ax=ax
        )

        # Highlight shortest route

        if len(route) > 1:

            route_edges = list(
                zip(route, route[1:])
            )

            nx.draw_networkx_edges(
                G,
                pos,
                edgelist=route_edges,
                edge_color="red",
                width=4,
                ax=ax
            )

        # Draw labels

        nx.draw_networkx_labels(
            G,
            pos,
            font_size=10,
            font_weight="bold",
            ax=ax
        )

        # Display distances

        edge_labels = nx.get_edge_attributes(
            G,
            "weight"
        )

        nx.draw_networkx_edge_labels(
            G,
            pos,
            edge_labels=edge_labels,
            ax=ax
        )

        plt.title("Shortest Route Graph")

        plt.axis("off")

        st.pyplot(fig)

        plt.close(fig)


# --------------------------------
# FOOTER
# --------------------------------

st.divider()

st.caption(
    "DAA Mini Project | Smart Route Finder "
    "using Dijkstra's Algorithm"
)