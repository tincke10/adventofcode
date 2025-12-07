#!/usr/bin/env python3

from collections import defaultdict

def parse_input(filename):
    with open(filename, 'r') as f:
        lines = [line.rstrip('\n') for line in f.readlines()]
    return lines

def find_start(grid):
    for row_idx, row in enumerate(grid):
        for col_idx, char in enumerate(row):
            if char == 'S':
                return (row_idx, col_idx)
    return None

def simulate_tachyon_beams(grid):
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    start = find_start(grid)
    if not start:
        return 0

    start_row, start_col = start
    active_beams = {start_col}
    split_count = 0

    for row in range(start_row + 1, rows):
        if not active_beams:
            break

        splitters_in_row = set()
        for col, char in enumerate(grid[row]):
            if char == '^':
                splitters_in_row.add(col)

        beams_hitting_splitters = active_beams & splitters_in_row
        beams_passing_through = active_beams - splitters_in_row
        new_beams = set(beams_passing_through)

        for col in beams_hitting_splitters:
            split_count += 1
            left_col = col - 1
            right_col = col + 1

            if 0 <= left_col < cols:
                new_beams.add(left_col)
            if 0 <= right_col < cols:
                new_beams.add(right_col)

        active_beams = new_beams

    return split_count

def simulate_quantum_timelines(grid):
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    start = find_start(grid)
    if not start:
        return 0

    start_row, start_col = start
    timelines = defaultdict(int)
    timelines[start_col] = 1

    for row in range(start_row + 1, rows):
        if not timelines:
            break

        splitters_in_row = set()
        for col, char in enumerate(grid[row]):
            if char == '^':
                splitters_in_row.add(col)

        new_timelines = defaultdict(int)

        for col, count in timelines.items():
            if col in splitters_in_row:
                left_col = col - 1
                right_col = col + 1

                if 0 <= left_col < cols:
                    new_timelines[left_col] += count
                if 0 <= right_col < cols:
                    new_timelines[right_col] += count
            else:
                new_timelines[col] += count

        timelines = new_timelines

    return sum(timelines.values())

def main():
    grid = parse_input('input7.md')

    splits = simulate_tachyon_beams(grid)
    print(f"Part 1: The beam is split {splits} times")

    timelines = simulate_quantum_timelines(grid)
    print(f"Part 2: {timelines} different timelines")

if __name__ == "__main__":
    main()
