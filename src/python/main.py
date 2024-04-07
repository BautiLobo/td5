import json
import numpy as np

BIG_NUMBER = 1e10  # Revisar si es necesario.


def main():

    # Ejemplo para leer una instancia con json
    instance_name = "titanium.json"
    filename = "C:\\Users\\bauti\\Desktop\\TD5\\td5\\data\\" + instance_name
    with open(filename) as f:
        instance = json.load(f)

    K = instance["n"]
    m = 6
    n = 6
    N = 8
    solucion = []
    soluciones = [[]]
    mejor_solucion = [None]
    mejor_error = [BIG_NUMBER]  

    # Ejemplo para definir una grilla de m x n.
    grid_x = np.linspace(min(instance["x"]), max(instance["x"]), num=m, endpoint=True)
    grid_y = np.linspace(min(instance["y"]), max(instance["y"]), num=n, endpoint=True)
    lista_breakpoints: list[list[tuple]] = [[] for _ in range(m)]

    for i in range(m):
        for j in range(n):
            lista_breakpoints[i].append((grid_x[i], grid_y[j]))

    # TODO: aca se deberia ejecutar el algoritmo

    def coordinates(solucion):
        cordenadas = {'x': [point[0] for point in solucion], 'y': [point[1] for point in solucion]}
        return cordenadas
	

    def FB(n, lista_breakpoints, x, solucion, soluciones,):
        if x == len(lista_breakpoints):
            soluciones.append(solucion.copy())  # Almacenar una copia de la solución actual
            return  # Terminar esta rama de la recursión

        for punto in lista_breakpoints[x]:
            solucion.append(punto)
            FB(n, lista_breakpoints, x + 1, solucion, soluciones)
            solucion.pop()  # Retirar el último elemento añadido

        return soluciones
    
    def error(soluciones, instance):
        lista_errores = []
        
        for punto in soluciones:
            coordenadas = coordinates(punto)
            error_parcial = 0
            
            for i in range(len(coordenadas['x']) - 1):
                m = (coordenadas['y'][i + 1] - coordenadas['y'][i]) / (coordenadas['x'][i + 1] - coordenadas['x'][i]) 
                b = coordenadas['y'][i] - (m * coordenadas['x'][i])
                
                for j in range(coordenadas['x'].index(coordenadas['x'][i]), 
                            coordenadas['x'].index(coordenadas['x'][i + 1])):
                    
                    x, y = coordenadas['x'][j], coordenadas['y'][j]
                    y_pred = (m * x) + b
                    error_parcial += abs(y - y_pred)
            lista_errores.append(error_parcial)
        
        return lista_errores
    def BT(n, lista_breakpoints, x, solucion, mejor_solucion, mejor_error):
        if x == n:
            e = error(solucion, instance)
            if e < mejor_error[0]:
                mejor_error[0] = e
                mejor_solucion[0] = solucion.copy()
            return

        for punto in lista_breakpoints[x]:
            solucion.append(punto)
            BT(n, lista_breakpoints, x + 1, solucion, mejor_solucion, mejor_error)
            solucion.pop()



    solucionesFB = FB(n, lista_breakpoints, 0, solucion, soluciones,)
    solucionesBT = BT(n, lista_breakpoints, 0, solucion, mejor_solucion, mejor_error)


    print(len(solucionesFB))
    print(len(solucionesBT))
    print(solucionesBT)
    errores = error(solucionesBT, instance)
    #print(errores)

  
    best = {}
    best['sol'] = [None] * (N + 1)
    best['obj'] = BIG_NUMBER

    #Posible ejemplo (para la instancia titanium) de formato de solucion, y como exportarlo a JSON.
    #La solucion es una lista de tuplas (i,j), donde:
    #- i indica el indice del punto de la discretizacion de la abscisa
    # - j indica el indice del punto de la discretizacion de la ordenada.
    best['sol'] = [(0, 0), (1, 0), (2, 0), (3, 2), (4, 0), (5, 0)]
    best['obj'] = 5.927733333333335

    # Representamos la solucion con un diccionario que indica:
    # - n: cantidad de breakpoints
    # - x: lista con las coordenadas de la abscisa para cada breakpoint
    ## - y: lista con las coordenadas de la ordenada para cada breakpoint
    solution = {}
    solution['n'] = len(best['sol'])
    solution['x'] = [grid_x[x[0]] for x in best['sol']]
    solution['y'] = [grid_y[x[1]] for x in best['sol']]
    solution['obj'] = best['obj']

    # Se guarda el archivo en formato JSON
    with open('solution_' + instance_name, 'w') as f:
        json.dump(solution, f)


if __name__ == "__main__":
    main()
