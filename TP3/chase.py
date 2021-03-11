#CONSTANTES DE DIMENSIONES
ALTO    = 30
ANCHO   = 45

#CONSTANTES DE DIRECCIONES
IZQUIERDA   = -1
DERECHA     = 1
ARRIBA      = -1
ABAJO       = 1

#CONSTANTES DE PERSONAJES 
VACIO       = 0
JUGADOR     = 1
ROBOT       = 2
ESCOMBRO    = 3
CANTIDAD_ROBOTS_BASE = 10 # Cantidad de robots que habrá en el juego en el nivel 1.

#CONSTANTES DE DIBUJADO
ANCHO_INTERFAZ = 1350
ALTO_INTERFAZ = 1050
ANCHO_Y_ALTO_CELDA = 30
MARGEN_SUPERIOR = 150

import random
import gamelib

#- Modificar la funcion trasladar_jugador para que cuando se mueva el jugador hacia x celda, si en esa x celda habia un escombro, el jugador "empuje" el escombro una posición hacia la dirección que se movio el jugador.
#- Pasar 
#Funciones principales

def crear_juego(nivel=1):
    """
    Esta función inicializa el estado del juego, con la posición del jugador, y la grilla 
    o tablero donde vana a estar los escombros y los robots en un principio va a estar vacia 
    como estamos creando el juego, el mismo no esta temrinado, o sea wqu ela funcion terminado(juego) devuelve False
    """

    jugador   = generar_celda_aleatoria()
    tablero = crear_tablero()

    juego = jugador, tablero, nivel
    juego = agregar_robots(juego)
    return juego 

def agregar_robots(juego):
    """
    Esta función se encarga de agregar los robots a la grilla, generando posiciones aleatorias mediante la funcion generar_celda_aleatoria
    y para determinar la cantidad de robots a agregar tiene en cuenta el nivel del juego. En el nivel 1 iniciamos con 10 robots y se van sumando otros
    10 por cada nivel que pasa (Nivel 1 = 10 Robots, Nivel 2 = 20 Robots, Nivel 3 = 30 Robots).
    
    Esta implementación tiene un problema y es que en el caso de que el jugador se encuentre en la misma celda donde se genero un robot,
    el robot tomara su lugar. Una posible solucion podria ser en el caso de que sean iguales, se le sume 1 cada coordenada del robot,
    pero esto tiene el riesgo de que se nos vaya del tablero.
    """
    jugador, tablero, nivel = juego

    for i in range(CANTIDAD_ROBOTS_BASE*nivel):
        celda = generar_celda_aleatoria()
        if celda != jugador:
            tablero[celda[1]][celda[0]] = 2
        if celda == jugador:
            tablero[celda[1]+1][celda[0]+1] = 2
    return juego

