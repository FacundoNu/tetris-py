import os.path as path
import csv
from random import randint


ANCHO_JUEGO, ALTO_JUEGO = 9, 18
IZQUIERDA, DERECHA = -1, 1
CUBO = 0
Z = 1
S = 2
I = 3
L = 4
L_INV = 5
T = 6

def rotaciones():   # Función que reemplaza la cte PIEZAS (está debajo de la función). Devuelve un diccionario y en generar pieza se utiliza el nombre de la pieza y la rotación en posición 0.
    PIEZAS = {}
    with open("piezas.txt") as piezas:
        for linea in piezas:
            rotaciones_final = []
            coordenadas, nombre = linea.split("#")
            
            coordenadas = coordenadas.rstrip(" ")
            nombre = nombre.lstrip(" ").rstrip("\n")
            
            coordenadas = coordenadas.split(" ")
            for coordenada in coordenadas:
                rotaciones = []                            
                coordenada = coordenada.split(";")
                for coordenada_individual in coordenada:                    
                    coordenada_x, coordenada_y = coordenada_individual.split(",")
                    coordenada_x, coordenada_y = int(coordenada_x), int(coordenada_y)
                    rotaciones.append((coordenada_x, coordenada_y))
                rotaciones_final.append(tuple(rotaciones))
                
            if not nombre in PIEZAS:
                PIEZAS[nombre] = rotaciones_final
            else:
                PIEZAS[nombre].append(rotaciones_final)
    return PIEZAS


PIEZAS = rotaciones()



def generar_pieza(pieza=None):
    """
    Genera una nueva pieza de entre PIEZAS al azar. Si se especifica el parámetro pieza
    se generará una pieza del tipo indicado. Los tipos de pieza posibles
    están dados por las constantes CUBO, Z, S, I, L, L_INV, T.

    El valor retornado es una tupla donde cada elemento es una posición
    ocupada por la pieza, ubicada en (0, 0). Por ejemplo, para la pieza
    I se devolverá: ( (0, 0), (0, 1), (0, 2), (0, 3) ), indicando que 
    ocupa las posiciones (x = 0, y = 0), (x = 0, y = 1), ..., etc.
    """
    piezas = ("Cubo", "Z", "S", "I", "L", "-L", "T")
    if pieza == None:
        pieza = piezas[randint(0, len(PIEZAS) - 1)]
    
    return PIEZAS[pieza][0]
    


def trasladar_pieza(pieza, dx, dy):
    """
    Traslada la pieza de su posición actual a (posicion + (dx, dy)).

    La pieza está representada como una tupla de posiciones ocupadas,
    donde cada posición ocupada es una tupla (x, y). 
    Por ejemplo para la pieza ( (0, 0), (0, 1), (0, 2), (0, 3) ) y
    el desplazamiento dx=2, dy=3 se devolverá la pieza 
    ( (2, 3), (2, 4), (2, 5), (2, 6) ).
    """
    pieza_trasladada = []
    
    for coordenadas in pieza:
        lista_para_modificar = list(coordenadas)
        lista_para_modificar[0] += dx
        lista_para_modificar[1] += dy
        pieza_trasladada.append(tuple(lista_para_modificar))
        
    return tuple(pieza_trasladada)


