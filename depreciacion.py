#Importe de la biblioteca statistics de Phyton
import statistics
 #Grafica de linea recta
def linea_recta(costo, residual, vida):
    anual = (costo - residual) / vida
    return [round(anual, 2)] * int(vida)
 #Grafica de saldo decreciente
def saldo_decreciente(costo, vida):
    tasa = 2 / vida
    valores = []
    actual = costo
    for _ in range(int(vida)):
        dep = round(actual * tasa, 2)
        valores.append(dep)
        actual -= dep
    return valores
 #Grafica de suma digitos
def suma_digitos(costo, residual, vida):
    total = sum(range(1, int(vida)+1))
    base = costo - residual
    return [round((vida-i)/total * base, 2) for i in range(int(vida))]
 #Grafica de unidad de produccion
def unidad_produccion(costo, residual, uso_anual, uso_total):
    tasa = (costo - residual) / uso_total if uso_total else 0
    return [round(u * tasa, 2) for u in uso_anual]
 #Seleccion de la opcion mas optima segun el criterio contable o el fiscal
def seleccion_optima(metodos, criterio):
    if criterio == "fiscal":
        mejor = max(metodos.items(), key=lambda x: x[1][0])
    elif criterio == "contable":
        mejor = min(metodos.items(), key=lambda x: statistics.stdev(x[1]) if len(x[1]) > 1 else float('inf'))
    else:
        mejor = ("Ninguno", [])
    return mejor