import heapq


class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = self.h = self.f = 0

    def __lt__(self, other):
        return self.f < other.f

class AStarSearch:
    def __init__(self, start, goal, grid_size):
        self.start, self.goal = start, goal
        self.grid_width, self.grid_height = grid_size
        self.memo = {}

    def heuristic(self, pos):
        if pos not in self.memo:
            self.memo[pos] = abs(pos[0] - self.goal[0]) + abs(pos[1] - self.goal[1])
        return self.memo[pos]

    def get_neighbors(self, node):
        moves = [(0,1), (1,0), (0,-1), (-1,0)]
        return [Node((node.position[0]+dx, node.position[1]+dy), node)
                for dx, dy in moves
                if 0 <= node.position[0]+dx < self.grid_width and 0 <= node.position[1]+dy < self.grid_height]

    def reconstruct_path(self, node):
        path = []
        while node:
            path.append(node.position)
            node = node.parent
        return path[::-1]

    def search(self):
        open_set = [Node(self.start)]
        closed_set = set()

        while open_set:
            current = heapq.heappop(open_set)
            if current.position == self.goal:
                return self.reconstruct_path(current)
            closed_set.add(current.position)

            for neighbor in self.get_neighbors(current):
                if neighbor.position in closed_set:
                    continue
                tentative_g = current.g + 1
                in_open = next((n for n in open_set if n.position == neighbor.position), None)
                if not in_open or tentative_g < neighbor.g:
                    neighbor.g = tentative_g
                    neighbor.h = self.heuristic(neighbor.position)
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.parent = current
                    if not in_open:
                        heapq.heappush(open_set, neighbor)
        return None

def get_input():
    def parse_tuple(s):
        x, y = map(int, s.strip().split(','))
        return (x, y)

    grid_width = int(input("Enter grid width: "))
    grid_height = int(input("Enter grid height: "))
    grid_size = (grid_width, grid_height)

    start = parse_tuple(input("Enter start position (x,y): "))
    goal = parse_tuple(input("Enter goal position (x,y): "))

    return start, goal, grid_size

if __name__ == "__main__":
    start, goal, grid_size = get_input()
    astar = AStarSearch(start, goal, grid_size)
    path = astar.search()
    print("Path found:" if path else "No path found.")
    if path:
        print(path)
