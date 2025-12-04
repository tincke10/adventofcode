def max_number_k_digits(bank: str, k: int) -> int:
    n = len(bank)
    to_remove = n - k

    stack = []
    for digit in bank:
        while stack and to_remove > 0 and stack[-1] < digit:
            stack.pop()
            to_remove -= 1
        stack.append(digit)

    while to_remove > 0:
        stack.pop()
        to_remove -= 1

    return int(''.join(stack))


def solve_day3_part2(filename: str) -> int:
    total = 0

    with open(filename, 'r') as f:
        for line in f:
            bank = line.strip()
            if not bank:
                continue

            joltage = max_number_k_digits(bank, 12)
            total += joltage

    return total


if __name__ == "__main__":
    examples = [
        ("987654321111111", 987654321111),
        ("811111111111119", 811111111119),
        ("234234234234278", 434234234278),
        ("818181911112111", 888911112111),
    ]

    print("Verificación del ejemplo:")
    example_total = 0
    for bank, expected in examples:
        result = max_number_k_digits(bank, 12)
        status = "✓" if result == expected else f"✗ (esperado {expected})"
        print(f"  {bank}: {result} {status}")
        example_total += result

    expected_total = 3121910778619
    status = "✓" if example_total == expected_total else f"✗ (esperado {expected_total})"
    print(f"  Total ejemplo: {example_total} {status}")
    print()

    result = solve_day3_part2("Input3.md")
    print(f"Respuesta Part 2: {result}")