def crear_juego(pieza_inicial):
    """
    Crea un nuevo juego de Tetris.

    El parámetro pieza_inicial es una pieza obtenida mediante 
    pieza.generar_pieza. Ver documentación de esa función para más información.

    El juego creado debe cumplir con lo siguiente:
    - La grilla está vacía: hay_superficie da False para todas las ubicaciones
    - La pieza actual está arriba de todo, en el centro de la pantalla.
    - El juego no está terminado: terminado(juego) da False

    Que la pieza actual esté arriba de todo significa que la coordenada Y de 
    sus posiciones superiores es 0 (cero).
    """
    juego = []
    for i in range(ALTO_JUEGO):
        fila = []
        for j in range(ANCHO_JUEGO):
            fila.append("O")
        juego.append(fila)
    
    pieza_centrada = trasladar_pieza(pieza_inicial, ANCHO_JUEGO//2, 0)
    
    for posicion_x, posicion_y in pieza_centrada:
        juego[posicion_y][posicion_x] = "P"

    return juego

def dimensiones(juego):
    """
    Devuelve las dimensiones de la grilla del juego como una tupla (ancho, alto).
    """
    alto = len(juego)
    ancho = len(juego[0])
    return (ancho, alto)

def pieza_actual(juego):
    """
    Devuelve una tupla de tuplas (x, y) con todas las posiciones de la
    grilla ocupadas por la pieza actual.

    Se entiende por pieza actual a la pieza que está cayendo y todavía no
    fue consolidada con la superficie.

    La coordenada (0, 0) se refiere a la posición que está en la esquina 
    superior izquierda de la grilla.
    """
    posiciones_ocupadas = []
    for fila in range(len(juego)):
        for columna in range(len(juego[fila])):
            if juego[fila][columna] == "P":
                posiciones_ocupadas.append((columna, fila))
    
    posiciones_ocupadas = tuple(posiciones_ocupadas)
        
    return posiciones_ocupadas

def hay_superficie(juego, x, y):
    """
    Devuelve True si la celda (x, y) está ocupada por la superficie consolidada.
    
    La coordenada (0, 0) se refiere a la posición que está en la esquina 
    superior izquierda de la grilla.
    """
    return juego[y][x] == 'X'


def mover(juego, direccion):
    """
    Mueve la pieza actual hacia la derecha o izquierda, si es posible.
    Devuelve un nuevo estado de juego con la pieza movida o el mismo estado 
    recibido si el movimiento no se puede realizar.

    El parámetro direccion debe ser una de las constantes DERECHA o IZQUIERDA.
    """
    pieza = pieza_actual(juego)
    

    contador = 0
    for posicion_x, posicion_y in pieza:
        if (posicion_x + direccion) < len(juego[posicion_y]) and not posicion_x + direccion < 0 and not hay_superficie(juego, posicion_x + direccion, posicion_y):
            contador += 1
    if contador == 4:
        pieza_trasladada = trasladar_pieza(pieza, direccion, 0)
    else:
        return juego
    
    
    for fila in range(len(juego)):
        for elemento in range(len(juego[0])):
            if juego[fila][elemento] == "P":
                juego[fila][elemento] = "O"
    for coordenada in pieza_trasladada:
        juego[coordenada[1]][coordenada[0]] = "P"
    
    
    return juego

def eliminar_filas(juego):
    """
    Recibe la grilla y analiza todas las filas que estén completamente consolidadas ("X") y las elimina.
    Luego, crea otra grilla a la que se le agrega la cantidad de filas eliminadas por filas enteras vacías.
    Por último, agrega la grilla original a esta grilla creada anteriormente.
    """
    
    contador_filas_llenas = 0
    puntaje = 0
    for fila in range(len(juego)):
        if not "O" in juego[fila - contador_filas_llenas] and not "P" in juego[fila - contador_filas_llenas]:
            juego.pop(fila - contador_filas_llenas)
            puntaje += 100
            contador_filas_llenas += 1
    juego_nuevo = []

    for filas_nuevas in range(contador_filas_llenas):
        fila_vacia = []
        for vacíos in range(ANCHO_JUEGO):
            fila_vacia.append("O")
        juego_nuevo.append(fila_vacia)

    for filas in juego:
        juego_nuevo.append(filas)
       
    
    return juego_nuevo, contador_filas_llenas, puntaje


def buscar_rotacion(pieza_en_origen, rotaciones):
    for elemento in rotaciones:
        if pieza_en_origen in rotaciones[elemento]:
            indice = rotaciones[elemento].index(pieza_en_origen)
            if not indice == len(rotaciones[elemento]) - 1:
                return rotaciones[elemento][indice + 1]
            return rotaciones[elemento][0]
            
            

def rotar(juego, rotaciones):
    pieza_ordenada = sorted(pieza_actual(juego))
    coor_x, coor_y = pieza_ordenada[0]
    pieza_trasladada_origen = trasladar_pieza(pieza_ordenada, -coor_x, -coor_y)
    siguiente_rotacion = buscar_rotacion(pieza_trasladada_origen, rotaciones)
    pieza_girada = trasladar_pieza(siguiente_rotacion, coor_x, coor_y)
    
    if (siguiente_rotacion[3][0] + coor_x) > (ANCHO_JUEGO - 1):
        pieza_girada = trasladar_pieza(pieza_girada, -((siguiente_rotacion[3][0] + coor_x) - (ANCHO_JUEGO - 1)), 0)
    
    juego_nuevo = []
    for linea in juego:
        juego_nuevo.append(list(linea[:]))
    
    contador_movimiento = 0
    for coordenada_x, coordenada_y in pieza_girada:
        if not coordenada_y > 17 and not coordenada_y < 0 and not hay_superficie(juego, coordenada_x, coordenada_y) and not coordenada_y + 1 == ALTO_JUEGO:
            contador_movimiento += 1
        if contador_movimiento == 4:
            for coordenada_x, coordenada_y in pieza_ordenada:
                juego_nuevo[coordenada_y][coordenada_x] = "O"
            for coordenada_x, coordenada_y in pieza_girada:
                juego_nuevo[coordenada_y][coordenada_x] = "P"
            return juego_nuevo, False
            
            
    return juego_nuevo, False                  
    
    
def guardar(juego, puntaje, pieza):
    puntaje_guardado = puntaje
    pieza_guardada = pieza
    with open("juego.csv", "w") as juego_guardado:
        csv_writer = csv.writer(juego_guardado)
        for linea in juego:
            csv_writer.writerow(linea)
    return puntaje_guardado, pieza_guardada
            
            
def cargar(juego):
    juego_cargado = []
    with open("juego.csv", "r") as cargado:
        csv_reader = csv.reader(cargado)
        for fila in csv_reader:
            if fila != []:
                juego_cargado.append(fila)
    return juego_cargado               
            

def avanzar(juego, siguiente_pieza):
    """
    Avanza al siguiente estado de juego a partir del estado actual.
    
    Devuelve una tupla (juego_nuevo, cambiar_pieza) donde el primer valor
    es el nuevo estado del juego y el segundo valor es un booleano que indica
    si se debe cambiar la siguiente_pieza (es decir, se consolidó la pieza
    actual con la superficie).
    
    Avanzar el estado del juego significa:
     - Descender una posición lpuntuaciona pieza actual.
     - Si al descender la pieza no colisiona con la superficie, simplemente
       devolver el nuevo juego con la pieza en la nueva ubicación.
     - En caso contrario, se debe
       - Consolidar la pieza actual con la superficie.
       - Eliminar las líneas que se hayan completado.
       - Cambiar la pieza actual por siguiente_pieza.

    Si se debe agregar una nueva pieza, se utilizará la pieza indicada en
    el parámetro siguiente_pieza. El valor del parámetro es una pieza obtenida 
    llamando a generar_pieza().

    **NOTA:** Hay una simplificación respecto del Tetris real a tener en
    consideración en esta función: la próxima pieza a agregar debe entrar 
    completamente en la grilla para poder seguir jugando, si al intentar 
    incorporar la nueva pieza arriba de todo en el medio de la grilla se
    pisara la superficie, se considerará que el juego está terminado.

    Si el juego está terminado (no se pueden agregar más piezas), la funcion no hace nada, 
    se debe devolver el mismo juego que se recibió.
    """
    juego_nuevo = []
    puntaje = 0
    for fila in juego:
        juego_nuevo.append(fila)
            
    pieza = pieza_actual(juego)
    contador_pieza_avanza = 0
    contador_pieza_colocable = 0

    if terminado(juego):
        return juego, False, puntaje
    
    for posicion_x, posicion_y in pieza:
        if not posicion_y + 1 == len(juego):
            if not hay_superficie(juego, posicion_x, posicion_y + 1):
                contador_pieza_avanza += 1
            
        if contador_pieza_avanza == 4:
            pieza_trasladada = trasladar_pieza(pieza, 0, 1)
            
            for coordenada in pieza:
                juego_nuevo[coordenada[1]][coordenada[0]] = "O"
            for coordenada in pieza_trasladada:
                juego_nuevo[coordenada[1]][coordenada[0]] = "P"
                
            return juego_nuevo, False, puntaje

        elif posicion_y + 1 == len(juego) or hay_superficie(juego, posicion_x, posicion_y + 1):
            for posicion_x, posicion_y in pieza:
                    juego_nuevo[posicion_y][posicion_x] = "X"
            
            juego_final, contador, puntaje = eliminar_filas(juego_nuevo)
            
            for posicion_x, posicion_y in siguiente_pieza:
                if juego_final[posicion_y][posicion_x + (len(juego_final[0]) // 2)] == "O":
                    contador_pieza_colocable += 1
                if contador_pieza_colocable == 4:                      
                    pieza_centrada = trasladar_pieza(siguiente_pieza, ANCHO_JUEGO // 2, 0)
                    for posicion_x, posicion_y in pieza_centrada:
                        juego_final[posicion_y][posicion_x] = "P"
                    
                
            if contador_pieza_colocable != 4:
                juego_final[0][0] = "T"
                    
            
            return juego_final, True, puntaje
        


def terminado(juego):
    """
    Devuelve True si el juego terminó, es decir no se pueden agregar
    nuevas piezas, o False si se puede seguir jugando.
    """
    if juego[0][0] == "T":
        return True
    return False


def best_scores(nuevo_jugador, puntaje_actual):
    puntajes = []
    nueva_puntuacion = {}
    if path.exists("puntajes.txt"):
        with open("puntajes.txt", 'r') as puntuaciones:
            for fila in puntuaciones:
                fila = fila.rstrip(")\n").lstrip("(").split(",")
                fila[0] = fila[0].strip("'")
                puntajes.append(fila)
            for jugador_actual in puntajes:
                jugador, puntaje = jugador_actual
                nueva_puntuacion[jugador] = int(puntaje)


                if int(puntaje) < puntaje_actual:
                    nueva_puntuacion[nuevo_jugador] = puntaje_actual
                    nueva_puntuacion = dict(sorted(nueva_puntuacion.items(), key=lambda item: item[1]))
                elif len(puntajes) < 10:
                    nueva_puntuacion[nuevo_jugador] = puntaje_actual
                    nueva_puntuacion = dict(sorted(nueva_puntuacion.items(), key=lambda item: item[1]))
                        
            if len(nueva_puntuacion) > 10:
                for nombre in nueva_puntuacion:
                    nueva_puntuacion.pop(nombre)
                    nueva_puntuacion = dict(sorted(nueva_puntuacion.items(), key=lambda item: item[1], reverse=True))
                    return nueva_puntuacion
            elif puntajes == []:
                nueva_puntuacion[nuevo_jugador] = puntaje_actual
                return nueva_puntuacion
            nueva_puntuacion = dict(sorted(nueva_puntuacion.items(), key=lambda item: item[1], reverse=True))
            return nueva_puntuacion
    
    nueva_puntuacion[nuevo_jugador] = puntaje_actual
    return nueva_puntuacion


def escribir_puntajes(diccionario):
    with open("puntajes.txt", "w") as texto:
        for linea in diccionario.items():
            texto.write(f"{linea}\n")
            
def scores_actuales():
    scores_actuales = []
    if path.exists("puntajes.txt"):
        with open("puntajes.txt", "r") as puntajes:
            for fila in puntajes:
                fila = fila.rstrip(")\n").lstrip("(").split(",")
                fila[0] = fila[0].strip("'")
                scores_actuales.append(fila)
        return scores_actuales
        


    