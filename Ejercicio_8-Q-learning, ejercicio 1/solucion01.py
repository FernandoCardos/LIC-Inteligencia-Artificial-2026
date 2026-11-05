import random
import csv

#parametros
TASA_APRENDIZAJE = 0.5
DESCUENTO = 1.0
PROB_EXPLORACION = 0.1
TOTAL_EPISODIOS = 500
MAXIMOS_PASOS = 200
SEMILLA_ALEATORIA = 99  # seed

#entorno
INICIO = (3, 0)
META = (3, 11)
MOVIMIENTOS = ['N', 'E', 'S', 'W']


def aplicar_transicion(posicion_actual, movimiento):
    fila, columna = posicion_actual

    #movimientos
    if movimiento == 'N': fila -= 1
    elif movimiento == 'E': columna += 1
    elif movimiento == 'S': fila += 1
    elif movimiento == 'W': columna -= 1

    #colisiones
    if fila < 0 or fila > 3 or columna < 0 or columna > 11:
        fila, columna = posicion_actual

    if fila == 3 and 1 <= columna <= 10:
        return INICIO, -100.0, False

    if (fila, columna) == META:
        return META, -1.0, True

    return (fila, columna), -1.0, False

#tabla q
def generar_tabla_q_vacia():
    tabla = {}
    for f in range(4):
        for c in range(12):
            tabla[(f, c)] = {mov: 0.0 for mov in MOVIMIENTOS}
    return tabla

def decidir_movimiento(posicion, tabla, probabilidad_azar):
    if random.random() < probabilidad_azar:
        return random.choice(MOVIMIENTOS)

    valores_estado = tabla[posicion]
    movimiento_optimo = MOVIMIENTOS[0]
    max_valor = float('-inf')

    for mov in MOVIMIENTOS:
        if valores_estado[mov] > max_valor:
            max_valor = valores_estado[mov]
            movimiento_optimo = mov

    return movimiento_optimo

#entrenamiento
def ejecutar_q_learning():
    random.seed(SEMILLA_ALEATORIA)
    tabla_q = generar_tabla_q_vacia()
    registro_recompensas = []

    for episodio in range(TOTAL_EPISODIOS):
        posicion = INICIO
        puntos_episodio = 0.0

        for paso in range(MAXIMOS_PASOS):
            accion = decidir_movimiento(posicion, tabla_q, PROB_EXPLORACION)
            siguiente_posicion, recompensa, finalizado = aplicar_transicion(posicion, accion)

            #valor futuro para Q-learning
            if finalizado:
                estimacion_futura = 0.0
            else:
                estimacion_futura = max(tabla_q[siguiente_posicion].values())

            #actualizacion
            valor_viejo = tabla_q[posicion][accion]
            tabla_q[posicion][accion] = valor_viejo + TASA_APRENDIZAJE * (recompensa + DESCUENTO * estimacion_futura - valor_viejo)

            puntos_episodio += recompensa
            posicion = siguiente_posicion

            if finalizado:
                break

        registro_recompensas.append(puntos_episodio)

    return tabla_q, registro_recompensas

#evaluacion greedy
def evaluar_politica_optima(tabla_q):
    posicion = INICIO
    retorno_total = 0.0
    ruta_acciones = []

    for _ in range(MAXIMOS_PASOS):
        mejor_accion = decidir_movimiento(posicion, tabla_q, probabilidad_azar=0.0)
        siguiente_posicion, recompensa, finalizado = aplicar_transicion(posicion, mejor_accion)

        ruta_acciones.append(mejor_accion)
        retorno_total += recompensa
        posicion = siguiente_posicion

        if finalizado:
            break

    return ruta_acciones, retorno_total

#archivo csv
def exportar_recompensas_csv(historial, nombre_archivo="recompensas_entrenamiento.csv"):
    with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as archivo:
        escritor = csv.writer(archivo)

        #encabezados
        escritor.writerow(['Episodio', 'Recompensa_Cruda', 'Media_Movil_10'])

        for i, recompensa in enumerate(historial):
            inicio_ventana = max(0, i - 9)
            ventana_actual = historial[inicio_ventana : i + 1]
            media_movil = sum(ventana_actual) / len(ventana_actual)
            escritor.writerow([i + 1, recompensa, media_movil])

#ejecucion principal
if __name__ == '__main__':
    tabla_final, historial = ejecutar_q_learning()
    acciones_camino, retorno_greedy = evaluar_politica_optima(tabla_final)
    exportar_recompensas_csv(historial)

    print("--- RESULTADOS DE LA EVALUACIÓN ---")
    print(f"Semilla utilizada: {SEMILLA_ALEATORIA}")
    print(f"Pasos tomados para llegar a la meta: {len(acciones_camino)}")
    print(f"Retorno total: {retorno_greedy}")
    print(f"Camino de acciones (S -> G): {acciones_camino}")