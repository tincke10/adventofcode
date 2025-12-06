import bisect


def parse_and_merge_ranges(filename: str) -> tuple[list[tuple[int, int]], list[int]]:
    with open(filename) as f:
        content = f.read()

    parts = content.strip().split('\n\n')
    ranges_raw = parts[0].strip().split('\n')
    ids_raw = parts[1].strip().split('\n')

    ranges = []
    for line in ranges_raw:
        start, end = map(int, line.split('-'))
        ranges.append((start, end))

    ranges.sort()
    merged = []
    for start, end in ranges:
        if merged and start <= merged[-1][1] + 1:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))

    ids_to_check = [int(line) for line in ids_raw]

    return merged, ids_to_check


def solve_part1(filename: str) -> int:
    merged, ids_to_check = parse_and_merge_ranges(filename)

    starts = [r[0] for r in merged]
    count = 0

    for id_val in ids_to_check:
        idx = bisect.bisect_right(starts, id_val) - 1
        if idx >= 0 and merged[idx][0] <= id_val <= merged[idx][1]:
            count += 1

    return count


def solve_part2(filename: str) -> int:
    merged, _ = parse_and_merge_ranges(filename)

    total = sum(end - start + 1 for start, end in merged)

    return total


if __name__ == "__main__":
    result1 = solve_part1("input5.md")
    print(f"Part 1 - Ingredientes frescos disponibles: {result1}")

    result2 = solve_part2("input5.md")
    print(f"Part 2 - Total IDs frescos en rangos: {result2}")
