import re
from itertools import combinations
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds


def parse_line(line):
    diagram_match = re.search(r'\[([.#]+)\]', line)
    if not diagram_match:
        return None, None, None

    diagram = diagram_match.group(1)
    n_lights = len(diagram)
    target = [1 if c == '#' else 0 for c in diagram]

    buttons = []
    for button_match in re.finditer(r'\(([0-9,]+)\)', line):
        indices = [int(x) for x in button_match.group(1).split(',')]
        button_vector = [0] * n_lights
        for idx in indices:
            if idx < n_lights:
                button_vector[idx] = 1
        buttons.append(button_vector)

    joltage_match = re.search(r'\{([0-9,]+)\}', line)
    joltage = None
    if joltage_match:
        joltage = [int(x) for x in joltage_match.group(1).split(',')]

    return target, buttons, joltage


def apply_buttons(buttons, button_mask, n_lights):
    state = [0] * n_lights
    for i, use_button in enumerate(button_mask):
        if use_button:
            for j in range(n_lights):
                state[j] ^= buttons[i][j]
    return state


def find_min_presses(target, buttons):
    n_lights = len(target)
    n_buttons = len(buttons)

    for num_presses in range(n_buttons + 1):
        for combo in combinations(range(n_buttons), num_presses):
            mask = [1 if i in combo else 0 for i in range(n_buttons)]
            state = apply_buttons(buttons, mask, n_lights)
            if state == target:
                return num_presses

    return -1


def find_min_joltage_presses(joltage, buttons):
    n_counters = len(joltage)
    n_buttons = len(buttons)

    button_matrix = []
    for button in buttons:
        indices = [i for i, v in enumerate(button) if v == 1]
        jolt_vector = [0] * n_counters
        for idx in indices:
            if idx < n_counters:
                jolt_vector[idx] = 1
        button_matrix.append(jolt_vector)

    A = np.array(button_matrix).T
    b = np.array(joltage)
    c = np.ones(n_buttons)
    constraints = LinearConstraint(A, lb=b, ub=b)
    upper_bound = sum(joltage) + 1
    bounds = Bounds(lb=0, ub=upper_bound)
    integrality = np.ones(n_buttons)

    result = milp(c, constraints=constraints, bounds=bounds, integrality=integrality)

    if result.success:
        return int(round(result.fun))
    else:
        return -1


def solve_part1(input_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    total = 0
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue

        target, buttons, _ = parse_line(line)
        if target is None:
            continue

        min_presses = find_min_presses(target, buttons)
        if min_presses >= 0:
            total += min_presses
            print(f"Máquina {i}: {min_presses} pulsaciones")
        else:
            print(f"Máquina {i}: SIN SOLUCIÓN")

    print(f"\nPart 1 Total: {total}")
    return total


def solve_part2(input_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    total = 0
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue

        _, buttons, joltage = parse_line(line)
        if joltage is None:
            continue

        min_presses = find_min_joltage_presses(joltage, buttons)
        if min_presses >= 0:
            total += min_presses
            print(f"Máquina {i}: {min_presses} pulsaciones")
        else:
            print(f"Máquina {i}: SIN SOLUCIÓN")

    print(f"\nPart 2 Total: {total}")
    return total


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "2":
        solve_part2("input10.md")
    else:
        solve_part1("input10.md")
