KB = {
    "Hechos": [],
    "Reglas": [
        {"condición": "riesgo=bajo ∧ eficiencia_energetica=True", "decisión": "Aprobado"},
        {"condición": "riesgo=alto ∧ impacto_ambiental=negativo", "decisión": "Rechazado"},
        {"condición": "riesgo=medio ∧ impacto_ambiental=positivo ∧ cofinanciamiento=True", "decisión": "AprobadoCondicionadoMitigaciónSeguimiento"}
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
        condiciones = regla["condición"].split("∧")
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


