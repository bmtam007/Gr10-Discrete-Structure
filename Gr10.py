#Phần cơ bản
#download: pip install networkx matplotlib
import heapq
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt
# CẤU TRÚC DỮ LIỆU CHUNG
# edges   : list[(u, v, weight)]   – danh sách cạnh (có trọng số)
# directed: bool                   – Cố định False = đồ thị VÔ HƯỚNG


edges    = []        # [(u, v, weight), ...]
directed = False     # CỐ ĐỊNH: đồ thị vô hướng


#1 VẼ ĐỒ THỊ TRỰC QUAN
#1.1 Nhập đồ thị từ người dùng
def input_graph():
    """Nhập đồ thị vô hướng từ bàn phím (hỗ trợ trọng số tuỳ chọn)."""
    n = int(input("Nhập số cạnh: "))
    new_edges = []
    for _ in range(n):
        raw = input("Nhập cạnh (u v [trọng_số]): ").split()
        u, v = raw[0], raw[1]
        w = float(raw[2]) if len(raw) >= 3 else 1.0   # mặc định trọng số = 1
        new_edges.append((u, v, w))
    return new_edges
 
 
def build_nx_graph(edges, directed):
    """Tạo đối tượng NetworkX từ danh sách cạnh."""
    G = nx.DiGraph() if directed else nx.Graph()
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)
    return G
 
#1.2 Vẽ đồ thị trực quan 
def draw_graph(edges, directed):
    """Vẽ đồ thị trực quan với nhãn trọng số."""
    if not edges:
        print("Chưa có đồ thị nào để vẽ.")
        return
 
    G   = build_nx_graph(edges, directed)
    pos = nx.spring_layout(G, seed=42)   # seed=42 → vị trí cố định
 
    edge_labels = {(u, v): f"{d['weight']:.0f}" for u, v, d in G.edges(data=True)}
 
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color='skyblue',
            node_size=700, font_size=12, arrows=directed,
            arrowsize=20, width=2)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
    title = "Đồ thị có hướng" if directed else "Đồ thị vô hướng"
    plt.title(title)
    plt.tight_layout()
    plt.show()


#2 LƯU VÀ TẢI ĐỒ THỊ
FILENAME = "graph.txt"
 
 
def save_graph(edges, directed):
    """Lưu đồ thị vào file (ghi đè)."""
    with open(FILENAME, 'w') as f:
        f.write(f"directed={'yes' if directed else 'no'}\n")
        for u, v, w in edges:
            f.write(f"{u} {v} {w}\n")
    print(f"✔ Đã lưu đồ thị vào '{FILENAME}'.")
 

def load_graph():
    """Tải đồ thị từ file."""
    global directed
    loaded_edges = []
    try:
        with open(FILENAME, 'r') as f:
            lines = f.readlines()
 
        # Dòng đầu: directed=yes/no
        first = lines[0].strip()
        directed = first.split('=')[1] == 'yes' if first.startswith('directed') else False
        start = 1 if first.startswith('directed') else 0
 
        for line in lines[start:]:
            parts = line.strip().split()
            if len(parts) >= 2:
                u, v = parts[0], parts[1]
                w = float(parts[2]) if len(parts) >= 3 else 1.0
                loaded_edges.append((u, v, w))
 
        print(f"✔ Đã tải đồ thị từ '{FILENAME}'.")
    except FileNotFoundError:
        print(f"✘ File '{FILENAME}' không tồn tại.")
    return loaded_edges



#3 TÌM ĐƯỜNG ĐI NGẮN NHẤT (DIJKSTRA)
def build_adj(edges, directed):
    """Xây dựng danh sách kề từ danh sách cạnh."""
    graph = {}
    for u, v, w in edges:
        if u not in graph: graph[u] = []
        if v not in graph: graph[v] = []
        graph[u].append((v, w))
        if not directed:
            graph[v].append((u, w))
    return graph
 
 
def dijkstra(graph, start):
    """
    Thuật toán Dijkstra – tìm khoảng cách ngắn nhất từ đỉnh start đến mọi đỉnh.
    graph : {đỉnh: [(đỉnh_kề, trọng_số), ...]}
    Trả về: (dist, prev)
        dist : {đỉnh: khoảng_cách_nhỏ_nhất}
        prev : {đỉnh: đỉnh_trước} – dùng để truy vết đường đi
    """
    dist = {node: float('inf') for node in graph}
    prev = {node: None for node in graph}
    dist[start] = 0
 
    pq = [(0, start)]   # (khoảng cách hiện tại, đỉnh)
 
    while pq:
        current_dist, u = heapq.heappop(pq)
 
        # Bỏ qua nếu đã tìm được đường ngắn hơn trước đó
        if current_dist > dist[u]:
            continue
 
        for v, weight in graph[u]:
            new_dist = current_dist + weight
            if new_dist < dist[v]:
                dist[v] = new_dist
                prev[v] = u
                heapq.heappush(pq, (new_dist, v))
 
    return dist, prev
 
 
