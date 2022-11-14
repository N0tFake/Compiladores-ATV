import matplotlib.pyplot as plt
import networkx as nx 

import numpy as np

def plotAutomato(automato):

    G = nx.DiGraph()

    G.add_nodes_from(automato.states)

    for transition in automato.transition:
        if type(transition.transition) == int:
            G.add_edge(
                transition.state, 
                transition.transition,
                label=transition.symbol if transition.symbol != None else '\u03B5'
            )
        else:
            for i in transition.transition:
                G.add_edge(
                transition.state, 
                i,
                label=transition.symbol if transition.symbol != None else '\u03B5'
            )


    for state in automato.states:
        if state == automato.initial:
            G.nodes[state]['color'] = 'green'
        elif state == automato.finals[0]:
            G.nodes[state]['color'] = 'red'
        else:
            G.nodes[state]['color'] = 'pink'

    colors = [node[1]['color'] for node in G.nodes(data=True)]

    print(colors)

    edge_labels = nx.get_edge_attributes(G, 'label')
    print(edge_labels)

    pos=nx.spectral_layout(G)

    nx.draw(G, pos, with_labels=True, edge_color='black', width=1, linewidths=1,
        node_size=500, node_color=colors, alpha=0.9)
    nx.draw_networkx_edge_labels(G, pos, edge_labels, label_pos=0.5)

    plt.figure(1,figsize=(8,8))

    plt.savefig('automato.png') 
    plt.close()
    G.clear()
