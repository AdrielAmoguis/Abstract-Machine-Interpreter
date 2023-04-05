import networkx as nx
from matplotlib import pyplot as plt

def graph_abstract_machine(logic):
    keys = logic.keys()
    G = nx.DiGraph()
    for key in keys:
        G.add_node(key)
        for transition in logic[key]:
            G.add_edge(key, transition[1], label=transition[0])
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_edge_labels(G, pos)
    plt.show()