def reconstruct_path(prev, start, end):
    """Truy vết đường đi từ start đến end."""
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = prev[current]
    path.reverse()
    # Kiểm tra đường đi hợp lệ
    if path[0] == start:
        return path
    return []
 
 
def shortest_path_menu(edges, directed):
    """Giao diện con cho phần tìm đường đi ngắn nhất."""
    if not edges:
        print("Chưa có đồ thị. Hãy nhập hoặc tải đồ thị trước.")
        return
 
    graph = build_adj(edges, directed)
    all_nodes = list(graph.keys())
    print(f"Các đỉnh hiện có: {', '.join(sorted(all_nodes))}")
 
    start = input("Nhập đỉnh bắt đầu: ").strip()
    end   = input("Nhập đỉnh kết thúc (để trống = in tất cả): ").strip()
 
    if start not in graph:
        print(f"✘ Đỉnh '{start}' không tồn tại trong đồ thị.")
        return
 
    dist, prev = dijkstra(graph, start)
 
    if end == "":
        # In khoảng cách từ start đến mọi đỉnh
        print(f"\nKhoảng cách ngắn nhất từ '{start}':")
        for node in sorted(dist):
            d = dist[node]
            if d == float('inf'):
                print(f"  {start} → {node} : Không có đường đi")
            else:
                path = reconstruct_path(prev, start, node)
                path_str = " → ".join(path)
                print(f"  {start} → {node} : {d:.1f}   [{path_str}]")
    else:
        if end not in graph:
            print(f"✘ Đỉnh '{end}' không tồn tại trong đồ thị.")
            return
        d = dist[end]
        if d == float('inf'):
            print(f"Không có đường đi từ '{start}' đến '{end}'.")
        else:
            path = reconstruct_path(prev, start, end)
            path_str = " → ".join(path)
            print(f"\n✔ Đường đi ngắn nhất: {path_str}")
            print(f"   Tổng trọng số     : {d:.1f}")
 
    # Vẽ đồ thị và tô màu đường đi ngắn nhất (nếu có đỉnh đích cụ thể)
    if end and end in graph and dist[end] != float('inf'):
        highlight_path(edges, directed, reconstruct_path(prev, start, end))
 
 
def highlight_path(edges, directed, path):
    """Vẽ đồ thị và tô màu đường đi ngắn nhất."""
    G   = build_nx_graph(edges, directed)
    pos = nx.spring_layout(G, seed=42)
 
    path_edges = list(zip(path[:-1], path[1:]))
 
    node_colors = ['#FF6B6B' if n in path else 'skyblue' for n in G.nodes()]
    edge_colors = []
    for u, v in G.edges():
        if (u, v) in path_edges or (not directed and (v, u) in path_edges):
            edge_colors.append('#FF6B6B')
        else:
            edge_colors.append('#AAAAAA')
 
    edge_labels = {(u, v): f"{d['weight']:.0f}" for u, v, d in G.edges(data=True)}
 
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color=node_colors,
            edge_color=edge_colors, node_size=700, font_size=12,
            arrows=directed, arrowsize=20, width=2)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
    plt.title("Đường đi ngắn nhất (màu đỏ)")
    plt.tight_layout()
    plt.show()



#4. DUYỆT ĐỒ THỊ (BFS / DFS)
def bfs(edges, directed, start):
    """
    Duyệt đồ thị theo chiều rộng (Breadth-First Search).
    Dùng hàng đợi (deque): lấy từ đầu, thêm vào cuối.
    Trả về: (order, parent)
        order  : thứ tự duyệt
        parent : {đỉnh: đỉnh_cha} – dùng để vẽ cây BFS
    """
    G = build_nx_graph(edges, directed)
    if start not in G.nodes():
        print(f"✘ Đỉnh '{start}' không tồn tại trong đồ thị.")
        return [], {}
 
    visited = set()
    queue   = deque([start])
    order   = []
    parent  = {start: None}
 
    while queue:
        node = queue.popleft()          # lấy phần tử đầu hàng đợi
        if node not in visited:
            visited.add(node)
            order.append(node)
            for neighbor in sorted(G.neighbors(node)):   # sorted → thứ tự cố định
                if neighbor not in visited and neighbor not in parent:
                    parent[neighbor] = node
                    queue.append(neighbor)
    return order, parent
 
 
