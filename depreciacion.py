
import statistics

def linea_recta(costo, residual, vida):
    anual = (costo - residual) / vida
    return [round(anual, 2)] * int(vida)

def saldo_decreciente(costo, vida):
    tasa = 2 / vida
    valores = []
    actual = costo
    for _ in range(int(vida)):
        dep = round(actual * tasa, 2)
        valores.append(dep)
        actual -= dep
    return valores

def suma_digitos(costo, residual, vida):
    total = sum(range(1, int(vida)+1))
    base = costo - residual
    return [round((vida-i)/total * base, 2) for i in range(int(vida))]

def unidad_produccion(costo, residual, uso_anual, uso_total):
    tasa = (costo - residual) / uso_total if uso_total else 0
    return [round(u * tasa, 2) for u in uso_anual]

import statistics

def seleccion_optima(metodos, criterio):
    """
    Selecciona el mejor método de depreciación según el criterio elegido.
    
    Parámetros:
    - metodos: diccionario con nombre del método como clave y lista de depreciaciones como valor.
    - criterio: 'fiscal' o 'contable'

    Retorna:
    - Tupla (nombre del método, lista de valores)
    """
    if not metodos:
        return ("Ninguno", [])

    if criterio == "fiscal":
        # Selecciona el método que genera la mayor depreciación en el primer año
        mejor = max(metodos.items(), key=lambda x: x[1][0] if x[1] else 0)

    elif criterio == "contable":
        # Selecciona el método con menor variabilidad (desviación estándar)
        mejor = min(
            metodos.items(),
            key=lambda x: statistics.stdev(x[1]) if len(set(x[1])) > 1 else float('inf')
        )
    else:
        mejor = ("Ninguno", [])

    return mejor
