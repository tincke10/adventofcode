#!/usr/bin/env python3
"""
Advent of Code - Day 2 Part Two: Invalid Product IDs
Un ID es inválido si es una secuencia de dígitos repetida AL MENOS dos veces.
Ej: 111 (1×3), 1212121212 (12×5), 565656 (56×3)
"""

def generar_invalidos_en_rango(start, end):
    """
    Genera todos los IDs inválidos dentro de un rango [start, end].
    Un ID es inválido si es una secuencia base repetida >= 2 veces.
    """
    invalidos = set()

    # Determinar el rango de longitudes a considerar
    min_len = len(str(start))
    max_len = len(str(end))

    # Para cada longitud total posible
    for longitud_total in range(2, max_len + 1):
        # Para cada posible longitud de base
        for longitud_base in range(1, longitud_total):
            # Verificar que longitud_total sea múltiplo de longitud_base
            if longitud_total % longitud_base != 0:
                continue

            repeticiones = longitud_total // longitud_base
            if repeticiones < 2:
                continue

            # Rango de la base (sin ceros iniciales)
            base_min = 10 ** (longitud_base - 1) if longitud_base > 1 else 1
            base_max = 10 ** longitud_base - 1

            # Generar candidatos
            for base in range(base_min, base_max + 1):
                # Crear el número inválido repitiendo la base
                base_str = str(base)
                invalido = int(base_str * repeticiones)

                # Verificar si está en el rango
                if start <= invalido <= end:
                    invalidos.add(invalido)

    return sorted(invalidos)


def resolver(input_str):
    """Resuelve el problema dado el string de input."""
    # Parsear los rangos
    rangos = []
    for parte in input_str.strip().split(','):
        if '-' in parte:
            inicio, fin = parte.split('-')
            rangos.append((int(inicio), int(fin)))

    # Encontrar todos los IDs inválidos
    total = 0
    todos_invalidos = []

    for start, end in rangos:
        invalidos = generar_invalidos_en_rango(start, end)
        todos_invalidos.extend(invalidos)
        subtotal = sum(invalidos)
        if invalidos:
            print(f"Rango {start}-{end}: {len(invalidos)} inválido(s) = {invalidos} -> suma parcial: {subtotal}")
        total += subtotal

    return total, todos_invalidos


# Verificar con el ejemplo del problema
ejemplo = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"""

# Input del problema
input_data = """874324-1096487,6106748-6273465,1751-4283,294380-348021,5217788-5252660,828815656-828846474,66486-157652,477-1035,20185-55252,17-47,375278481-375470130,141-453,33680490-33821359,88845663-88931344,621298-752726,21764551-21780350,58537958-58673847,9983248-10042949,4457-9048,9292891448-9292952618,4382577-4494092,199525-259728,9934981035-9935011120,6738255458-6738272752,8275916-8338174,1-15,68-128,7366340343-7366538971,82803431-82838224,72410788-72501583"""

if __name__ == "__main__":
    # Primero verificar con el ejemplo
    print("=" * 60)
    print("VERIFICACIÓN CON EJEMPLO")
    print("=" * 60)
    resultado_ejemplo, _ = resolver(ejemplo)
    print(f"\nResultado ejemplo: {resultado_ejemplo}")
    print(f"Esperado: 4174379265")
    print(f"¿Correcto? {'✓ SÍ' if resultado_ejemplo == 4174379265 else '✗ NO'}")

    print("\n")
    print("=" * 60)
    print("SOLUCIÓN REAL - Day 2 Part Two")
    print("=" * 60)
    print()

    resultado, invalidos = resolver(input_data)

    print()
    print("=" * 60)
    print(f"Total de IDs inválidos encontrados: {len(invalidos)}")
    print(f"RESPUESTA FINAL: {resultado}")
    print("=" * 60)
