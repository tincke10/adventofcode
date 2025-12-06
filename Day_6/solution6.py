def parse_problems(lines):
    if not lines:
        return []

    max_len = max(len(line) for line in lines)
    padded_lines = [line.ljust(max_len) for line in lines]
    number_rows = padded_lines[:-1]
    operator_row = padded_lines[-1]

    problems = []
    current_numbers = [[] for _ in range(len(number_rows))]
    current_op = None
    in_problem = False

    for col in range(max_len):
        chars = [row[col] if col < len(row) else ' ' for row in number_rows]
        op_char = operator_row[col] if col < len(operator_row) else ' '
        all_spaces = all(c == ' ' for c in chars) and op_char == ' '

        if all_spaces:
            if in_problem:
                numbers = []
                for row_nums in current_numbers:
                    if row_nums:
                        num_str = ''.join(row_nums).strip()
                        if num_str:
                            numbers.append(int(num_str))

                if numbers and current_op:
                    problems.append((numbers, current_op))

                current_numbers = [[] for _ in range(len(number_rows))]
                current_op = None
                in_problem = False
        else:
            in_problem = True
            for i, c in enumerate(chars):
                current_numbers[i].append(c)

            if op_char in ['+', '*']:
                current_op = op_char

    if in_problem:
        numbers = []
        for row_nums in current_numbers:
            if row_nums:
                num_str = ''.join(row_nums).strip()
                if num_str:
                    numbers.append(int(num_str))

        if numbers and current_op:
            problems.append((numbers, current_op))

    return problems


def solve(input_text):
    lines = input_text.rstrip('\n').split('\n')
    problems = parse_problems(lines)

    grand_total = 0

    for i, (numbers, op) in enumerate(problems):
        if op == '+':
            result = sum(numbers)
        else:
            result = 1
            for n in numbers:
                result *= n

        grand_total += result

    return grand_total


def solve_verbose(input_text):
    lines = input_text.rstrip('\n').split('\n')
    problems = parse_problems(lines)

    print(f"Total de problemas encontrados: {len(problems)}")
    print("-" * 50)

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

    print("-" * 50)
    print(f"GRAN TOTAL: {grand_total}")

    return grand_total


example = """123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +  """

print("=== TEST CON EJEMPLO ===")
result = solve_verbose(example)
expected = 4277556
print(f"\nResultado esperado: {expected}")
print(f"Resultado obtenido: {result}")
print(f"Test: {'PASS ✓' if result == expected else 'FAIL ✗'}")

print("\n" + "=" * 50)
print("=== SOLUCIÓN DEL INPUT REAL ===")
print("=" * 50 + "\n")

with open('input6.md', 'r') as f:
    input_real = f.read()

lines = input_real.rstrip('\n').split('\n')
problems = parse_problems(lines)

print(f"Total de problemas en el input: {len(problems)}")
print("\nPrimeros 5 problemas:")
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

print("\nÚltimos 5 problemas:")
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

print("\n" + "-" * 50)
final_result = solve(input_real)
print(f"\n🎯 RESPUESTA FINAL: {final_result}")
