def parse_input(text):
    graph = {}
    for line in text.strip().split('\n'):
        parts = line.split(': ')
        node = parts[0]
        neighbors = parts[1].split() if len(parts) > 1 else []
        graph[node] = neighbors
    return graph


def count_paths(graph, start, end, memo=None):
    if memo is None:
        memo = {}
    if start == end:
        return 1
    if start in memo:
        return memo[start]
    if start not in graph:
        return 0
    total = 0
    for neighbor in graph[start]:
        total += count_paths(graph, neighbor, end, memo)
    memo[start] = total
    return total


def count_paths_through_both(graph, start, end, required1, required2):
    paths_via_1_then_2 = (count_paths(graph, start, required1, {}) *
                          count_paths(graph, required1, required2, {}) *
                          count_paths(graph, required2, end, {}))
    paths_via_2_then_1 = (count_paths(graph, start, required2, {}) *
                          count_paths(graph, required2, required1, {}) *
                          count_paths(graph, required1, end, {}))
    return paths_via_1_then_2 + paths_via_2_then_1


def solve_part1(input_text):
    graph = parse_input(input_text)
    return count_paths(graph, 'you', 'out')


def solve_part2(input_text):
    graph = parse_input(input_text)
    return count_paths_through_both(graph, 'svr', 'out', 'dac', 'fft')


def main():
    with open('Day_11/input11.md', 'r') as f:
        input_text = f.read()

    result1 = solve_part1(input_text)
    print(f"Part 1: {result1}")

    result2 = solve_part2(input_text)
    print(f"Part 2: {result2}")


if __name__ == '__main__':
    main()
