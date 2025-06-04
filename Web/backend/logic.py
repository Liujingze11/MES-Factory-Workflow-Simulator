# logic.py
class Node:
    def __init__(self, name):
        self.name = name
        self.outputs = []

    def add_output(self, node):
        self.outputs.append(node)

def build_graph_and_path(start_name, end_name):
    # 构造节点
    a60_receive = Node("A60 收货区")
    a60_buffer = Node("A60 地堆存储区")
    msu_point = Node("MSU站点")
    supermarket = Node("超市1.0")
    production_line = Node("生产线")

    # 建立有向边
    a60_receive.add_output(a60_buffer)
    a60_buffer.add_output(msu_point)
    msu_point.add_output(supermarket)
    msu_point.add_output(production_line)

    all_nodes = [a60_receive, a60_buffer, msu_point, supermarket, production_line]
    name_to_node = {node.name: node for node in all_nodes}

    path = []
    visited = set()

    # 深度优先搜索，记录路径
    def dfs(node):
        if node.name in visited:
            return False
        visited.add(node.name)
        path.append(node.name)
        if node.name == end_name:
            return True
        for nxt in node.outputs:
            if dfs(nxt):
                return True
        path.pop()
        return False

    start_node = name_to_node.get(start_name)
    if start_node and dfs(start_node):
        return path
    else:
        return None
