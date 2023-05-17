import networkx as nx

smallBA = nx.barabasi_albert_graph(500,5)
bigBA = nx.barabasi_albert_graph(1500,5)

def getSmallBA():
    return smallBA

def getBigBA():
    return bigBA