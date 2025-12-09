def parse_input(filename):
    """Lee el archivo y retorna lista de coordenadas (x, y)"""
    tiles = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                x, y = map(int, line.split(','))
                tiles.append((x, y))
    return tiles


def find_max_rectangle_area(tiles):
    """Encuentra el área máxima de un rectángulo con dos baldosas rojas en esquinas opuestas"""
    max_area = 0
    n = len(tiles)

    for i in range(n):
        x1, y1 = tiles[i]
        for j in range(i + 1, n):
            x2, y2 = tiles[j]
            # El área incluye las baldosas de los bordes: (diferencia + 1)
            width = abs(x2 - x1) + 1
            height = abs(y2 - y1) + 1
            area = width * height
            max_area = max(max_area, area)

    return max_area


def build_polygon_edges(tiles):
    """Construye el conjunto de baldosas en el borde del polígono (rojas + verdes conectoras)"""
    edge_tiles = set()
    n = len(tiles)

    for i in range(n):
        x1, y1 = tiles[i]
        x2, y2 = tiles[(i + 1) % n]
        if x1 == x2:  # Línea vertical
            for y in range(min(y1, y2), max(y1, y2) + 1):
                edge_tiles.add((x1, y))
        else:  # Línea horizontal
            for x in range(min(x1, x2), max(x1, x2) + 1):
                edge_tiles.add((x, y1))

    return edge_tiles


def get_polygon_segments(tiles):
    """Retorna los segmentos horizontales del polígono para ray-casting"""
    n = len(tiles)
    horizontal_segments = []
    vertical_segments = []

    for i in range(n):
        x1, y1 = tiles[i]
        x2, y2 = tiles[(i + 1) % n]

        if y1 == y2:  # Segmento horizontal
            horizontal_segments.append((min(x1, x2), max(x1, x2), y1))
        else:  # Segmento vertical
            vertical_segments.append((x1, min(y1, y2), max(y1, y2)))

    return horizontal_segments, vertical_segments


def is_inside_polygon(x, y, tiles, horizontal_segments, vertical_segments):
    """Determina si un punto está dentro del polígono usando ray-casting"""

    crossings = 0

    for seg_x, y_min, y_max in vertical_segments:
        if seg_x > x and y_min < y < y_max:
            crossings += 1

    return crossings % 2 == 1


def get_horizontal_segments(tiles):
    """Retorna segmentos horizontales del polígono"""
    n = len(tiles)
    horizontal_segments = []
    for i in range(n):
        x1, y1 = tiles[i]
        x2, y2 = tiles[(i + 1) % n]
        if y1 == y2:
            horizontal_segments.append((min(x1, x2), max(x1, x2), y1))
    return horizontal_segments


def rectangle_is_valid_optimized(x1, y1, x2, y2, vertical_segments, horizontal_segments):
    """
    Verifica si el rectángulo está completamente dentro del polígono.
    Un rectángulo está dentro si:
    1. Las 4 esquinas están dentro o en el borde
    2. Ningún segmento del polígono cruza el interior del rectángulo
    """
    min_x, max_x = min(x1, x2), max(x1, x2)
    min_y, max_y = min(y1, y2), max(y1, y2)

    # Verificar que las 4 esquinas estén dentro del polígono
    corners = [(min_x, min_y), (max_x, min_y), (min_x, max_y), (max_x, max_y)]

    for cx, cy in corners:
        crossings = 0
        for seg_x, seg_y_min, seg_y_max in vertical_segments:
            if seg_x > cx and seg_y_min < cy < seg_y_max:
                crossings += 1
        on_vertical = any(seg_x == cx and seg_y_min <= cy <= seg_y_max
                          for seg_x, seg_y_min, seg_y_max in vertical_segments)
        on_horizontal = any(seg_y == cy and seg_x_min <= cx <= seg_x_max
                            for seg_x_min, seg_x_max, seg_y in horizontal_segments)

        if not on_vertical and not on_horizontal and crossings % 2 == 0:
            return False

    for seg_x, seg_y_min, seg_y_max in vertical_segments:
        if min_x < seg_x < max_x:

            if seg_y_min < max_y and seg_y_max > min_y:
                return False

    for seg_x_min, seg_x_max, seg_y in horizontal_segments:
        if min_y < seg_y < max_y:
            if seg_x_min < max_x and seg_x_max > min_x:
                return False

    return True


def find_max_rectangle_area_part2(tiles):
    """Encuentra el área máxima considerando solo baldosas rojas/verdes"""
    _, vertical_segments = get_polygon_segments(tiles)
    horizontal_segments = get_horizontal_segments(tiles)

    max_area = 0
    n = len(tiles)

    for i in range(n):
        x1, y1 = tiles[i]
        for j in range(i + 1, n):
            x2, y2 = tiles[j]

            if rectangle_is_valid_optimized(x1, y1, x2, y2, vertical_segments, horizontal_segments):
                width = abs(x2 - x1) + 1
                height = abs(y2 - y1) + 1
                area = width * height
                max_area = max(max_area, area)

    return max_area


def main():
    tiles = parse_input('input9.md')
    print(f"Total de baldosas rojas: {len(tiles)}")
    max_area = find_max_rectangle_area(tiles)
    print(f"Parte 1 - Área máxima del rectángulo: {max_area}")

    print("Calculando parte 2...")
    max_area_p2 = find_max_rectangle_area_part2(tiles)
    print(f"Parte 2 - Área máxima del rectángulo: {max_area_p2}")


if __name__ == "__main__":
    main()
