import yaml

class MotorInferenciaBiblioteca:
    def __init__(self, ruta_archivo):
        self.ruta = ruta_archivo

        #archivo yaml
        self.hechos = []
        self.reglas = []
        self.cargar_base_conocimiento()

    def cargar_base_conocimiento(self):
        with open(self.ruta, 'r', encoding='utf-8') as archivo:
            datos = yaml.safe_load(archivo)
            self.hechos = datos.get('facts', [])
            self.reglas = datos.get('rules', [])
    #Separa funcion y argumento
    def desglosar_atomo(self, texto):
        partes = texto.split('(')
        predicado = partes[0]
        argumento = partes[1].replace(')', '')
        return predicado, argumento

    #variable o constante
    def es_variable(self, texto):
        return texto[0].islower()
    #compara regla con hecho
    def unificar(self, atomo_regla, atomo_hecho):
        pred_regla, arg_regla = self.desglosar_atomo(atomo_regla)
        pred_hecho, arg_hecho = self.desglosar_atomo(atomo_hecho)
        if pred_regla != pred_hecho:
            return None
        if self.es_variable(arg_regla):
            return {arg_regla: arg_hecho}
        elif arg_regla == arg_hecho:
            return {}
        return None

    #variables por valor real
    def sustituir(self, atomo, diccionario_valores):
        pred, arg = self.desglosar_atomo(atomo)
        if self.es_variable(arg) and arg in diccionario_valores:
            valor_real = diccionario_valores[arg]
            return f"{pred}({valor_real})"
        return atomo
    
    #evaluar todo xd
    def evaluar_condiciones(self, condiciones, hechos_conocidos, dicc_valores, indice, resultados):
        if indice == len(condiciones):
            resultados.append(dicc_valores.copy())
            return

        condicion_actual = condiciones[indice]
        condicion_lista = self.sustituir(condicion_actual, dicc_valores)

        for hecho in hechos_conocidos:
            nuevos_valores = self.unificar(condicion_lista, hecho)
            if nuevos_valores is not None:
                dicc_actualizado = dicc_valores.copy()
                dicc_actualizado.update(nuevos_valores)
                self.evaluar_condiciones(condiciones, hechos_conocidos, dicc_actualizado, indice + 1, resultados)

# Forward chaining
    def encadenamiento_hacia_adelante(self):
        hechos_actuales = self.hechos.copy()
        atomos_descubiertos = []

        while True:
            nuevos_en_esta_ronda = []

            for regla in self.reglas:
                combinaciones_exitosas = []
                self.evaluar_condiciones(regla['if'], hechos_actuales, {}, 0, combinaciones_exitosas)
                for dicc in combinaciones_exitosas:
                    nueva_conclusion = self.sustituir(regla['then'], dicc)
                    if nueva_conclusion not in hechos_actuales and nueva_conclusion not in nuevos_en_esta_ronda:
                        nuevos_en_esta_ronda.append(nueva_conclusion)
                        atomos_descubiertos.append(nueva_conclusion)
            if not nuevos_en_esta_ronda:
                break
            hechos_actuales.extend(nuevos_en_esta_ronda)
        return hechos_actuales, atomos_descubiertos
    
#Backward Chaining
    def bc_and(self, condiciones, sub, visitados, traza):
        for cond in condiciones:
            c_sustituida = self.sustituir(cond, sub)
            exito, nueva_traza = self.backward_chain(c_sustituida, visitados)
            traza.extend(nueva_traza)
            if not exito:
                return False, sub
        return True, sub

    def backward_chain(self, meta, visitados=None):
        if visitados is None:
            visitados = set()
        if meta in self.hechos:
            return True, [f"Hecho encontrado: {meta}"]
        if meta in visitados:
            return False, [f"Loop cortado: {meta}"]
        traza = [f"Objetivo actual: {meta}"]
        for regla in self.reglas:
            sub = self.unificar(regla['then'], meta)
            if sub is not None:
                traza.append(f"Aplica regla {regla['id']}")
                exito, _ = self.bc_and(regla['if'], sub, visitados | {meta}, traza)
                if exito:
                    traza.append(f"Validado: {meta}")
                    return True, traza
        traza.append(f"Descartado: {meta}")
        return False, traza

if __name__ == '__main__':
    motor = MotorInferenciaBiblioteca('Razonamiento lógico/solucion01/biblioteca.yaml')

    print("\n=== ENCADENAMIENTO HACIA ADELANTE ===")
    todos_los_hechos, descubrimientos = motor.encadenamiento_hacia_adelante()
    print("Átomos nuevos descubiertos:", descubrimientos)
    for consulta in ["AccesoNoche(Ana)", "AccesoNoche(Luis)", "AccesoNoche(Marta)"]:
        print(f"{consulta} -> {'SI' if consulta in todos_los_hechos else 'NO'}")

    print("\n=== ENCADENAMIENTO HACIA ATRÁS ===")
    for consulta in ["AccesoNoche(Ana)", "AccesoNoche(Luis)", "AccesoNoche(Marta)"]:
        status, traza = motor.backward_chain(consulta)
        print(f"\n[{consulta}] -> {'SI' if status else 'NO'}")
        for paso in traza:
            print(f"  * {paso}")