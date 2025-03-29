from typing import Dict, List, Set

class Graph:
    vertices: int
    graph: Dict[int, List[int]]
    
    def __init__(self, vertices: int):
        self.vertices = vertices
        self.graph = {i: [] for i in range(self.vertices)}

    
    def add_edge(self, u: int, v: int) -> None:
        """Adds edges to the graph"""
        if 0 <= u < self.vertices and 0 <= v < self.vertices:
            self.graph[u].append(v)
            self.graph[v].append(u)
            print(f"Edge added: ({u}, {v})")


    def walk(self, node: int, visited: Set) -> bool:
        """Helper function to recursively perform DFS in the graph"""
        visited.add(node)
        print(node, end=" ")

        for adj in self.graph[node]:
            if adj not in visited:
                self.walk(adj, visited)


    def dfs(self, start_node: int):
        """Performs DFS (Depth First Search) traversal"""
        if start_node >= self.vertices:
            print("Start node is out of bounds.")
            return
        
        visited = set()
        print(f"DFS starting from node: {start_node}")
        self.walk(start_node, visited)
        print()


    def show_graph(self) -> None:
        """To print the graph"""
        print("Graph:")
        for node, neighbors in self.graph.items():
            neighbors_str = ", ".join(map(str, neighbors))
            print(f"{node} → {neighbors_str if neighbors else 'No connections'}")


if __name__ == "__main__":
    graph = Graph(6)

    graph.add_edge(0, 1)
    graph.add_edge(0, 2)
    graph.add_edge(1, 3)
    graph.add_edge(1, 4)
    graph.add_edge(2, 5)

    graph.show_graph()

    graph.dfs(0)
