from pulp import LpProblem, LpMaximize, LpVariable, lpSum, LpBinary, LpStatus, value
import sys

def leer_postulaciones(archivo):
    actores = {}
    with open(archivo, 'r') as file:
        for linea in file:
            datos = linea.strip().split(',')
            actor = datos[0]
            postulaciones = {int(datos[i]): int(datos[i+1]) for i in range(1, len(datos), 2)}
            actores[actor] = postulaciones
    return actores

def main(archivo_postulaciones):
  actores = leer_postulaciones(archivo_postulaciones)
  papeles = set(p for postulaciones in actores.values() for p in postulaciones.keys())
  potencialidades = {(actor, papel): potencialidad for actor, postulaciones in actores.items() for papel, potencialidad in postulaciones.items()}

  print(potencialidades)

  prob = LpProblem("Asignacion de Actores", LpMaximize)

  x = LpVariable.dicts("asignacion", [(a, p) for a in actores for p in papeles], 0, 1, LpBinary)

  # Función objetivo
  prob += lpSum(actores[a].get(p, 0) * x[(a, p)] for a in actores for p in papeles)

  # Restricciones
  for a in actores:
      prob += lpSum(x[(a, p)] for p in actores[a]) <= 1, f"actor_{a}_max_papel"
  for p in papeles:
      prob += lpSum(x[(a, p)] for a in actores if p in actores[a]) == 1, f"papel_{p}_un_actor"

  prob.solve()

  print("Estado:", LpStatus[prob.status])
  print("Potencialidad total:", value(prob.objective))
  print("Asignaciones:")
  for a in actores:
      for p in actores[a]:
          if x[(a, p)].varValue == 1:
              print(f"{a} asignado a {p} con potencialidad {actores[a][p]}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
      print("Uso: python actores-papeles.py [archivo_postulaciones]")
    else:
      main(sys.argv[1])