from typing import List, Set
from collections import defaultdict


class Graph:
    vertices: int
    graph: defaultdict[int, List[int]]

    def __init__(self, vertices: int) -> None:
        self.vertices = vertices
        self.graph = defaultdict(list)

    def add_edge(self, u: int, v: int) -> None:
        """Adds edges to the graph"""
        if 0 <= u < self.vertices and 0 <= v < self.vertices:
            self.graph[u].append(v)
            self.graph[v].append(u)
            print(f"Edge added: ({u}, {v})")

    def walk(self, node: int, visited: Set) -> None:
        """Helper function to recursively perform DFS in the graph"""
        visited.add(node)
        print(node, end=" ")

        for adj in self.graph[node]:
            if adj not in visited:
                self.walk(adj, visited)

    def dfs(self, start_node: int) -> None:
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
        print("\nGraph:")
        for node, neighbors in self.graph.items():
            neighbors_str = ", ".join(map(str, neighbors))
            print(f"{node} → {neighbors_str if neighbors else 'No connections'}")


if __name__ == "__main__":
    vertices = int(input("Enter the number of vertices: "))
    graph = Graph(vertices)

    edges_count = int(input("Enter the number of edges: "))
    print("Enter the edges (u v):")

    for _ in range(edges_count):
        u, v = map(int, input().split())
        graph.add_edge(u, v)

    graph.show_graph()

    start_node = int(input("\nEnter the start node for DFS: "))
    graph.dfs(start_node)
