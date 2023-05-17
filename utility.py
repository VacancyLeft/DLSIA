import BA
import SW
import ICLT
import RealWorldData
import random
import networkx as nx
import numpy as np

def getNodesNumber(g):
    return len(list(g.nodes))

def getEdgesNumber(g):
    return len(list(g.edges))

def getDegreeMartrix(g):
    N = getNodesNumber(g)
    # 节点数
    adj = np.array(nx.adjacency_matrix(g).todense())
    row = adj.shape[0]
    col = adj.shape[1]
    degree = np.empty([row, col], dtype=int)
    nodes = list(g.nodes)
    for i in range(0,N-1):
        node = nodes[i]
        degree[i][i] = g.degree(node)
    return degree

def getDegreeList(g):
    N = getNodesNumber(g)
    # 节点数
    adj = np.mat(nx.adjacency_matrix(g).todense())
    row = adj.shape[0]
    col = adj.shape[1]
    degree = [0 for i in range(N)]
    nodes = list(g.nodes)
    for i in range(N):
        node  = nodes[i]
        degree[i] = g.degree(node)
    return degree

def getAdjMartrix(g):
    adj = np.mat(nx.adjacency_matrix(g).todense())
    return adj

def getXvectorsToMatrix(x, N, k, m):
    new = np.zeros((N, m, k))
    for i in range(N):
        new_x = x[i]
        new_x = np.array(new_x)
        new_x = new_x.astype(float)
        new[i,:,:] = new_x
        pass
    return new

def getReshapeMatrix(x, N, k, m):
    x_new = x.reshape(x.shape[0],-1)
    return x_new



def getClustering(g):
    return nx.clustering(g)


def getAverageShortestPathLength(g):
    return nx.average_shortest_path_length(g)

def getConnectedComponents(g):
    return nx.number_connected_components(g)

def getBetweenness(g):
    return list(nx.betweenness_centrality(g))

def getClosenness(g):
    return list(nx.closeness_centrality(g))


