import os 
import json
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
#新增加的两行
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = 'SimHei'
from itertools import cycle

# 用户关注关系数据

def get_data():
        
    user_file = open("analysis/todo-31-69_followees.json","r",encoding="utf-8")
    user_data = json.loads(user_file.read())

    center_data = []
    user_infos ={}
    for item in user_data.values():
        center_data.append(item["username"])
        user_infos[item["url_token"]] =item["username"]


    all_data ={}
    all_data["王信超"] =center_data

    for root,dir,file_lists in os.walk("data/"):

        for filename in file_lists:
            url_token = filename.split("_")[0]
            followees =[]

            file = open(os.path.join(root,filename),"r",encoding="utf-8")
            data = json.loads(file.read())

            for item in data.values():
                followees.append(item["username"])

            try:
                all_data[user_infos[url_token]] = followees
            except:
                pass

    return all_data

def draw_network(relationships):

    G = nx.DiGraph()
    # 添加节点和边
    for person, friends in relationships.items():
        G.add_node(person)
        G.add_edges_from((person, friend) for friend in friends)

    # 使用 spring_layout 进行布局，并调整 k 来控制节点之间的距离
    layout = nx.spring_layout(G, k=1.0)  # 调整 k 的值

    # 计算入度和出度
    in_degree = dict(G.in_degree())
    out_degree = dict(G.out_degree())

    # 为每个节点赋予一个唯一的颜色
    color_cycle = cycle(plt.cm.tab10.colors)
    node_colors = {node: next(color_cycle) for node in G.nodes()}

    # 为每个key之间的链接设置不同的颜色
    edge_colors = {key: next(color_cycle) for key in relationships.keys()}
    # 绘制图形，并根据入度和出度设置节点的大小和字体的大小
    node_size = [100 * (in_degree[node] + out_degree[node]) for node in G.nodes()]
    font_size = {node: 10 * (in_degree[node] + out_degree[node]) for node in G.nodes()}
    
    # 设置节点标签
    labels = {node: node for node in G.nodes()}
    # 绘制图形
    nx.draw(G, pos=layout, with_labels=True, labels=labels, font_weight='bold', node_size=node_size, node_color=list(node_colors.values()), font_size=8, edge_color=list(edge_colors.values()), arrows=True)

    # 显示图形
    plt.show()


def draw_relation(relationships):
   
    G = nx.DiGraph()
    # 添加节点和边
    for person, friends in relationships.items():
        G.add_node(person)
        G.add_edges_from((person, friend) for friend in friends)
    # 提取节点级别
    node_levels = nx.get_node_attributes(G, 'level')

    # 区分一级和二级节点
    level1_nodes = [node for node, level in node_levels.items() if level == 1]
    level2_nodes = [node for node, level in node_levels.items() if level == 2]

    # 创建图形布局
    pos = nx.spring_layout(G)

    color_cycle = cycle(plt.cm.tab10.colors)
    node_colors = {node for node in level1_nodes}


    # 为每个一级节点分配不同的颜色
    level1_colors = ['b', 'g', 'r']
    color_mapping = {node: level1_colors[i % len(level1_colors)] for i, node in enumerate(level1_nodes)}

    # 绘制节点
    nx.draw_networkx_nodes(G, pos, nodelist=level1_nodes, node_color=[color_mapping[node] for node in level1_nodes], node_size=500, label='Level 1')
    nx.draw_networkx_nodes(G, pos, nodelist=level2_nodes, node_color='orange', node_size=500, label='Level 2')

    # 绘制边
    nx.draw_networkx_edges(G, pos)

    # 添加标签
    nx.draw_networkx_labels(G, pos)


    plt.legend()
    plt.show()

def draw_png(data):

    G = nx.DiGraph()

    for key, values in data.items():
        G.add_node(key, level=1)
        for value in values:
            G.add_node(value, level=2)

    # Add edges between first-level and second-level nodes
    for key, values in data.items():
        for value in values:
            G.add_edge(key, value)

    in_degree = dict(G.in_degree())
    out_degree = dict(G.out_degree())

    color_cycle = cycle(plt.cm.tab10.colors)
    
    first_level_nodes = [node for node, data in G.nodes(data=True) if data['level'] == 1]
    
    node_size = [100 * (in_degree[node] + out_degree[node]) for node in G.nodes() ]
    shell_pos = nx.shell_layout(G, nlist=[first_level_nodes, G.nodes() - first_level_nodes])

    node_colors ={}
    for node in G.nodes:
        if node in first_level_nodes:
            node_colors[node] = next(color_cycle)
        else: 
            node_colors[node] = (0.12156862745098039, 0.4666666666666667, 0.7058823529411765)

    nx.draw_networkx_nodes(G, pos=shell_pos, node_size=node_size,node_color=list(node_colors.values()))
    nx.draw_networkx_nodes(G, shell_pos, nodelist=G.nodes - first_level_nodes,  node_size=10)

    color_cycle = cycle(plt.cm.tab10.colors)
    node_colors = {node: next(color_cycle) for node in first_level_nodes}
    print(node_colors)

    edge_colors = {edge: node_colors[edge[0]] for edge in G.edges()}

    print(edge_colors)
    nx.draw_networkx_edges(G, shell_pos, edge_color=list(node_colors.values()))

    labels = {node: node for node in G.nodes()}
    nx.draw_networkx_labels(G, shell_pos, labels=labels, font_size=8, font_color='black')
    plt.show()

relationships = get_data()
draw_png(relationships)
# draw_network(relationships)
# draw_relation(relationships)