import networkx as nx
import matplotlib.pyplot as plt

# 创建一个图
G = nx.Graph()

# 添加边，形成聚类
edges = [(1, 2), (1, 3), (2, 3), (4, 5), (6, 7)]
G.add_edges_from(edges)

# 找到连接关系的聚类
clusters = list(nx.connected_components(G))

# 绘制节点分布
pos = nx.spring_layout(G)  # 选择一种节点分布算法，这里使用spring_layout

# 绘制每个聚类
for i, cluster in enumerate(clusters):
    nx.draw_networkx_nodes(G, pos, nodelist=list(cluster), node_color=f'C{i+1}', label=f'Cluster {i+1}')

nx.draw_networkx_edges(G, pos)
nx.draw_networkx_labels(G, pos)

plt.legend()
plt.show()
