#CONSTANTES DE DIMENSIONES
ALTO    = 30
ANCHO   = 45

#CONSTANTES DE DIRECCIONES
IZQUIERDA   = -1
DERECHA     =  1
ARRIBA      =  1
ABAJO       = -1

#CONSTANTES DE PEROSNAJES 
VACIO       = 0
JUGADOR     = 1
ROBOT       = 2
ESCOMBRO    = 3

import random

def generar_jugador():
    """devuelve una lista con un par de valores [y,x] que es la posicion donde va a estar 
    el jugador al principio """
    x = random.randint(0, ANCHO - 1)
    y = random.randint(0,ALTO - 1)
    return x, y
def crear_tablero():
    """en esta funcion lo que vamos a hacer es crear la grilla donde va a ocurrir el juego
    vamos a empezar el juego con una grilla vacia, en este caso representada por el 
    valor 0 como aclaramos en las constantes del principio """

    #vamos a hacer una lista por comprension para el tablero 
    tablero = [[VACIO] * ANCHO for i in range(ALTO)]
    return tablero
print(crear_tablero()[27][43])
def crear_juego():
    """esta funcion inicializa el estado del juego, con la psoicion del jugador, y la grilla 
    o tablero donde vana a estar los escombros y los robots en un principio va a estar vacia 
    como estamos creando el juego, el mismo no esta temrinado, o sea wqu ela funcion terminado(juego) devuelve False"""
     
    jugador   = generar_jugador()
    tablero = crear_tablero()  
    nivel     = 1
    
    juego = jugador, tablero, nivel
    return juego 

def agregar_escombro(escombros, x, y):
    tablero[y][x] = ESCOMBRO

def agregar_escombro(tablero, x, y):
    tablero[y][x] = ROBOT

def hay_escombro(juego, x, y):
    jugador, tablero, nivel = juego
    if tablero[y][x] == ESCOMBRO:
        return True
    return False

def hay_robot(tablero, x, y):
    jugador, tablero, nivel = juego
    if tablero[y][x] == ROBOT:
        return True
    return False

def trasladar_jugador(jugador, dx, dy):
    x, y = jugador 
    x   += dx
    y   += dy
    return x, y   


def 

def terminado(juego):
    """el juego termina cuadno el jugador se choca con un robot, o sea, una vez que en la posicion 
    x,y hay un robot y el jugador a la vez"""
    jugador, tablero, nivel = juego
    posx, posy              = jugador
    if hay_robot(juego, posx, posy):
        return True
    return False
