# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 22:14:48 2023

@author: david

Punto 1 parcial 2 MOS
"""

#Imports plots
import matplotlib.pyplot as plt

#Pyomo para el modelo
from pyomo.environ import *
from pyomo.opt import SolverFactory


#Funcion para eliminar un componente
def eliminarComponente(modelo, nombreComponente):

        #lista de componentes para ser eliminados que corresponden con el nombre dado
        lista_eliminados = [vr for vr in vars(modelo) if vr.startswith(nombreComponente)]

        lista_eliminados_str = ', '.join(lista_eliminados)
        print('Eliminando los componentes ({}) del modelo.'.format(lista_eliminados_str))

        for componente in lista_eliminados:
            modelo.del_component(componente)


#Iteraciones
numIter=5
itera=range(numIter)
vector = [i/(numIter-1) for i in range(numIter)]
valor1, valor2 = 0,0
#e_vec=[2,3,4,5,6,7,8,9,10,11]

#Creación del modelo
Modelo = ConcreteModel()

#parametros y conjuntos
numNodos = 5
Modelo.N=RangeSet(1,numNodos)

#Saltos (hops)
Modelo.h =Param(Modelo.N, Modelo.N, mutable=True, default= 999)

Modelo.h[1,2] = 1
Modelo.h[1,3] = 1
Modelo.h[2,5] = 1
Modelo.h[3,4] = 1
Modelo.h[4,5] = 1

#costos (Costs)
Modelo.c =Param(Modelo.N, Modelo.N, mutable=True, default= 999)

Modelo.c[1,2] = 10
Modelo.c[1,3] = 5
Modelo.c[2,5] = 10
Modelo.c[3,4] = 5
Modelo.c[4,5] = 5

#Se escoge el nodo origen y el nodo destino
nodoOrigen = 1
nodoDestino = 5
        

#variables

Modelo.x = Var(Modelo.N,Modelo.N, domain=Binary)


## Funciones objetivo

#Función saltos(hops)
Modelo.f1 = sum(Modelo.x[i,j] * Modelo.h[i,j] for i in Modelo.N for j in Modelo.N)

#Función de costos(costs)
Modelo.f2 = sum(Modelo.x[i,j] * Modelo.c[i,j] for i in Modelo.N for j in Modelo.N)


#Proceso de suma ponderada para ejecución en multiples iteraciones del modelo.
valoresF1 = []
valoresF2 =[]
for valor2 in vector:
    
    valor1 = 1 - valor2 

    # Definición de la función objetivo general
    Modelo.O_z = Objective(expr=valor1 * Modelo.f1 + valor2 * Modelo.f2, sense=minimize)
    
    # Restricción eConstraint
    Modelo.eConstraint = Constraint(Modelo.N, rule=lambda m, i: sum(m.x[i, j] * m.h[i, j] for j in m.N) <= numIter)

    # Restricción del nodo de origen
    Modelo.origen = Constraint(Modelo.N, rule=lambda m, i: sum(m.x[i, j] for j in m.N) == 1 if i == nodoOrigen else Constraint.Skip)

    # Restricción del nodo de destino
    Modelo.destino = Constraint(Modelo.N, rule=lambda m, j: sum(m.x[i, j] for i in m.N) == 1 if j == nodoDestino else Constraint.Skip)

    # Restricción de nodos intermedios
    Modelo.intermedios = Constraint(Modelo.N, rule=lambda m, i: sum(m.x[i, j] for j in m.N) - sum(m.x[j, i] for j in m.N) == 0 if i != nodoOrigen and i != nodoDestino else Constraint.Skip) 

    # Resolver el modelo
    SolverFactory('glpk').solve(Modelo)

    # Obtener los valores de las funciones objetivo
    valor_f1 = value(Modelo.f1)
    valor_f2 = value(Modelo.f2)
    valores_f1.append(valor_f1)
    valores_f2.append(valor_f2)

    # Eliminar los componentes de restricción
    eliminar_componente(modelo, 'O_z')
    eliminar_componente(modelo, 'origen')
    eliminar_componente(modelo, 'destino')
    eliminar_componente(modelo, 'intermedios')
    eliminar_componente(modelo, 'eConstraint')

# Grafica del frente óptimo de Pareto
plt.plot(valores_f1, valores_f2, 'o-.')
plt.title('Frente Óptimo de Pareto')
plt.xlabel('F1')
plt.ylabel('F2')
plt.grid(True)
plt.show()
