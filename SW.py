import networkx as nx

smallSW = nx.watts_strogatz_graph(500, 6, 0.64)
bigSW = nx.watts_strogatz_graph(1500, 6, 0.64)

def getSmallSW():
    return smallSW

def getBigSW():
    return bigSW