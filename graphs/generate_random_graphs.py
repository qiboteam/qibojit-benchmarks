"""Generate random regular graphs for MaxCut QAOA benchmark."""
import json
import networkx


for nqubits in range(4, 31, 2):
    graph = networkx.random_regular_graph(3, nqubits)
    data = networkx.readwrite.json_graph.node_link_data(graph)
    with open(f"randomgraph_3_{nqubits}.json", "w") as file:
        json.dump(data, file)