def trasladar_jugador(juego, dx, dy):
    """
    Esta función se encarga de tomar las coordenadas x e y donde el usuario clickeo, verifica en que dirección se tiene que mover al jugador
    y lo mueva 1 bloque en dicha dirección.
    """
    jugador, tablero, nivel = juego
    #Proceso las coordenadas y averiguo en que celda clickeo.
    x, y = int(dx//ANCHO_Y_ALTO_CELDA), int((dy-MARGEN_SUPERIOR)//ANCHO_Y_ALTO_CELDA)
    x_jugador, y_jugador = jugador
    
    if x == x_jugador and y == y_jugador:
        return jugador
    elif x == x_jugador:
        if y > y_jugador:
            jugador = x_jugador, y_jugador + ABAJO 
        else:
            jugador = x_jugador, y_jugador + ARRIBA

    elif y == y_jugador:
        if x > x_jugador:
            jugador = x_jugador+DERECHA, y_jugador
        else:    
            jugador = x_jugador+IZQUIERDA, y_jugador


    elif x > x_jugador and y > y_jugador:
        jugador = x_jugador+ABAJO, y_jugador+ABAJO

    elif x < x_jugador and y < y_jugador:
        jugador = x_jugador+ARRIBA, y_jugador+ARRIBA

    elif x > x_jugador and y < y_jugador:
        jugador = x_jugador+DERECHA, y_jugador+ARRIBA
        

    elif x < x_jugador and y > y_jugador:
        jugador = x_jugador+IZQUIERDA, y_jugador+ABAJO
    
    return jugador


def mover_escombro(juego, x, y):
    return 0


def teletransportar_jugador(juego):
    """
    Esta función se encarga de teletransportar al jugador a una celda aleatoria del tablero.
    """
    jugador, tablero, puntaje = juego
    jugador = generar_celda_aleatoria()

    return jugador, tablero, puntaje

def perseguir_a_jugador(juego):
    jugador, tablero, nivel = juego 
    for y in range(len(tablero)):
        for x in range(len(tablero[0])):
            if hay_robot(juego, x, y):
                juegonuevo = acercar_robot(x, y, juego)
                juego = juegonuevo
    return juego

def avanzar(juego):
    jugador, tablero, nivel = juego 
    x_jugador, y_jugador = jugador
    if not terminado(juego):
        juego = perseguir_a_jugador(juego)

        if tablero_sin_robots(juego):
            nivel += 1
            juego = crear_juego(nivel)

    return juego 

def terminado(juego):
    """el juego termina cuadno el jugador se choca con un robot, o sea, una vez que en la posicion 
    x,y hay un robot y el jugador a la vez"""
    posx, posy = juego[0][0], juego[0][1]

    if hay_robot(juego, posx, posy):
        return True
    return False



#Funciones auxiliares
def hay_n(juego, n, x, y):
    """
    Esta función sirve para averiguar si en una celda dada por parámetro, se encuentra un elemento n que puede ser, por ejemplo, ROBOT o ESCOMBRO. 
    Devuelve True si esta ahí o false si no lo esta.
    """
    jugador, tablero, nivel = juego
    return tablero[y][x] == n

def tablero_sin_robots(juego):
    jugador, tablero, nivel = juego
    for y in range(len(tablero)):
        for x in range(len(tablero[0])):
            if hay_robot(juego, x, y):
                return False
    return True


def acercar_robot(x, y, juego):
    jugador, tablero, nivel = juego 
    x_jugador, y_jugador = jugador
    x_resultante = x_jugador - x
    y_resultante = y_jugador - y 

    if x_resultante == 0 and y_resultante == 0 :
        return juego
   
    #Si Y_Resultante es = 0, significa que el jugador y el robot estan en la misma columna, por lo que solo me muevo en x.
    elif x_resultante != 0 and y_resultante == 0 :
        x_final = x_resultante/abs(x_resultante)
        tablero[y][x] = VACIO
        if tablero[y][x + int(x_final)] == ESCOMBRO or tablero[y][x + int(x_final)] == ROBOT:
            tablero[y][x + int(x_final)] = ESCOMBRO
        else:
            tablero[y][x + int(x_final)] = ROBOT
        juego = jugador, tablero, nivel
        return juego

    #Si X_Resultante es = 0, significa que el jugador y el robot estan en la misma columna, por lo que solo me muevo en Y.
    elif x_resultante == 0 and y_resultante != 0:
        y_final = y_resultante/abs(y_resultante)
        tablero = actualizar_tablero(VACIO, tablero, x, y)
        
        if tablero[y + int(y_final)][x] == ESCOMBRO or tablero[y + int(y_final)][x] == ROBOT:
            tablero[y + int(y_final)][x] = ESCOMBRO
        else:
            tablero[y + int(y_final)][x] = ROBOT
        juego = jugador, tablero, nivel
        return juego
    
    #Si X_Resultante e Y_Resultante  es = 0, significa que el jugador y el robot estan en la misma columna, por lo que solo me muevo en x.
    elif x_resultante != 0 and y_resultante != 0:
        x_final = x_resultante/abs(x_resultante)
        y_final = y_resultante/abs(y_resultante)
        tablero = actualizar_tablero(VACIO, tablero, x, y)
        
        
        if tablero[y + int(y_final)][x + int(x_final)] == ESCOMBRO or tablero[y + int(y_final)][x + int(x_final)] == ROBOT:
            tablero[y + int(y_final)][x + int(x_final)] = ESCOMBRO
        else:
            tablero[y + int(y_final)][x + int(x_final)] = ROBOT     
        juego = jugador, tablero, nivel
        return juego
    
def buscar_n_en_tablero(n, tablero):
    """
    Esta función se encarga de buscar un elemento n dado por parámetro, dentro del tablero del juego, tambien dado por 
    parámetro, y devuelve las coordenadas X e Y de nuestra grilla en las que se encuentra dicho valor. 
    """
    resultado = []
    for fila in range(len(tablero)):
        for columna in range(len(tablero[fila])):
                posicion = columna, fila
                if tablero[fila][columna] == n:
                    resultado.append(posicion)
     
    return resultado 

def crear_tablero():
    """
    Esta función se encarga de crear la grilla donde va a ocurrir el juego.
    Vamos a empezar el juego con una grilla vacia, en este caso representada por el 
    valor 0 como aclaramos en las constantes del principio.
    """ 
    tablero = [[VACIO] * ANCHO for i in range(ALTO)]
    return tablero

def actualizar_tablero(n, tablero, x, y):
    """
    Esta función auxiliar se encarga de modificar el tablero que guarda el estado del juego actual 
    cambiando la celda elegida por el valor N dado por parámetro.
    Esta función puede ser utilizada para, por ejemplo, modificar el estado de una celda cuando 2 robots se chochan entre si,
    """
    tablero[y][x] = n
    
    return tablero

def generar_celda_aleatoria():
    """
    Esta función devuelve una tupla con un par de valores (x, y) aleatorios dentro del tablero.
    """
    return random.randint(0, ANCHO - 1), random.randint(0,ALTO - 1)



#Funciones de dibujado
def dibujar_pantalla_de_inicio():
    """
    Esta función se encarga de dibujar la pantalla de inicio del juego.
    """
    gamelib.draw_image('media/logointro.gif', 275, ALTO_INTERFAZ//25)
    gamelib.draw_image('media/boton.gif', (ANCHO_INTERFAZ//2)-MARGEN_SUPERIOR, (ALTO_INTERFAZ - ALTO_INTERFAZ//5))
    gamelib.draw_text('Jugar', ANCHO_INTERFAZ//2, (ALTO_INTERFAZ//2+ALTO_INTERFAZ//3+15), anchor = 'c', size = 30)
    
def dibujar_grilla():
    #Dibujo los bordes del juego.
    gamelib.draw_polygon([0, MARGEN_SUPERIOR, ANCHO_INTERFAZ, MARGEN_SUPERIOR, ANCHO_INTERFAZ, ALTO_INTERFAZ, 0, ALTO_INTERFAZ], outline='white', fill='white')
    
    #Dibujo columnas.
    for i in range(ANCHO):
        gamelib.draw_line(0+i*ANCHO_Y_ALTO_CELDA, MARGEN_SUPERIOR, 0+i*ANCHO_Y_ALTO_CELDA, ALTO_INTERFAZ, fill='black', width=1)
        
    #Dibujo filas.
    for i in range(ALTO):
        gamelib.draw_line(0, MARGEN_SUPERIOR+i*ANCHO_Y_ALTO_CELDA, ANCHO_INTERFAZ, MARGEN_SUPERIOR+i*ANCHO_Y_ALTO_CELDA, fill='black', width=1)

def dibujar_panel_superior(juego):
    """
    Esta función se encarga de dibujar todo lo que se encuentra en la parte superior del tablero del juego.
    """
    #Dibujo logo del juego
    gamelib.draw_image("media/logo.gif", ANCHO_INTERFAZ//2-200, 0)

    #Dibujo boton de teletransportación.
    gamelib.draw_image("media/botonchico.gif", 100, (MARGEN_SUPERIOR/2)/2)
    gamelib.draw_text("Teleport",200,MARGEN_SUPERIOR/2, size = 20)

    #Dibujo nivel
    gamelib.draw_text("Nivel:", ANCHO_INTERFAZ-250, MARGEN_SUPERIOR/2, size = 20)
    gamelib.draw_text(juego[2], ANCHO_INTERFAZ-200, MARGEN_SUPERIOR/2, size = 20)

def dibujar_juego(juego):
    """
    Esta función se encarga de dibujar la grilla del juego, los escombros que hay en la grilla
    """
    gamelib.draw_rectangle(0, 0, ANCHO_INTERFAZ, ALTO_INTERFAZ, fill='black')
    #Dibujo panel superior
    dibujar_panel_superior(juego)

    #Dibujo grilla
    dibujar_grilla()

    #Dibujo robots.
    robots = buscar_n_en_tablero(2, juego[1])
    for i in range(len(robots)):
        x_celda, y_celda = robots[i][0], robots[i][1]
        gamelib.draw_image("media/robot.gif", ANCHO_Y_ALTO_CELDA*x_celda, MARGEN_SUPERIOR+ANCHO_Y_ALTO_CELDA*y_celda)
    
    #Dibujo escombros
    escombros = buscar_n_en_tablero(3, juego[1])
    for i in range(len(escombros)):
        x_celda, y_celda = escombros[i][0], escombros[i][1]
        gamelib.draw_image("media/escombros.gif", ANCHO_Y_ALTO_CELDA*x_celda, MARGEN_SUPERIOR+ANCHO_Y_ALTO_CELDA*y_celda)

    #Dibujo jugador
    jugador = juego[0]
    x_celda, y_celda = jugador[0], jugador[1]
    gamelib.draw_image("media/astronauta.gif", 1+ANCHO_Y_ALTO_CELDA*x_celda, MARGEN_SUPERIOR+ANCHO_Y_ALTO_CELDA*y_celda)

def dibujar_game_over():
    """
    Esta función dibuja en pantalla un cartel que indica game over en pantalla una vez que ha terminado el juego 
    y le pregunta al usuario si quiere volver a jugar.
    """
    gamelib.draw_rectangle(0, 0, ANCHO_INTERFAZ, ALTO_INTERFAZ, fill='black')
    gamelib.draw_text('GAME OVER', ANCHO_INTERFAZ//2, ALTO_INTERFAZ//2 - MARGEN_SUPERIOR//2, size = 80, fill = 'red')
    gamelib.draw_image('media/boton.gif', ANCHO_INTERFAZ//2-MARGEN_SUPERIOR, ALTO_INTERFAZ//2+50)
    gamelib.draw_text('Volver', ANCHO_INTERFAZ//2, ALTO_INTERFAZ//2+80, size = 20)
    gamelib.draw_text('a jugar', ANCHO_INTERFAZ//2, ALTO_INTERFAZ//2+110, size = 20)

def dibujar_ganaste():
    """
    Esta función dibuja en pantalla un cartel que indica que el jugador ganó el juego, esto ocurrira cuando pase de nivel.
    """
    gamelib.draw_rectangle(0, 0, ANCHO_INTERFAZ, ALTO_INTERFAZ, fill='black')
    gamelib.draw_text('¡GANASTE!', ANCHO_INTERFAZ//2, ALTO_INTERFAZ//2 - MARGEN_SUPERIOR//2, size = 80, fill = 'green')
    gamelib.draw_image('media/boton.gif', ANCHO_INTERFAZ//2-150, ALTO_INTERFAZ//2+50)
    gamelib.draw_text('Volver', ANCHO_INTERFAZ//2, ALTO_INTERFAZ//2+80, size = 20)
    gamelib.draw_text('a jugar', ANCHO_INTERFAZ//2, ALTO_INTERFAZ//2+110, size = 20)
