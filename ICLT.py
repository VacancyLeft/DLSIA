import random
import utility
import numpy as np
import networkx as nx

def ICModel(g, seed_num):
    spread = 500
    icg = g.copy()
    N = utility.getNodesNumber(icg)
    adj = utility.getAdjMartrix(icg)
    prob = np.empty([N, N], dtype=float)
    degreeM = utility.getDegreeMartrix(icg)
    degree = utility.getDegreeList(icg)
    infected_graph = nx.Graph()
    # print(icg.degree())
    for node in icg:
        icg.add_node(node, state = 0)
        icg.add_node(node, time = -1)
    # 为边赋权重
    # 需要优化：
    # for i in range(0, N-1):
    #     for j in range(0, N-1):
    #         if adj[i][j] == 1:
    #             if degree[i] >= degree[j]:
    #                 prob[i][j] = float(1/degree[i])
    #                 icg.add_edge(i, j, weight=prob[i][j])
    #             else:
    #                 prob[i][j] = float(1 / degree[j])
    #                 icg.add_edge(i, j, weight=prob[i][j])
    #         else:
    #             icg.add_edge(i, j, weight=1)
    # print("节点权重矩阵为："+ prob)
    for edge in icg.edges:
        icg.add_edge(edge[0], edge[1], weight = random.uniform(0,1))
    seeds = random.sample(range(N), seed_num)
    seeds_sort = sorted(seeds).copy()
    print(seeds_sort)
    # # 找到图中度最多的前seed_num个节点
    # seeds_sec = [0 for i in range(seed_num)]
    # for i in range(seed_num):
    #     temp = int(degree.index(max(degree)))
    #     # print(icg.degree(temp))
    #     seeds_sec[i] = temp
    #     degree[temp] = 0
    # print(seeds_sec)
    # # seeds = seeds_sec
    print(seeds)
    for i in range(seed_num):
        icg.add_node(seeds[i], state=1)
        icg.add_node(seeds[i], time=0)
        infected_graph.add_node(seeds[i], time=0, state=1)
    # 存储活跃节点
    all_active_nodes = seeds.copy()
    start_nodes = seeds.copy()
    for i in range(1, spread+1):
        count = len(all_active_nodes)
        if count >= N * 0.25:
            break
        new_active_nodes = list()
        for v in start_nodes:
            for nbr in icg.neighbors(v):
                if icg.nodes[nbr]['state'] == 0:
                    edge_data = icg.get_edge_data(v, nbr)
                    temp = edge_data['weight']
                    if random.uniform(0,1) < temp:
                        icg.add_node(nbr, state=1)
                        icg.add_node(nbr, time=i)
                        new_active_nodes.append(nbr)
                        # infected_graph.add_node(nbr, time=0, state=1)
                        # infected_graph.add_edge(v, nbr)
        start_nodes.clear()
        start_nodes.extend(new_active_nodes)
        all_active_nodes.extend(new_active_nodes)
        # result = '第%s次'%i + '激活%s个节点' %len(new_active_nodes)
        # print(result)
    result = '总计%s个节点被激活' %len(all_active_nodes)
    print(result)
    return icg

def LTModel(g, seed_num):
    spread = 500
    icg = g.copy()
    N = utility.getNodesNumber(icg)
    adj = utility.getAdjMartrix(icg)
    prob = np.empty([N, N], dtype=float)
    degreeM = utility.getDegreeMartrix(icg)
    degree = utility.getDegreeList(icg)
    threashould=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
    # print(icg.degree())
    for node in icg:
        icg.add_node(node, state=0)
        icg.add_node(node, time=-1)
    # 为边赋权重
    # 需要优化：
    # for i in range(0, N-1):
    #     for j in range(0, N-1):
    #         if adj[i][j] == 1:
    #             if degree[i] >= degree[j]:
    #                 prob[i][j] = float(1/degree[i])
    #                 icg.add_edge(i, j, weight=prob[i][j])
    #             else:
    #                 prob[i][j] = float(1 / degree[j])
    #                 icg.add_edge(i, j, weight=prob[i][j])
    #         else:
    #             icg.add_edge(i, j, weight=1)
    # print("节点权重矩阵为："+ prob)
    for edge in icg.edges:
        icg.add_edge(edge[0], edge[1], weight=random.uniform(0, 1))
    seeds = random.sample(range(N), seed_num)
    seeds_sort = sorted(seeds).copy()
    print(seeds_sort)
    # 找到图中度最多的前seed_num个节点
    seeds_sec = [0 for i in range(seed_num)]
    for i in range(seed_num):
        temp = int(degree.index(max(degree)))
        # print(icg.degree(temp))
        seeds_sec[i] = temp
        degree[temp] = 0
    print(seeds_sec)
    # seeds = seeds_sec
    print(seeds)
    for i in range(seed_num):
        icg.add_node(seeds[i], state=1)
        icg.add_node(seeds[i], time=0)
    # 存储活跃节点
    all_active_nodes = seeds.copy()
    start_nodes = seeds.copy()
    # infected_graph = nx.Graph()
    # infected_graph.add_node(seeds)
    for i in range(1, spread + 1):
        count = len(all_active_nodes)
        if count >= N * 0.25:
            break
        new_active_nodes = list()
        for v in icg:
            if icg.nodes[v]['state']==1:
                continue
            else:
                sum = 0
                nbr_list = []
                temp_list = []
            for nbr in list(nx.neighbors(icg,v)):
                nbr_list.append(nbr)
            for nbr in icg.neighbors(v):
                if icg.nodes[nbr]['state'] == 1:
                    edge_data = icg.get_edge_data(v, nbr)
                    temp = edge_data['weight']
                    temp_list.append(nbr)
                    sum = sum + temp
                    if threashould[7] < sum and len(temp_list)<=len(nbr_list):
                        icg.add_node(v, state=1)
                        icg.add_node(v, time=i)
                        new_active_nodes.append(v)
                        break
                        # infected_graph.add_node(temp_list[j], state=1, time=i)
                        # infected_graph.add_edge(v, temp_list[j])
                    else:
                        continue
        start_nodes.extend(new_active_nodes)
        all_active_nodes.extend(new_active_nodes)
        # result = '第%s次'%i + '激活%s个节点' %len(new_active_nodes)
        # print(result)
    result = '总计%s个节点被激活' % len(all_active_nodes)
    print(result)
    with open('SI.txt', 'a') as f:
        f.write("本次感染节点：")
        f.write('\n')
        f.write(str(all_active_nodes))
    return icg

