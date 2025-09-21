KB = {
    "Hechos": [],
    "Reglas": [
        {"condición": "riesgo=bajo && eficiencia_energetica=True", "decisión": "Aprobado"},
        {"condición": "riesgo=alto && impacto_ambiental=negativo", "decisión": "Rechazado"},
        {"condición": "riesgo=medio && impacto_ambiental=positivo && cofinanciamiento=True", "decisión": "AprobadoCondicionadoMitigaciónSeguimiento"}
    ]
}

def agregar_hecho(solicitante, proyecto, condición, valor):
    KB["Hechos"].append({
        "solicitante": solicitante,
        "proyecto": proyecto,
        "condición": condición,
        "valor": valor
    })

def hechos_de(solicitante, proyecto):
    return [h for h in KB["Hechos"] if h["solicitante"] == solicitante and h["proyecto"] == proyecto]

def aplicar_reglas(solicitante, proyecto):
    hechos = hechos_de(solicitante, proyecto)
    decisiones = []
    justificaciones = []
    for regla in KB["Reglas"]:
        condiciones = regla["condición"].split("&&")
        cumple = True
        for cond in condiciones:
            cond = cond.strip()
            if "=" in cond:
                clave, valor = cond.split("=")
                clave = clave.strip()
                valor = valor.strip()
                if valor == "True":
                    valor = True
                elif valor == "False":
                    valor = False
                encontrado = any(
                    h["condición"] == clave and h["valor"] == valor
                    for h in hechos
                )
                if not encontrado:
                    cumple = False
                    break
        if cumple:
            decisiones.append(regla["decisión"])
            justificaciones.append(regla["condición"])
    return decisiones, justificaciones

def priorizar_recomendaciones(decisiones):
    prioridad = {
        "Aprobado": 3,
        "AprobadoCondicionadoMitigaciónSeguimiento": 2,
        "Rechazado": 0
    }
    if not decisiones:
        return "Sin decisión"
    return sorted(decisiones, key=lambda d: prioridad.get(d, -1), reverse=True)[0]

def evaluar_credito(solicitante, proyecto):
    print(f"Evaluando crédito para {solicitante} y proyecto {proyecto}")
    decisiones, justificaciones = aplicar_reglas(solicitante, proyecto)
    decision_final = priorizar_recomendaciones(decisiones)
    print(f"Decisión priorizada: {decision_final}")
    print(f"Justificación: {justificaciones}")
    print("---")

agregar_hecho("Juan", "Edificio Verde", "riesgo", "bajo")
agregar_hecho("Juan", "Edificio Verde", "eficiencia_energetica", True)

agregar_hecho("Ana", "Fabrica", "riesgo", "alto")
agregar_hecho("Ana", "Fabrica", "impacto_ambiental", "negativo")

agregar_hecho("Luis", "Planta Solar", "riesgo", "medio")
agregar_hecho("Luis", "Planta Solar", "impacto_ambiental", "positivo")
agregar_hecho("Luis", "Planta Solar", "cofinanciamiento", True)

# Pruebas
evaluar_credito("Juan", "Edificio Verde")
evaluar_credito("Ana", "Fabrica")
evaluar_credito("Luis", "Planta Solar")

