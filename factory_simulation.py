import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# ✅ 设置支持中文字体（适用于 macOS）
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['Heiti SC', 'PingFang SC', 'STHeiti']
matplotlib.rcParams['axes.unicode_minus'] = False

# ------------ 基础建模类 ------------

class Material:
    def __init__(self, material_id):
        self.id = material_id

    def __str__(self):
        return f"物料[{self.id}]"

class Node:
    def __init__(self, name):
        self.name = name
        self.outputs = []

    def add_output(self, node):
        self.outputs.append(node)

    def get_outputs(self):
        return self.outputs

# ------------ 建图结构 ------------

# 定义节点
a60_receive = Node("A60 收货区")
a60_buffer = Node("A60 地堆存储区")
msu_point = Node("MSU站点")

# a70_buffer = Node("A70 缓存区")
# big_sort_point = Node("大件分拣点")
# sklt_oversize = Node("SKLT Oversize")
# big_temp_storage = Node("大件临时缓存位")

# 连接关系
a60_receive.add_output(a60_buffer)
a60_buffer.add_output(msu_point)
# msu_point.add_output(a60_buffer)  # 可选：形成闭环
# a60_buffer.add_output(a70_buffer)
# a70_buffer.add_output(big_sort_point)
# big_sort_point.add_output(sklt_oversize)
# sklt_oversize.add_output(big_temp_storage)

# 构建图结构
# all_nodes = [
#     a60_receive, a60_buffer, msu_point,
#     a70_buffer, big_sort_point, sklt_oversize, big_temp_storage
# ]
all_nodes = [
    a60_receive, a60_buffer, msu_point
]

G = nx.DiGraph()
for node in all_nodes:
    G.add_node(node.name)
    for out in node.get_outputs():
        G.add_edge(node.name, out.name)


# 自定义节点位置（横向排列）
pos = {
    "A60 收货区": (0, 0),
    "A60 地堆存储区": (1, 0),
    "MSU站点": (2, 0)
}


# ------------ 控制器类：按钮控制 + 保留箭头线 ------------

class FlowController:
    def __init__(self, path):
        self.path = path
        self.index = 0
        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(bottom=0.2)
        self.dot, = self.ax.plot([], [], 'ro', markersize=15)

        self.draw_graph()

        # 按钮区域
        axprev = plt.axes([0.25, 0.05, 0.1, 0.075])
        axnext = plt.axes([0.65, 0.05, 0.1, 0.075])
        self.bnext = Button(axnext, '下一步 ➡️')
        self.bprev = Button(axprev, '⬅️ 上一步')
        self.bnext.on_clicked(self.next_step)
        self.bprev.on_clicked(self.prev_step)

        self.update_dot()
        plt.show()

    def draw_graph(self):
        self.ax.clear()
        nx.draw_networkx_nodes(
            G, pos, ax=self.ax, node_shape='s',
            node_size=3000, node_color="lightblue"
        )
        nx.draw_networkx_labels(G, pos, ax=self.ax, font_size=10)
        nx.draw_networkx_edges(
            G, pos, ax=self.ax, edgelist=G.edges(),
            arrows=True, arrowstyle='-|>', arrowsize=20
        )

    def update_dot(self):
        name = self.path[self.index]
        x, y = pos[name]
        self.dot.set_data([x], [y])
        self.ax.plot(x, y, 'ro', markersize=15)
        self.ax.set_title(f"当前位置：{name}")
        self.fig.canvas.draw_idle()

    def next_step(self, event):
        if self.index < len(self.path) - 1:
            self.index += 1
            self.draw_graph()
            self.update_dot()

    def prev_step(self, event):
        if self.index > 0:
            self.index -= 1
            self.draw_graph()
            self.update_dot()

# ------------ 路径查找与模拟 ------------

def simulate(material: Material, start_node: Node, end_node_name: str):
    path = []
    visited = set()

    def dfs(current_node):
        if current_node.name in visited:
            return False
        visited.add(current_node.name)
        path.append(current_node.name)
        if current_node.name == end_node_name:
            return True
        for next_node in current_node.get_outputs():
            if dfs(next_node):
                return True
        path.pop()
        return False

    if dfs(start_node):
        print(f"{material} 路径：", " → ".join(path))
        FlowController(path)
    else:
        print("未找到路径")

# ------------ 启动主程序 ------------

if __name__ == "__main__":
    material1 = Material("L001")
    simulate(material1, a60_receive, "MSU站点")
