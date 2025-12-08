"""
Day 8: Playground - Advent of Code
Solution using Union-Find (Disjoint Set Union) data structure
"""

def parse_input(filename):
    """Parse the input file and return list of 3D coordinates."""
    coordinates = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                x, y, z = map(int, line.split(','))
                coordinates.append((x, y, z))
    return coordinates


class UnionFind:
    """Union-Find data structure with path compression and union by size."""

    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        """Find the root of x with path compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        """Unite the sets containing x and y. Returns True if they were in different sets."""
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False

        if self.size[root_x] < self.size[root_y]:
            root_x, root_y = root_y, root_x

        self.parent[root_y] = root_x
        self.size[root_x] += self.size[root_y]
        return True

    def get_circuit_sizes(self):
        """Return a list of all circuit sizes."""
        sizes = []
        for i in range(len(self.parent)):
            if self.parent[i] == i:
                sizes.append(self.size[i])
        return sizes


def distance_squared(p1, p2):
    """Calculate squared Euclidean distance between two 3D points."""
    return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2


def generate_sorted_pairs(coordinates):
    """Generate all pairs sorted by distance (ascending)."""
    n = len(coordinates)
    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            dist_sq = distance_squared(coordinates[i], coordinates[j])
            pairs.append((dist_sq, i, j))
    pairs.sort()
    return pairs


def solve_part1(coordinates, num_connections=1000):
    """
    Part 1: Connect the closest pairs of junction boxes and return
    the product of the three largest circuit sizes.
    """
    n = len(coordinates)
    pairs = generate_sorted_pairs(coordinates)
    uf = UnionFind(n)

    connections_made = 0
    for dist_sq, i, j in pairs:
        uf.union(i, j)
        connections_made += 1

        if connections_made >= num_connections:
            break

    sizes = uf.get_circuit_sizes()
    sizes.sort(reverse=True)

    result = sizes[0] * sizes[1] * sizes[2]

    return result, sizes[:10]


def solve_part2(coordinates):
    """
    Part 2: Connect junction boxes until all are in one circuit.
    Return the product of X coordinates of the last two boxes connected.
    """
    n = len(coordinates)
    pairs = generate_sorted_pairs(coordinates)
    uf = UnionFind(n)

    num_circuits = n
    last_i, last_j = -1, -1

    for dist_sq, i, j in pairs:
        if uf.union(i, j):
            num_circuits -= 1
            last_i, last_j = i, j

            if num_circuits == 1:
                break

    x1 = coordinates[last_i][0]
    x2 = coordinates[last_j][0]

    return x1 * x2, (last_i, last_j), (coordinates[last_i], coordinates[last_j])


def main():
    coordinates = parse_input('input8.md')
    print(f"Number of junction boxes: {len(coordinates)}")

    print("\n--- Part 1 ---")
    result1, top_sizes = solve_part1(coordinates, num_connections=1000)
    print(f"Top 10 circuit sizes: {top_sizes}")
    print(f"Product of three largest circuits: {result1}")

    print("\n--- Part 2 ---")
    result2, indices, coords = solve_part2(coordinates)
    print(f"Last connection: box {indices[0]} and box {indices[1]}")
    print(f"Coordinates: {coords[0]} and {coords[1]}")
    print(f"X coordinates: {coords[0][0]} and {coords[1][0]}")
    print(f"Product of X coordinates: {result2}")


if __name__ == "__main__":
    main()
