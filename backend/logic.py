class Node:
    def __init__(self, name):
        self.name = name
        self.outputs = []  # 存储该节点的所有下游节点

    def add_output(self, node):
        """添加下游节点"""
        self.outputs.append(node)


def build_graph_and_paths(start_name, end_name):
    """
    构建工厂流程图并查找所有从起点到终点的路径（支持分叉）
    :param start_name: 起点节点名称
    :param end_name: 终点节点名称
    :return: 所有路径列表，形如 [["A", "B", "C"], ["A", "D", "C"]]
    """

    # ==================== 构建A60路线 ====================
    a60_receive = Node("A60 收货区")
    a60_buffer = Node("A60 地堆存储区")
    msu_point = Node("MSU站点")
    supermarket = Node("超市1.0")
    production_line = Node("生产线")

    a60_receive.add_output(a60_buffer)
    a60_buffer.add_output(msu_point)
    msu_point.add_output(supermarket)
    msu_point.add_output(production_line)
    supermarket.add_output(production_line)

    # ==================== 构建A70路线 ====================
    a70_receive = Node("A70 收货区")
    a70_repack = Node("A70 转包区")
    a70_transfer = Node("A70 转运")

    a70_receive.add_output(a70_repack)
    a70_repack.add_output(a70_transfer)

    # ==================== A70转运的分支 ====================
    bulky_store = Node("大件立体库")
    rack_buffer = Node("立体库上架缓存区")
    a70_ground_store = Node("A70 地堆存储区")

    trash_station = Node("小件垃圾处理站")
    unpack_station = Node("小件拆垛站")
    exception_station = Node("小件入库异常处理站")
    small_store = Node("小件立体库")

        # 新增后续流程节点
    small_stock = Node("小件备货站")
    small_out_exception = Node("小件出库异常处理站")
    small_station = Node("小件站点")
    supermarket2 = Node("超市2.0")  # 超市2.0

    bulky_buffer = Node("大件备货站")
    bulky_station = Node("大件站点")
    skl_area = Node("SKLTOVERSIZE货区") 


    small_store.add_output(small_stock)
    small_store.add_output(small_out_exception)
    small_stock.add_output(small_station)
    small_station.add_output(supermarket)
    small_out_exception.add_output(small_stock)


    a70_transfer.add_output(bulky_store)
    a70_transfer.add_output(rack_buffer)
    a70_transfer.add_output(a70_ground_store)

    rack_buffer.add_output(trash_station)
    trash_station.add_output(unpack_station)
    unpack_station.add_output(exception_station)
    exception_station.add_output(small_store)

    a70_ground_store.add_output(supermarket2)        # A70 地堆存储区 → 超市2.0
    small_station.add_output(supermarket2)           # 小件站点 → 超市2.0
    supermarket2.add_output(production_line)         # 超市2.0 → 生产线

    small_store.add_output(small_station)  # 小件立体库 → 小件站点
    small_store.add_output(small_out_exception)  # 小件立体库 → 小件出库异常处理站
    small_out_exception.add_output(small_stock)  # 小件出库异常处理站 → 小件备货站（闭环）

    bulky_store.add_output(bulky_buffer)
    bulky_buffer.add_output(bulky_station)
    bulky_station.add_output(skl_area)
    skl_area.add_output(production_line)

    bulky_station.add_output(supermarket)
    bulky_station.add_output(supermarket2)

    a70_ground_store.add_output(bulky_buffer)
    a70_ground_store.add_output(skl_area)

    # ==================== 所有节点集合 ====================
    all_nodes = [
        a60_receive, a60_buffer, msu_point, supermarket, production_line,
        a70_receive, a70_repack, a70_transfer,
        bulky_store, rack_buffer, a70_ground_store,
        trash_station, unpack_station, exception_station, small_store,
        small_stock, small_out_exception, small_station,supermarket2,
        bulky_buffer, bulky_station, skl_area
    ]

    name_to_node = {node.name: node for node in all_nodes}
    all_paths = []

    def dfs(node, path):
        path.append(node.name)
        if node.name == end_name:
            all_paths.append(path[:])  # 保存一条完整路径
        else:
            for nxt in node.outputs:
                dfs(nxt, path)
        path.pop()  # 回溯

    start_node = name_to_node.get(start_name)
    if start_node:
        dfs(start_node, [])

    return all_paths if all_paths else None