def dfs(edges, directed, start):
    """
    Duyệt đồ thị theo chiều sâu (Depth-First Search).
    Dùng đệ quy (call stack).
    Trả về: (order, parent)
        order  : thứ tự duyệt
        parent : {đỉnh: đỉnh_cha} – dùng để vẽ cây DFS
    """
    G = build_nx_graph(edges, directed)
    if start not in G.nodes():
        print(f"✘ Đỉnh '{start}' không tồn tại trong đồ thị.")
        return [], {}
 
    visited = set()
    order   = []
    parent  = {start: None}
 
    def dfs_visit(node):
        visited.add(node)
        order.append(node)
        for neighbor in sorted(G.neighbors(node)):
            if neighbor not in visited:
                parent[neighbor] = node
                dfs_visit(neighbor)
 
    dfs_visit(start)
    return order, parent
 
 
def draw_traversal(edges, directed, order, parent, title):
    """Vẽ đồ thị và làm nổi bật thứ tự duyệt + cây duyệt."""
    G   = build_nx_graph(edges, directed)
    pos = nx.spring_layout(G, seed=42)
 
    # Cạnh thuộc cây duyệt (tree edges)
    tree_edges = [(parent[v], v) for v in parent if parent[v] is not None]
 
    # Màu đỉnh: gradient theo thứ tự duyệt
    cmap       = plt.cm.YlOrRd
    color_map  = {}
    for i, node in enumerate(order):
        color_map[node] = cmap(0.2 + 0.7 * i / max(len(order) - 1, 1))
    node_colors = [color_map.get(n, (0.7, 0.9, 1.0, 1.0)) for n in G.nodes()]
 
    # Màu cạnh
    edge_colors = []
    for u, v in G.edges():
        if (u, v) in tree_edges or (not directed and (v, u) in tree_edges):
            edge_colors.append('#E74C3C')   # đỏ = cạnh cây
        else:
            edge_colors.append('#CCCCCC')   # xám = cạnh còn lại
 
    # Nhãn số thứ tự duyệt
    labels = {n: f"{n}\n(#{order.index(n)+1})" if n in order else n for n in G.nodes()}
 
    plt.figure(figsize=(9, 6))
    nx.draw(G, pos, labels=labels, node_color=node_colors,
            edge_color=edge_colors, node_size=900, font_size=9,
            arrows=directed, arrowsize=20, width=2)
    edge_labels = {(u, v): f"{d['weight']:.0f}" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)
    plt.title(f"{title}\nThứ tự: {' → '.join(order)}")
    plt.tight_layout()
    plt.show()
 
 
def traversal_menu(edges, directed):
    """Giao diện con cho phần duyệt đồ thị."""
    if not edges:
        print("Chưa có đồ thị. Hãy nhập hoặc tải đồ thị trước.")
        return
 
    G = build_nx_graph(edges, directed)
    print(f"Các đỉnh hiện có: {', '.join(sorted(G.nodes()))}")
    start = input("Nhập đỉnh bắt đầu duyệt: ").strip()
 
    print("\n  a. BFS (duyệt theo chiều rộng)")
    print("  b. DFS (duyệt theo chiều sâu)")
    print("  c. Cả hai")
    sub = input("Chọn: ").strip().lower()
 
    if sub in ('a', 'c'):
        order, parent = bfs(edges, directed, start)
        if order:
            print(f"\n✔ BFS từ '{start}': {' → '.join(order)}")
            draw_traversal(edges, directed, order, parent, f"BFS từ đỉnh '{start}'")
 
    if sub in ('b', 'c'):
        order, parent = dfs(edges, directed, start)
        if order:
            print(f"\n✔ DFS từ '{start}': {' → '.join(order)}")
            draw_traversal(edges, directed, order, parent, f"DFS từ đỉnh '{start}'")
 
    if sub not in ('a', 'b', 'c'):
        print("Lựa chọn không hợp lệ.")

