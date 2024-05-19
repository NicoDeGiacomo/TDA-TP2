from pulp import LpProblem, LpMaximize, LpVariable, lpSum, LpBinary, LpStatus, value

actores = ['A1', 'A2']
papeles = ['P1', 'P2']
potencialidades = {
    ('A1', 'P1'): 100,
    ('A1', 'P2'): 50,
    ('A2', 'P1'): 60,
    ('A2', 'P2'): 60
}

prob = LpProblem("Asignacion de Actores", LpMaximize)

# Variables de decisión
x = LpVariable.dicts("asignacion", [(a, p) for a in actores for p in papeles], 0, 1, LpBinary)

# Función objetivo
prob += lpSum(potencialidades[(a, p)] * x[(a, p)] for a in actores for p in papeles)

# Restricciones
for a in actores:
    prob += lpSum(x[(a, p)] for p in papeles) <= 1, f"actor_{a}_max_papel"
for p in papeles:
    prob += lpSum(x[(a, p)] for a in actores) == 1, f"papel_{p}_un_actor"

prob.solve()

print("Estado:", LpStatus[prob.status])
print("Potencialidad total:", value(prob.objective))
print("Asignaciones:")
for a in actores:
    for p in papeles:
        if x[(a, p)].varValue == 1:
            print(f"{a} asignado a {p} con potencialidad {potencialidades[(a, p)]}")

