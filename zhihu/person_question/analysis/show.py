

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
# # 创建一个有向图
# G = nx.DiGraph()
# # 添加一级节点
# G.add_node("A")
# # 添加二级节点
# second_level_nodes = ["B", "C", "D"]
# G.add_nodes_from(second_level_nodes)
# # 添加边，连接一级节点和二级节点
# G.add_edges_from([("A", node) for node in second_level_nodes])

# # 设置节点位置，一级节点在中间，二级节点在外围
# pos = {"A": (0, 0)}
# radius = 2  # 外围节点的半径
# theta = 2 * 3.1415926 / len(second_level_nodes)  # 角度间隔

# for i, node in enumerate(second_level_nodes):
#     x = radius * 1.5 * (i + 1) * np.cos(theta * i)
#     y = radius * 1.5 * (i + 1) * np.sin(theta * i)
#     pos[node] = (x, y)

# # 绘制图
# nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_size=8)

# # 显示图
# plt.show()


import networkx as nx
import matplotlib.pyplot as plt

# 创建一个图
G = nx.Graph()

# 添加中间节点
G.add_node(0)

theta = 2 * 3.1415926 / 6  # 角度间隔
pos = {0: (0, 0)}

radius = 5
first_nodes = []
# 添加二级节点，并与中间节点连接
for i in range(1, 7):
    x = radius * 1.5 * (i + 1) * np.cos(theta * i)
    y = radius * 1.5 * (i + 1) * np.sin(theta * i)
    pos[i] =(x,y)
    first_nodes.append(i)
    G.add_node(i)
    G.add_edge(0, i)

# second_nodes =[1] 
# # 添加三级节点，并与相应的二级节点连接
# for i in range(7, 19):
#     G.add_node(i)
#     G.add_edge(i // 3, i)

# 绘制节点分布
# pos = nx.shell_layout(G)  # 选择一种节点分布算法，这里使用shell_layout
# pos = {"A": (0, 0)}

nx.draw(G, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=10, font_color='black', font_weight='bold', edge_color='gray', linewidths=1, alpha=0.7)

# 显示图形
plt.show()