#5. KIỂM TRA 1 ĐỒ THỊ CÓ PHẢI LÀ 2 PHÍA HAY KHÔNG?
def is_bipartite(edges):
    # Kiểm tra đồ thị có phải là đồ thị 2 phía không.
    #- Nếu 2 đỉnh kề nhau cùng màu → KHÔNG phải 2 phía
    #- Tô màu xong hết mà không xung đột → LÀ đồ thị 2 phía
    #Lưu ý: dùng đỉnh dạng chuỗi ("A","B",...) thay vì số nguyên
    # Xây dựng danh sách kề (vô hướng, không cần trọng số)
    graph = {}
    for u, v, w in edges:
        if u not in graph: graph[u] = []
        if v not in graph: graph[v] = []
        graph[u].append(v)
        graph[v].append(u)   # vô hướng → thêm cả 2 chiều
 
    color = {}   # {đỉnh: 0 hoặc 1} – thay mảng color[] trong demo
 
    for start in graph:
        if start not in color:          # chưa tô màu → bắt đầu BFS từ đây
            queue = deque([start])
            color[start] = 0
 
            while queue:
                u = queue.popleft()
                for v in graph[u]:
                    if v not in color:              # chưa tô → tô màu ngược
                        color[v] = 1 - color[u]
                        queue.append(v)
                    elif color[v] == color[u]:      # cùng màu → xung đột!
                        return False, color, graph
 
    return True, color, graph
 
 
def draw_bipartite(edges, color):
    """Vẽ đồ thị và tô 2 màu cho 2 tập đỉnh."""
    G  = build_nx_graph(edges, directed)
    pos = nx.spring_layout(G, seed=42)
 
    # Tập A (màu 0 → xanh dương), Tập B (màu 1 → cam)
    node_colors = ['#3498DB' if color.get(n) == 0 else '#E67E22' for n in G.nodes()]
 
    edge_labels = {(u, v): f"{d['weight']:.0f}" for u, v, d in G.edges(data=True)}
 
    # Tạo nhãn kèm tên tập
    set_A = sorted([n for n in color if color[n] == 0])
    set_B = sorted([n for n in color if color[n] == 1])
 
    plt.figure(figsize=(9, 6))
    nx.draw(G, pos, with_labels=True, node_color=node_colors,
            node_size=800, font_size=12, font_color='white',
            width=2, edge_color='#888888')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
    plt.title(
        f"Đồ thị 2 phía ✔\n"
        f"Tập A (xanh): {{{', '.join(set_A)}}}    "
        f"Tập B (cam): {{{', '.join(set_B)}}}"
    )
    plt.tight_layout()
    plt.show()
 
 
def bipartite_menu(edges):
    """Giao diện con cho phần kiểm tra đồ thị 2 phía."""
    if not edges:
        print("Chưa có đồ thị. Hãy nhập hoặc tải đồ thị trước.")
        return
 
    result, color, graph = is_bipartite(edges)
 
    if result:
        set_A = sorted([n for n in color if color[n] == 0])
        set_B = sorted([n for n in color if color[n] == 1])
        print("\n✔ Đây LÀ đồ thị 2 phía!")
        print(f"   Tập A: {{{', '.join(set_A)}}}")
        print(f"   Tập B: {{{', '.join(set_B)}}}")
        draw_bipartite(edges, color)
    else:
        print("\n✘ Đây KHÔNG phải đồ thị 2 phía!")
        print("   (Tồn tại cạnh nối 2 đỉnh cùng tập)")



#Main Chính
def main():
    global edges, directed
 
    while True:
        print(f"\n{'='*45}")
        print(f"   ĐỒ THỊ VÔ HƯỚNG – {len(edges)} cạnh")
        print(f"{'='*45}")
        print("  1. Nhập đồ thị mới")
        print("  2. Lưu đồ thị vào file")
        print("  3. Tải đồ thị từ file")
        print("  4. Vẽ đồ thị trực quan")
        print("  5. Tìm đường đi ngắn nhất (Dijkstra)")
        print("  6. Duyệt đồ thị (BFS / DFS)")
        print("  7. Kiểm tra đồ thị 2 phía")
        print("  0. Thoát")
        print(f"{'='*45}")
 
        choice = input("Chọn: ").strip()
 
        if choice == '1':
            edges    = input_graph()
            print(f"✔ Đã nhập {len(edges)} cạnh.")
 
        elif choice == '2':
            if edges:
                save_graph(edges, directed)
            else:
                print("Chưa có đồ thị nào để lưu.")
 
        elif choice == '3':
            loaded = load_graph()
            if loaded:
                edges = loaded
 
        elif choice == '4':
            draw_graph(edges, directed)
 
        elif choice == '5':
            shortest_path_menu(edges, directed)
 
        elif choice == '6':
            traversal_menu(edges, directed)
 
        elif choice == '7':
            bipartite_menu(edges)
 
        elif choice == '0':
            print("Tạm biệt!")
            break
        else:
            print("Lựa chọn không hợp lệ, thử lại.")
 
 
if __name__ == "__main__":
    main()