def SIModel(g, seed_num):
    spread = 1500
    icg = g.copy()
    N = utility.getNodesNumber(icg)
    adj = utility.getAdjMartrix(icg)
    prob = np.empty([N, N], dtype=float)
    degreeM = utility.getDegreeMartrix(icg)
    degree = utility.getDegreeList(icg)
    beta=[0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7]
    for edge in icg.edges:
        icg.add_edge(edge[0], edge[1], weight=random.uniform(0, 0.6))  # 可不可以作为权值 病毒的感染能力
    for node in icg:
        icg.add_node(node, state=0)
        icg.add_node(node, time=0)
    seeds = random.sample(range(N), seed_num)
    seeds_sort = sorted(seeds).copy()
    print(seeds_sort)
    # # 找到图中度最多的前seed_num个节点
    # seeds_sec = [0 for i in range(seed_num)]
    # for i in range(seed_num):
    #     temp = int(degree.index(max(degree)))
    #     # print(icg.degree(temp))
    #     seeds_sec[i] = temp
    #     degree[temp] = 0
    # print(seeds_sec)
    # # seeds = seeds_sec
    print(seeds)
    for i in range(seed_num):
        icg.add_node(seeds[i], state=1)
        icg.add_node(seeds[i], time=0)
    all_infect_nodes = []
    all_infect_nodes.append(seeds)
    # infected_graph = nx.Graph()
    # infected_graph.add_node(seeds)
    for i in range(1, spread+1):
        count = len(all_infect_nodes)
        if count >= N * 0.25:
            break
        new_infect = list()
        # 感染的机会不止一次
        for v in icg:
            if icg.nodes[v]['state'] == 1:
                for nbr in icg.neighbors(v):
                    if icg.nodes[nbr]['state'] == 0:
                        edge_data = icg.get_edge_data(v, nbr)
                        if beta[2] < edge_data['weight']:
                            icg.nodes[nbr]['state'] = 1
                            icg.add_node(nbr, time=i)
                            new_infect.append(nbr)
                            pass
                        pass
                    pass
                else:
                    continue
                pass
            else:
                continue
            pass
        all_infect_nodes.extend(new_infect)
    with open('SI.txt', 'a') as f:
        f.write("本次感染节点：")
        f.write('\n')
        f.write(str(all_infect_nodes))
    return icg

def getAllActiveNodes(g):
    allnodes = []
    for v in g.nodes:
        if g.nodes[v]['state'] == 1:
            allnodes.append(v)
    return allnodes

def getRealSeeds(g):
    seeds = []
    infected = getAllActiveNodes(g)
    for v in infected:
        if g.nodes[v]['state'] == 1 and g.nodes[v]['time'] == 0:
            seeds.append(v)
    return seeds

def getInfectedGragh(g):
    infected = nx.Graph()
    for node in g.nodes:
        if g.nodes[node]['state'] == 1:
            infected.add_node(node, state = 1)
            for v in g.neighbors(node):
                if g.nodes[v]['state'] == 1:
                    wght = g.edges[node, v]['weight']
                    infected.add_edge(node, v, weight = wght)
        else:
            continue
    return infected

