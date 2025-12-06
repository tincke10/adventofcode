def parse_problems_part2(lines):
    if not lines:
        return []

    max_len = max(len(line) for line in lines)
    padded_lines = [line.ljust(max_len) for line in lines]
    number_rows = padded_lines[:-1]
    operator_row = padded_lines[-1]

    problems = []
    current_columns = []
    current_op = None
    in_problem = False

    for col in range(max_len - 1, -1, -1):
        chars = [row[col] if col < len(row) else ' ' for row in number_rows]
        op_char = operator_row[col] if col < len(operator_row) else ' '
        all_spaces = all(c == ' ' for c in chars) and op_char == ' '

        if all_spaces:
            if in_problem and current_columns:
                numbers = []
                for col_chars in current_columns:
                    digits = [c for c in col_chars if c.isdigit()]
                    if digits:
                        num = int(''.join(digits))
                        numbers.append(num)

                if numbers and current_op:
                    problems.append((numbers, current_op))

                current_columns = []
                current_op = None
                in_problem = False
        else:
            in_problem = True
            current_columns.append(chars)

            if op_char in ['+', '*']:
                current_op = op_char

    if in_problem and current_columns:
        numbers = []
        for col_chars in current_columns:
            digits = [c for c in col_chars if c.isdigit()]
            if digits:
                num = int(''.join(digits))
                numbers.append(num)

        if numbers and current_op:
            problems.append((numbers, current_op))

    return problems


def solve_part2(input_text):
    lines = input_text.rstrip('\n').split('\n')
    problems = parse_problems_part2(lines)

    grand_total = 0

    for numbers, op in problems:
        if op == '+':
            result = sum(numbers)
        else:
            result = 1
            for n in numbers:
                result *= n

        grand_total += result

    return grand_total


def solve_part2_verbose(input_text):
    lines = input_text.rstrip('\n').split('\n')
    problems = parse_problems_part2(lines)

    print(f"Total de problemas encontrados: {len(problems)}")
    print("-" * 60)

    grand_total = 0

    for i, (numbers, op) in enumerate(problems):
        if op == '+':
            result = sum(numbers)
            expr = ' + '.join(map(str, numbers))
        else:
            result = 1
            for n in numbers:
                result *= n
            expr = ' * '.join(map(str, numbers))

        print(f"Problema {i+1}: {expr} = {result}")
        grand_total += result

    print("-" * 60)
    print(f"GRAN TOTAL: {grand_total}")

    return grand_total


example = """123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +  """

print("=== TEST CON EJEMPLO (PART TWO) ===")
print("Ejemplo input:")
print(example)
print()

result = solve_part2_verbose(example)
expected = 3263827
print(f"\nResultado esperado: {expected}")
print(f"Resultado obtenido: {result}")
print(f"Test: {'PASS ✓' if result == expected else 'FAIL ✗'}")

print("\nVerificación manual del ejemplo:")
print("  - Problema más a la derecha: 4 + 431 + 623 = 1058")
print("  - Segundo desde la derecha: 175 * 581 * 32 = 3253600")
print("  - Tercero desde la derecha: 8 + 248 + 369 = 625")
print("  - Más a la izquierda: 356 * 24 * 1 = 8544")
print("  - Total: 1058 + 3253600 + 625 + 8544 = 3263827")

print("\n" + "=" * 60)
print("=== SOLUCIÓN PART TWO - INPUT REAL ===")
print("=" * 60 + "\n")

with open('input6.md', 'r') as f:
    input_real = f.read()

lines = input_real.rstrip('\n').split('\n')
problems = parse_problems_part2(lines)

print(f"Total de problemas en el input: {len(problems)}")
print("\nPrimeros 5 problemas (desde la derecha):")
for i, (nums, op) in enumerate(problems[:5]):
    if op == '+':
        result = sum(nums)
        expr = ' + '.join(map(str, nums))
    else:
        result = 1
        for n in nums:
            result *= n
        expr = ' * '.join(map(str, nums))
    print(f"  {i+1}. {expr} = {result}")

print("\nÚltimos 5 problemas (más a la izquierda):")
for i, (nums, op) in enumerate(problems[-5:]):
    idx = len(problems) - 5 + i
    if op == '+':
        result = sum(nums)
        expr = ' + '.join(map(str, nums))
    else:
        result = 1
        for n in nums:
            result *= n
        expr = ' * '.join(map(str, nums))
    print(f"  {idx+1}. {expr} = {result}")

print("\n" + "-" * 60)
final_result = solve_part2(input_real)
print(f"\n🎯 RESPUESTA PART TWO: {final_result}")
