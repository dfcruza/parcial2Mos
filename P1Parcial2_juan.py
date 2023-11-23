# Punto 1. Parcial 2 MOS. Juan Felipe Castaño Lozano. 20182065.
import matplotlib.pyplot as plt
from pyomo.environ import *
from pyomo.opt import SolverFactory

# Función para eliminar componentes del modelo
def eliminar_componente(modelo, nombre_componente):
    # Elimina los componentes del modelo que comienzan con el nombre dado
    componentes_a_eliminar = [var for var in vars(modelo) if var.startswith(nombre_componente)]
    
    # Elimina todos los componentes que coinciden con el nombre dado a partir de la función del_component de pyomo. 
    for componente in componentes_a_eliminar:
        modelo.del_component(componente)

# Definir parámetros y variables
num_iteraciones = 5
vector = [i / (num_iteraciones - 1) for i in range(num_iteraciones)]
peso1, peso2 = 0, 0

# Creación del modelo
modelo = ConcreteModel()

# Definición de conjuntos
num_nodos = 5
modelo.N = RangeSet(1, num_nodos)

# Definición de parámetros 'h' (Saltos)
modelo.h = Param(modelo.N, modelo.N, mutable=True, default=999)
modelo.h[1, 2] = 1
modelo.h[1, 3] = 1
modelo.h[2, 5] = 1
modelo.h[3, 4] = 1
modelo.h[4, 5] = 1

# Definición de parámetros 'c' (Costos)
modelo.c = Param(modelo.N, modelo.N, mutable=True, default=999)
modelo.c[1, 2] = 10
modelo.c[1, 3] = 5
modelo.c[2, 5] = 10
modelo.c[3, 4] = 5
modelo.c[4, 5] = 5

# Definición nodos de origen y destino
nodo_origen = 1
nodo_destino = 5

# Definición de variables
modelo.x = Var(modelo.N, modelo.N, domain=Binary)

# Definición de funciones objetivo
modelo.f1 = sum(modelo.x[i, j] * modelo.h[i, j] for i in modelo.N for j in modelo.N)  # Función 'saltos'
modelo.f2 = sum(modelo.x[i, j] * modelo.c[i, j] for i in modelo.N for j in modelo.N)  # Función 'costos'

# Proceso de método de suma ponderada ejecutando en mutliples iteraciones el modelo. 
valores_f1 = []
valores_f2 = []
for peso2 in vector:
    peso1 = 1 - peso2

    # Definición de la función objetivo general
    modelo.O_z = Objective(expr=peso1 * modelo.f1 + peso2 * modelo.f2, sense=minimize)

    # Restricción para el nodo de origen
    modelo.origen = Constraint(modelo.N, rule=lambda m, i: sum(m.x[i, j] for j in m.N) == 1 if i == nodo_origen else Constraint.Skip)

    # Restricción para el nodo de destino
    modelo.destino = Constraint(modelo.N, rule=lambda m, j: sum(m.x[i, j] for i in m.N) == 1 if j == nodo_destino else Constraint.Skip)

    # Restricción para nodos intermedios
    modelo.intermedios = Constraint(modelo.N, rule=lambda m, i: sum(m.x[i, j] for j in m.N) - sum(m.x[j, i] for j in m.N) == 0 if i != nodo_origen and i != nodo_destino else Constraint.Skip)

    # Restricción eConstraint
    modelo.restriccion_e = Constraint(modelo.N, rule=lambda m, i: sum(m.x[i, j] * m.h[i, j] for j in m.N) <= num_iteraciones)

    # Resolver el modelo
    SolverFactory('glpk').solve(modelo)

    # Obtenemos los valores de las funciones objetivo
    valor_f1 = value(modelo.f1)
    valor_f2 = value(modelo.f2)
    valores_f1.append(valor_f1)
    valores_f2.append(valor_f2)

    # Eliminamos los componentes de restricción
    eliminar_componente(modelo, 'O_z')
    eliminar_componente(modelo, 'origen')
    eliminar_componente(modelo, 'destino')
    eliminar_componente(modelo, 'intermedios')
    eliminar_componente(modelo, 'restriccion_e')

# Graficamos el frente óptimo de Pareto
plt.plot(valores_f1, valores_f2, 'o-.')
plt.title('Frente Óptimo de Pareto')
plt.xlabel('F1')
plt.ylabel('F2')
plt.grid(True)
plt.show()
