#Phần cơ bản
# 1.Vẽ đồ thị trực quan , Dùng 1 đồ thị duy nhất
#download: pip install networkx matplotlib
#1.1 Nhập đồ thị
def input_graph():
    n = int(input("Nhập số cạnh: "))  #u và v là hai đỉnh của cạnh, [u, v] là một cạnh nối 2 đỉnh.
    edges = []
    for _ in range(n):
        u, v = input("Nhập cạnh (u v): ").split()
        edges.append((u, v))
    return edges
# 2 Lưu đồ thị vào file
#2.1 Lưu đồ thị vào file , ghi đè nội dung cũ vào file
def save_graph(edges, filename):
    with open(filename, 'w') as f:
        for u, v in edges:
            f.write(f"{u} {v}\n")

#2.2 Load đồ thị từ file
def load_graph(filename):
    edges = []
    with open(filename, 'r') as f:
        for line in f:
            u, v = line.strip().split()
            edges.append((u, v))
    return edges

#1. vẼ ĐỒ THỊ TRỰC QUAN
import networkx as nx
import matplotlib.pyplot as plt
def draw_graph(edges):
    G = nx.Graph()
    G.add_edges_from(edges)
    
    nx.draw(G, with_labels=True)
    plt.show()

# 4. Duyệt sơ đồ BFS và DFS
def bfs(edges, start):
    from collections import deque
    G = nx.Graph()
    G.add_edges_from(edges)
    visited = set()
    queue = deque([start])
    order = []
    
    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            order.append(node)
            for neighbor in G.neighbors(node):
                if neighbor not in visited:
                    queue.append(neighbor)
    return order

def dfs(edges, start):
    G = nx.Graph()
    G.add_edges_from(edges)
    visited = set()
    order = []
    
    def dfs_visit(node):
        visited.add(node)
        order.append(node)
        for neighbor in G.neighbors(node):
            if neighbor not in visited:
                dfs_visit(neighbor)
    dfs_visit(start)
    return order

#Main Chính
edges = []
while True:
    print("1. Nhập đồ thị")
    print("2. Lưu đồ thị vào file")
    print("3. Load đồ thị từ file")
    print("4. Vẽ đồ thị trực quan")
    print("5. Duyệt sơ đồ BFS")
    print("6. Duyệt sơ đồ DFS")
    print("7. Thoát")
    
    choice = input("Chọn một tùy chọn: ")
    
    if choice == '1':
        edges = input_graph()
        
    elif choice == '2':
        if edges:
            save_graph(edges, 'graph.txt')
            print("Đã lưu đồ thị vào file 'graph.txt'.")
        else:
            print("Chưa có đồ thị nào để lưu.")
            
    elif choice == '3':
        edges = load_graph('graph.txt')
        if edges:
            print("Đã load đồ thị từ file 'graph.txt'.")
        else:
            print("File rỗng hoặc không tồn tại.")
            
    elif choice == '4':
        if edges:
            draw_graph(edges)
        else:
            print("Chưa có đồ thị nào để vẽ.")
            
    elif choice == '5':
        if edges:
            start = input("Nhập đỉnh bắt đầu BFS: ")
            print("Kết quả BFS: ", bfs(edges, start)
        else:
            print("Chưa đồ thị nào để vẽ.")
            
    elif choice == '6':
        if edges:
            start = input("Nhập đỉnh bắt đầu DFS: ")
            print("Kết quả DFS: ",dfs(edges, start))
        else:
            print("Chưa có đồ thị nào để vẽ.")
          
    elif choice == '7':
            break
        else:
            print("Lựa chọn không hợp lệ, vui lòng thử lại.")
