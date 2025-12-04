# Advent of Code - Day 2: Los IDs Truchos

## De qué va la cosa

Resulta que en la tienda de regalos del Polo Norte, un pibito elfo se puso a boludear con la compu y llenó la base de datos con IDs de productos re truchos. Nosotros tenemos que encontrar esos IDs chotos dentro de unos rangos y sumarlos todos.

---

## Parte Uno: El Número se Repite Dos Veces Exactas

### La Onda

Un ID es **trucho** si el número es una secuencia que se repite **exactamente dos veces**, ni más ni menos.

### Ejemplos pa' que se entienda

| Número | Cómo se arma | ¿Trucho? |
|--------|--------------|----------|
| `55` | "5" + "5" | Sí, re trucho |
| `6464` | "64" + "64" | Trucho mal |
| `123123` | "123" + "123" | Trucho también |
| `101` | No es repetición doble | Na, este anda |
| `111` | "1" × 3 (son 3, no 2) | Este zafa |

### La Matemática del Asunto

1. **Tiene que ser par**: El número trucho siempre tiene cantidad par de dígitos (2, 4, 6, 8...)

2. **La fórmula**:
   ```
   str(N) = X + X  donde la mitad es igual a la otra mitad
   ```

3. **Cuántos truchos hay por longitud**:
   - De 2 dígitos: 9 truchos (11, 22, ..., 99)
   - De 4 dígitos: 90 truchos (1010, 1111, ..., 9999)
   - De 2n dígitos: `9 × 10^(n-1)` truchos

4. **Nada de ceros adelante**: El "0101" no existe porque no arrancamos con cero

---

## Parte Dos: Se Repite Dos Veces O Más

### El Cambio

Ahora un ID es **trucho** si la secuencia se repite **dos veces o más**. O sea, también cuentan los que se repiten 3, 4, 5 veces...

### Ejemplos Nuevos

| Número | Cómo se arma | ¿Trucho? |
|--------|--------------|----------|
| `111` | "1" × 3 | Ahora sí es trucho |
| `1212121212` | "12" × 5 | Re trucho |
| `565656` | "56" × 3 | Trucho |
| `828828828` | "828" × 3 | Trucho también |
| `9292929292` | "92" × 5 | Trucho a full |

### La Matemática (un toque más heavy)

1. **El largo tiene que ser divisible**: La longitud del número tiene que dividirse exactamente por la longitud de la base, y el resultado >= 2

2. **Un número puede armarse de varias formas**:
   - `111111` = "1" × 6 = "11" × 3 = "111" × 2
   - Pero lo contamos una sola vez, no somos boludos

---

## Las Soluciones

### Solución 1: A lo Bruto (No va)

Recorrer todos los números del rango uno por uno y fijarte si es trucho.

```python
def es_trucho(n):
    """Fijate si n es trucho."""
    s = str(n)
    largo = len(s)

    if largo % 2 == 0:
        mitad = largo // 2
        if s[:mitad] == s[mitad:]:
            return True
    return False
```

**El problema**: Si el rango es de 9292891448 a 9292952618, tenés que revisar ~61,000 números. Un embole.

---

### Solución 2: Generar los Candidatos (Esta va como piña)

En vez de revisar todos, generamos solamente los números que pueden ser truchos.

#### Parte Uno

```python
def generar_truchos_parte1(start, end):
    """Genera los truchos (secuencia × 2) en el rango."""
    truchos = []
    max_largo = len(str(end))

    for largo in range(2, max_largo + 2, 2):  # Solo largos pares
        n = largo // 2
        base_min = 10 ** (n - 1) if n > 1 else 1
        base_max = 10 ** n - 1

        for base in range(base_min, base_max + 1):
            trucho = int(str(base) * 2)
            if start <= trucho <= end:
                truchos.append(trucho)
            elif trucho > end:
                break  # Ya fue, nos pasamos

    return truchos
```

#### Parte Dos

```python
def generar_truchos_parte2(start, end):
    """Genera los truchos (secuencia × n, n >= 2) en el rango."""
    truchos = set()  # Usamos set pa' no repetir
    max_largo = len(str(end))

    for largo_total in range(2, max_largo + 1):
        for largo_base in range(1, largo_total):
            if largo_total % largo_base != 0:
                continue

            repeticiones = largo_total // largo_base
            if repeticiones < 2:
                continue

            base_min = 10 ** (largo_base - 1) if largo_base > 1 else 1
            base_max = 10 ** largo_base - 1

            for base in range(base_min, base_max + 1):
                trucho = int(str(base) * repeticiones)
                if start <= trucho <= end:
                    truchos.add(trucho)

    return sorted(truchos)
```

**Por qué va**: Generás solo los candidatos truchos en vez de revisar millones de números al pedo.

---

### Solución 3: Pura Matemática (Para los cracks)

Si tenés rangos gigantes, podés calcular directo cuántos truchos hay sin generar ninguno. Pero ya es mucho bardo para este problema.

---

## Qué tan rápido anda cada una

| Solución | Tiempo | Memoria | Cuándo usarla |
|----------|--------|---------|---------------|
| A lo bruto | Lento mal | Poca | Rangos chiquitos (<1000) |
| Generar candidatos | Piola | Normal | La mayoría de casos |
| Matemática pura | Un cohete | Casi nada | Rangos gigantes |

---

## Los Resultados

### Parte Uno

| Qué | Cuánto |
|-----|--------|
| Truchos encontrados | 565 |
| **Suma total** | **43,952,536,386** |

### Parte Dos

| Qué | Cuánto |
|-----|--------|
| Truchos encontrados | 623 |
| **Suma total** | **54,486,209,192** |

### La Diferencia

| Qué | Cuánto más |
|-----|------------|
| Truchos extra | +58 |
| Guita extra | +10,533,672,806 |

---

## Rangos Copados del Input

### Los que más truchos tienen
| Rango | Parte 1 | Parte 2 |
|-------|---------|---------|
| `621298-752726` | 131 | 143 |
| `874324-1096487` | 126 | 137 |

### Los truchos más grosos
| Trucho | De qué rango | El patrón |
|--------|--------------|-----------|
| 9,934,999,349 | `9934981035-9935011120` | "99349" × 2 |
| 9,292,929,292 | `9292891448-9292952618` | "92" × 5 |
| 7,366,473,664 | `7366340343-7366538971` | "73664" × 2 |

---

## Los Archivos

- `solution_day2.py` - Solución Parte Uno
- `solution_day2_part2.py` - Solución Parte Dos

---

## Lo que Aprendimos

1. **Mejor generar que verificar**: Es al pedo revisar millones de números si podés generar solo los que te interesan.

2. **El set es tu amigo**: En la Parte Dos un número puede armarse de varias formas. Con `set()` te asegurás de no contarlo dos veces como un salame.

3. **Cortar a tiempo**: Si ya te pasaste del rango, dejá de buscar. No seas termo.
