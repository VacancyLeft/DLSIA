import ICLT
import RealWorldData
import utility
import sourceLocation
import networkx as nx
import random
import TestError as te
import time
import sys
import numpy as np
for count in range(20):
    g = nx.Graph()
    infected = nx.Graph()
    seed_num = 0
    seeds_predic = []
    realseeds = []
    # num = input("选择数据集（0-11）：")
    # num = int(num)
    num = 2
    if (num>=0 and num<=3):
        g = RealWorldData.readRealGraph(num)
    else:
        g = RealWorldData.readVirtualGraph(num)
    seed_num = 2
    k = 2
    # 传入模型进行感染
    g = ICLT.ICModel(g, seed_num)
    # g = ICLT.LTModel(g, seed_num)
    # g = ICLT.SIModel(g, seed_num)
    infected_nodes = ICLT.getAllActiveNodes(g)
    realseeds.extend(ICLT.getRealSeeds(g))
    if len(infected_nodes)<=2:
        print("预测源为：")
        print(realseeds)
        print("准确率：")
        print(1.0)
        print("错误距离：")
        print(0.00)
        with open('ed.txt', 'a') as f:
            f.write('0.0')
            f.write('\n')
        with open('pr.txt', 'a') as f:
            f.write('1.0')
            f.write('\n')
        continue
    # print(infected_nodes)
    # 进行观测者的选取
    O_percent = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7]
    steps = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
    a = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    o = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    gamma = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    tau = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]
    hidden = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    start = time.time()
    O_count = int(O_percent[8]*len(infected_nodes))
    Om = [0 for i in range(O_count)]
    Tm = [0 for i in range(O_count)]
    temp = random.sample(range(len(infected_nodes)), O_count)
    for j in range(O_count):
        tp = temp[j]
        Om[j] = infected_nodes[tp]
        Tm[j] = g.nodes[Om[j]]['time']
    pass
    del(temp)
    print("原始观测节点：")
    print(Om)
    print("原始观测节点时间轴：")
    print(Tm)
    length = len(Tm)
    for i in range(length-1):
        if i == length:
            break
        else:
            if Tm[i] == 0:
                seeds_predic.append(Om[i])
                O_count -= 1
                k -= 1
                Tm.pop(i)
                Om.pop(i)
                length -= 1
                if k==0:
                    print("预测源为：")
                    print(seeds_predic)
                    end = time.time()
                    print("运行时间为：%s秒" % (end - start))
                    print("准确率：")
                    print(1.0)
                    print("错误距离：")
                    print(0.00)
                    with open('ed.txt', 'a') as f:
                        f.write('0.0')
                        f.write('\n')
                    with open('pr.txt', 'a') as f:
                        f.write('1.0')
                        f.write('\n')
                    continue
                pass
            pass
        pass
    pass
    # 初始数据集处理完毕
    # print("处理后观测节点：")
    # print(Om)
    # print("处理后时间轴：")
    # print(Tm)
    infected = ICLT.getInfectedGragh(g)
    # infected = g.copy()
    seed_other = sourceLocation.sourcePredic(infected, k, Om, Tm, tau[9],a[5], o[6], steps[3], hidden[0], gamma[4])
    end = time.time()
    print("已知源：")
    print(seeds_predic)
    seeds_predic.extend(seed_other)
    print("所有预测源：")
    print(seeds_predic)
    sorted(realseeds)
    print("所有真实源：")
    print(realseeds)
    #验证效果
    accuracy = te.getAccuracy(seeds_predic, realseeds)
    error_distence = te.getErrorDistence(g, seeds_predic, realseeds)
    print("准确率：")
    print(accuracy)
    print("错误距离：")
    print(error_distence)
    print("运行时间为：%s秒"%(end-start))
    with open('ed.txt', 'a') as f:
        f.write(str(error_distence))
        f.write('\n')
    with open('pr.txt', 'a') as f:
        f.write(str(accuracy))
        f.write('\n')
pass
