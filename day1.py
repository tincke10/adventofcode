DIAL_SIZE = 100
INITIAL_POSITION = 50


def parse_rotation(line):
    """Extrae la dirección y distancia de una linea de rotacion."""
    if '→' in line:
        rotation = line.split('→')[1].strip()
    else:
        rotation = line.strip()
    return rotation[0], int(rotation[1:])


def parse_input(input_text):
    """Parsea todas las rotaciones del texto de entrada."""
    return [parse_rotation(line) for line in input_text.strip().split('\n')]


def count_zero_endings(input_text):
    """Parte 1: Cuenta cuantas veces el dial termina en 0 después de una rotacion."""
    rotations = parse_input(input_text)
    position = INITIAL_POSITION
    zero_count = 0

    for direction, distance in rotations:
        if direction == 'R':
            position = (position + distance) % DIAL_SIZE
        else:
            position = (position - distance) % DIAL_SIZE

        if position == 0:
            zero_count += 1

    return zero_count


def count_zero_passes_right(position, distance):
    """Cuenta cuantas veces pasamos por 0 al rotar a la derecha."""
    return (position + distance) // DIAL_SIZE


def count_zero_passes_left(position, distance):
    """Cuenta cuantas veces pasamos por 0 al rotar a la izquierda."""
    if position == 0:
        return distance // DIAL_SIZE
    elif distance >= position:
        return (distance - position) // DIAL_SIZE + 1
    return 0


def count_all_zero_clicks(input_text):
    """Parte 2: Cuenta cada click que cae en 0 (durante y al final de las rotaciones)."""
    rotations = parse_input(input_text)
    position = INITIAL_POSITION
    zero_count = 0

    for direction, distance in rotations:
        if direction == 'R':
            zero_count += count_zero_passes_right(position, distance)
            position = (position + distance) % DIAL_SIZE
        else:
            zero_count += count_zero_passes_left(position, distance)
            position = (position - distance) % DIAL_SIZE

    return zero_count


if __name__ == "__main__":
    EXAMPLE = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""

    print(f"Parte 1 - Ejemplo: {count_zero_endings(EXAMPLE)}")  # Segun example: 3
    print(f"Parte 2 - Ejemplo: {count_all_zero_clicks(EXAMPLE)}")  # Segun example: 6

    try:
        with open("inputday1.md") as f:
            data = f.read()
            print(f"Parte 1 - Respuesta: {count_zero_endings(data)}")
            print(f"Parte 2 - Respuesta: {count_all_zero_clicks(data)}")
    except FileNotFoundError:
        print("Input file not found.")
