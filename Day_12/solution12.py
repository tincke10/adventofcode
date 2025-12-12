def parse_input(text):
    sections = text.strip().split('\n\n')
    shapes = []
    regions = []

    for section in sections:
        lines = section.strip().split('\n')
        if lines[0][0].isdigit() and ':' in lines[0]:
            first_line = lines[0]
            if 'x' in first_line:
                for line in lines:
                    parts = line.split(': ')
                    dims = parts[0].split('x')
                    width, height = int(dims[0]), int(dims[1])
                    quantities = list(map(int, parts[1].split()))
                    regions.append((width, height, quantities))
            else:
                shape = set()
                for r, line in enumerate(lines[1:]):
                    for c, char in enumerate(line):
                        if char == '#':
                            shape.add((r, c))
                shapes.append(shape)

    return shapes, regions


def normalize_shape(shape):
    if not shape:
        return tuple()
    min_r = min(r for r, c in shape)
    min_c = min(c for r, c in shape)
    return tuple(sorted((r - min_r, c - min_c) for r, c in shape))


def rotate_90(shape):
    return {(c, -r) for r, c in shape}


def flip_horizontal(shape):
    return {(r, -c) for r, c in shape}


def get_all_orientations(shape):
    orientations = set()
    current = shape
    for _ in range(4):
        orientations.add(normalize_shape(current))
        orientations.add(normalize_shape(flip_horizontal(current)))
        current = rotate_90(current)
    return list(orientations)


def get_shape_dimensions(shape):
    if not shape:
        return (0, 0)
    max_r = max(r for r, c in shape)
    max_c = max(c for r, c in shape)
    return (max_r + 1, max_c + 1)


def can_place(grid, shape, start_r, start_c, height, width):
    for r, c in shape:
        nr, nc = start_r + r, start_c + c
        if nr >= height or nc >= width or grid[nr][nc]:
            return False
    return True


def place_shape(grid, shape, start_r, start_c):
    for r, c in shape:
        grid[start_r + r][start_c + c] = True


def remove_shape(grid, shape, start_r, start_c):
    for r, c in shape:
        grid[start_r + r][start_c + c] = False


def solve_region(height, width, pieces):
    if not pieces:
        return True

    grid = [[False] * width for _ in range(height)]

    piece_types = {}
    for piece in pieces:
        key = tuple(sorted(piece))
        if key not in piece_types:
            orientations = get_all_orientations(set(piece))
            placements = []
            for orientation in orientations:
                shape_h, shape_w = get_shape_dimensions(orientation)
                for start_r in range(height - shape_h + 1):
                    for start_c in range(width - shape_w + 1):
                        placements.append((orientation, start_r, start_c))
            piece_types[key] = {'placements': placements, 'count': 0}
        piece_types[key]['count'] += 1

    piece_list = list(piece_types.values())
    total_pieces = sum(p['count'] for p in piece_list)
    min_positions = [0] * len(piece_list)

    def backtrack(type_idx, pieces_placed):
        if pieces_placed == total_pieces:
            return True

        while type_idx < len(piece_list) and piece_list[type_idx]['count'] == 0:
            type_idx += 1
            if type_idx < len(piece_list):
                min_positions[type_idx] = 0

        if type_idx >= len(piece_list):
            return False

        piece_info = piece_list[type_idx]
        placements = piece_info['placements']

        for i in range(min_positions[type_idx], len(placements)):
            orientation, start_r, start_c = placements[i]

            if can_place(grid, orientation, start_r, start_c, height, width):
                place_shape(grid, orientation, start_r, start_c)
                piece_info['count'] -= 1
                old_min = min_positions[type_idx]
                min_positions[type_idx] = i + 1

                if backtrack(type_idx, pieces_placed + 1):
                    return True

                min_positions[type_idx] = old_min
                piece_info['count'] += 1
                remove_shape(grid, orientation, start_r, start_c)

        min_positions[type_idx] = 0
        return False

    return backtrack(0, 0)


def can_fit_region(width, height, quantities, shape_orientations, shape_sizes):
    total_cells_needed = sum(q * s for q, s in zip(quantities, shape_sizes))
    if total_cells_needed > width * height:
        return False

    pieces = []
    for shape_idx, qty in enumerate(quantities):
        base_orientation = shape_orientations[shape_idx][0]
        for _ in range(qty):
            pieces.append(base_orientation)

    if not pieces:
        return True

    pieces.sort(key=lambda p: -len(p))
    return solve_region(height, width, pieces)


def solve_part1(input_text):
    shapes, regions = parse_input(input_text)
    shape_orientations = [get_all_orientations(shape) for shape in shapes]
    shape_sizes = [len(shape) for shape in shapes]

    count = 0
    for i, (width, height, quantities) in enumerate(regions):
        if can_fit_region(width, height, quantities, shape_orientations, shape_sizes):
            count += 1
        if (i + 1) % 100 == 0:
            print(f"Processed {i + 1}/{len(regions)} regions...")

    return count


def main():
    with open('Day_12/input12.md', 'r') as f:
        input_text = f.read()

    result = solve_part1(input_text)
    print(f"Part 1: {result}")


if __name__ == '__main__':
    main()
