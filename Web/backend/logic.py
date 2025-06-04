class Node:
    def __init__(self, name):
        self.name = name
        self.outputs = []

    def add_output(self, node):
        self.outputs.append(node)

def build_graph_and_path(start_name, end_name):
    # A60 路线
    a60_receive = Node("A60 收货区")
    a60_buffer = Node("A60 地堆存储区")
    msu_point = Node("MSU站点")
    supermarket = Node("超市1.0")
    production_line = Node("生产线")

    a60_receive.add_output(a60_buffer)
    a60_buffer.add_output(msu_point)
    msu_point.add_output(supermarket)
    msu_point.add_output(production_line)

    # A70 路线
    a70_receive = Node("A70 收货区")
    a70_repack = Node("A70 转包区")
    a70_transfer = Node("A70 转运")

    a70_receive.add_output(a70_repack)
    a70_repack.add_output(a70_transfer)

    # 三条 A70 转运分支
    bulky_store = Node("大件立体库")
    rack_buffer = Node("立体库上架缓存区")
    a70_ground_store = Node("A70 地堆存储区")

    a70_transfer.add_output(bulky_store)
    a70_transfer.add_output(rack_buffer)
    a70_transfer.add_output(a70_ground_store)

    all_nodes = [
        a60_receive, a60_buffer, msu_point, supermarket, production_line,
        a70_receive, a70_repack, a70_transfer,
        bulky_store, rack_buffer, a70_ground_store
    ]
    name_to_node = {node.name: node for node in all_nodes}

    path = []
    visited = set()

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
