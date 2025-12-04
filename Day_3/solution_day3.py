def solve_day3(filename: str) -> int:
    total = 0

    with open(filename, 'r') as f:
        for line in f:
            bank = line.strip()
            if not bank:
                continue

            max_joltage = 0

            for i in range(len(bank) - 1):
                first_digit = int(bank[i])
                max_second = max(int(d) for d in bank[i + 1:])
                joltage = first_digit * 10 + max_second

                if joltage > max_joltage:
                    max_joltage = joltage

            total += max_joltage

    return total


if __name__ == "__main__":
    example = [
        "987654321111111",
        "811111111111119",
        "234234234234278",
        "818181911112111",
    ]

    example_total = 0
    for bank in example:
        max_joltage = 0
        for i in range(len(bank) - 1):
            first_digit = int(bank[i])
            max_second = max(int(d) for d in bank[i + 1:])
            joltage = first_digit * 10 + max_second
            if joltage > max_joltage:
                max_joltage = joltage
        print(f"{bank}: {max_joltage}")
        example_total += max_joltage

    print(f"Ejemplo total: {example_total} (esperado: 357)")
    print()

    result = solve_day3("Input3.md")
    print(f"Respuesta Part 1: {result}")
