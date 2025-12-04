def count_accessible_rolls(filename: str) -> int:
    with open(filename, 'r') as f:
        grid = [line.rstrip('\n') for line in f if line.strip()]

    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]

    accessible_count = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != '@':
                continue

            neighbor_rolls = 0
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if grid[nr][nc] == '@':
                        neighbor_rolls += 1

            if neighbor_rolls < 4:
                accessible_count += 1

    return accessible_count


if __name__ == "__main__":
    example = [
        "..@@.@@@@.",
        "@@@.@.@.@@",
        "@@@@@.@.@@",
        "@.@@@@..@.",
        "@@.@@@@.@@",
        ".@@@@@@@.@",
        ".@.@.@.@@@",
        "@.@@@.@@@@",
        ".@@@@@@@@.",
        "@.@.@@@.@.",
    ]

    rows = len(example)
    cols = len(example[0])
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]

    example_count = 0
    for r in range(rows):
        for c in range(cols):
            if example[r][c] != '@':
                continue
            neighbor_rolls = 0
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if example[nr][nc] == '@':
                        neighbor_rolls += 1
            if neighbor_rolls < 4:
                example_count += 1

    print(f"Ejemplo: {example_count} rollos accesibles (esperado: 13)")
    print()

    result = count_accessible_rolls("Input_4.md")
    print(f"Respuesta Part 1: {result}")
