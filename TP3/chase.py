# CONSTANTES DE DIMENSIONES
import gamelib
import random

ALTO = 30
ANCHO = 45
# CONSTANTES DE DIRECCIONES
IZQUIERDA = -1
DERECHA = 1
ARRIBA = -1
ABAJO = 1
# CONSTANTES DE PERSONAJES
VACIO = 0
JUGADOR = 1
ROBOT = 2
ESCOMBRO = 3
# CONSTANTES DE DIBUJADO
ANCHO_INTERFAZ = 1350
ALTO_INTERFAZ = 1050
ANCHO_Y_ALTO_CELDA = 30
MARGEN_SUPERIOR = 150

#otras constantes 
ROBOTS_POR_NIVEL = 10
# Funciones principales


def crear_juego(nivel=1):
    """
    Esta función inicializa el estado del juego, con la posición del jugador, y la grilla
    o tablero donde vana a estar los escombros y los robots en un principio va a estar vacia
    como estamos creando el juego, el mismo no esta temrinado, o sea wqu ela funcion terminado(juego) devuelve False
    """

    jugador = generar_celda_aleatoria()
    tablero = crear_tablero()

    juego = jugador, [], tablero, nivel
    juego = agregar_robots(juego)
    return juego


def hay_escombro(juego, x, y):
    jugador, robots, tablero, nivel = juego
    return tablero[y][x] == ESCOMBRO


def hay_robot(juego, x, y):
    jugador, robots, tablero, nivel = juego
    return (x, y) in robots


def agregar_robots(juego):
    """
    Esta función se encarga de agregar los robots a la grilla, generando posiciones aleatorias mediante la funcion generar_celda_aleatoria
    y para determinar la cantidad de robots a agregar tiene en cuenta el nivel del juego. En el nivel 1 iniciamos con 10 robots y se van sumando otros
    10 por cada nivel que pasa (Nivel 1 = 10 Robots, Nivel 2 = 20 Robots, Nivel 3 = 30 Robots).

    Esta implementación tiene un problema y es que en el caso de que el jugador se encuentre en la misma celda donde se genero un robot,
    el robot tomara su lugar. Una posible solucion podria ser en el caso de que sean iguales, se le sume 1 cada coordenada del robot,
    pero esto tiene el riesgo de que se nos vaya del tablero.
    """
    jugador, robots, tablero, nivel = juego
    robots = []
    for i in range(ROBOTS_POR_NIVEL * nivel):
        celda = generar_celda_aleatoria()
        if celda != jugador:
            robots.append((celda[0], celda[1]))

        elif celda == jugador:
            robots.append((celda[0] + 1, celda[1] + 1))
        

    juego = jugador, robots, tablero, nivel
    return juego


def trasladar_jugador(juego, dx, dy):
    """
    Esta función se encarga de tomar las coordenadas x e y donde el usuario clickeo, verifica en que dirección se tiene que mover al jugador
    y lo mueva 1 bloque en dicha dirección.
    """

    jugador, robots, tablero, nivel = juego
    # Proceso las coordenadas y averiguo en que celda clickeo.
    x, y = int(dx // ANCHO_Y_ALTO_CELDA), int((dy - MARGEN_SUPERIOR) // ANCHO_Y_ALTO_CELDA)
    x_jugador, y_jugador = jugador

    if x == x_jugador and y == y_jugador:
        return juego
    elif x == x_jugador:
        if y > y_jugador:
            jugador, tablero = verificar_escombro(jugador, tablero, 0, ABAJO)
        else:
            jugador, tablero = verificar_escombro(jugador, tablero, 0, ARRIBA)

    elif y == y_jugador:
        if x > x_jugador:
            jugador, tablero = verificar_escombro(jugador, tablero, DERECHA, 0)
        else:
            jugador, tablero = verificar_escombro(jugador, tablero, IZQUIERDA, 0)

    elif x > x_jugador and y > y_jugador:
        jugador, tablero = verificar_escombro(jugador, tablero, DERECHA, ABAJO)

    elif x < x_jugador and y < y_jugador:
        jugador, tablero = verificar_escombro(jugador, tablero, IZQUIERDA, ARRIBA)

    elif x > x_jugador and y < y_jugador:
        jugador, tablero = verificar_escombro(jugador, tablero, DERECHA, ARRIBA)

    elif x < x_jugador and y > y_jugador:
        jugador, tablero = verificar_escombro(jugador, tablero, IZQUIERDA, ABAJO)

    juego = jugador, robots, tablero, nivel

    return juego




def teletransportar_jugador(juego):
    """
    Esta función se encarga de teletransportar al jugador a una celda aleatoria del tablero.
    """
    jugador, robots, tablero, nivel = juego
    x, y = generar_celda_aleatoria()
    jugador = x, y
    juego = jugador, robots, tablero, nivel
    return juego


def perseguir_a_jugador(juego):
    """recibe como parametro el estado anterior del juego, luego recorre la lista de posiciones de robots y las pasa por la funcion aceeercar_robot,
    si la funcion devuelve una tupla, se chequea que esa tupla no este previamente en la lista nueva, si no esta, entonces se la agrega a la nueva lista
    y si esta en la lista, significa que habria uno en la misma posicion y por lo tanto un choque , entonces se remueve el elemento que ya esta en la lista nueva de posiciones de robots
    y se pone un escombro en el lugar x,y de la tupla, la nueva lista se transforma en la lista de psoiciones de robots, y se devuelve el nuevo estado del juego
    y se pone un escombro"""
    jugador, robots, tablero, nivel = juego 
    nuevos_robots = []
    for robot in robots:
        if hay_robot(juego, robot[0], robot[1]):
            tupla = acercar_robot(robot, juego)
            if tupla:
                if tupla in nuevos_robots:
                    x,y = tupla
                    nuevos_robots.remove(tupla)
                    tablero[y][x] = ESCOMBRO
                else:
                    nuevos_robots.append(tupla)
    juego = jugador, nuevos_robots, tablero, nivel
    return juego


def avanzar(juego):
    """cada uno de los robots se acercan al jugador, si uno de los robots choca con el jugador se devuelve el mismo estado, sino, 
    luego se verifica que el tablero ya no tenga robots, sino hay mas, enotnces significa que gano el nivel y se pasa al proximo"""
    jugador, robots, tablero, nivel = juego
    x_jugador, y_jugador = jugador
    if not terminado(juego):
        juego = perseguir_a_jugador(juego)
        if tablero_sin_robots(juego):
            nivel += 1
            juego = crear_juego(nivel)
    return juego


def terminado(juego):
    """
    Esta función se encarga de verificar si el juego ha terminado o no.
    El juego en si no tiene fin, se puede jugar ad infinitum, sin embargo, el juego se puede perder y cuando se pierde se termina el juego.
    Esta funcion verifica si ocurrio algun choque entre un robot y el jugador, y de ser así, da por terminado el juego.
    """
    jugador, robots, tablero, nivel = juego
    x_jugador, y_jugador = jugador
    if hay_n(juego, ROBOT, x_jugador, y_jugador):
        return True
    return False


# Funciones auxiliares
def tablero_sin_robots(juego):
    jugador, robots, tablero, nivel = juego
    return len(robots) == 0


def acercar_robot(robot, juego):
    """la funcion toma al robot y al juego, luego teniendo en cuentea las posiciones del jugador, lo que hacer es encontrar un vecetor que vaya en la direccion 
    desde el robot hacia el jugador, se resta componente a componente con el robot, y se obtiene una x resultante y una y resultante,
    lo que se hace despues es a ese vector dividirlo por su modulo para que solo se mueva 1 cuadro, luego se forma una tupla con los valores x e y finales,
    si la tupla es (0,0) o si en le tablero en esa posicion x,y hay un escombro, se devuelve un None, y si no se devuelve la tula x,y con los valores correspondientes a la operacion"""
    jugador, robots, tablero, nivel = juego 
    x_jugador, y_jugador = jugador

    x = robot[0]
    y = robot[1]

    x_resultante = x_jugador - x
    y_resultante = y_jugador - y


    if x_resultante == 0 and y_resultante == 0 :
        tupla = (x,y)
        return tupla

    #Si Y_Resultante es = 0, significa que el jugador y el robot estan en la misma columna, por lo que solo me muevo en x.

    x_final = int(x_resultante/abs(x_resultante)) if x_resultante != 0 else 0
    y_final = int(y_resultante/abs(y_resultante)) if y_resultante != 0 else 0 

    #Si X_Resultante e Y_Resultante  es = 0, significa que el jugador y el robot estan en la misma columna, por lo que solo me muevo en x.

    if tablero[y + y_final][x + x_final] == ESCOMBRO:
        return None
    else:
        tupla = (x + x_final, y + y_final)
        return  tupla   

    


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
    x = random.randint(0, ANCHO - 1)
    y = random.randint(0, ALTO - 1)
    return x, y

def hay_n(juego, n, x, y):
    """
    Esta función auxiliar permite verificar si en ciertas coordenadas x e y se encuentra o no un N especifico.
    Esta función está pensada para solamente buscar robots y escombros en el juego.
    """
    jugador, robots, tablero, nivel = juego
    if n == ROBOT:
        return (x, y) in robots
    return tablero[y][x] == ESCOMBRO


def verificar_escombro(jugador, tablero, dx, dy):
    """
    Esta función se encarga de, dadas ciertas coordenadas x e y a las cuales el jugador esta intentando moverse, verificar
    si en dichas coordenadas se encuentra un escombro o es una celda vacia. En el caso de que haya un escombro, lo "empujará"
    una celda en la misma dirección y sentido en la que se desplaza el jugador.
    """
    x_jugador, y_jugador = jugador
    if tablero[y_jugador + dy][x_jugador + dx] == ESCOMBRO:
        if  y_jugador + dy * 2 < 0 or y_jugador + dy * 3 > ALTO or x_jugador + dx * 3 > ANCHO or x_jugador + dx * 2 < 0 :
            return jugador, tablero

        tablero[y_jugador + dy][x_jugador + dx] = VACIO
        tablero[y_jugador + dy * 2][x_jugador + dx * 2] = ESCOMBRO
        nuevojugador = x_jugador + dx, y_jugador + dy
    else:
        nuevojugador = x_jugador + dx, y_jugador + dy
    
    return nuevojugador, tablero



#funciones de dibujo

def dibujar_pantalla_de_inicio():
    """
    Esta función se encarga de dibujar la pantalla de inicio del juego.
    """
    gamelib.draw_image('media/logointro.gif', 275, ALTO_INTERFAZ // 25)
    gamelib.draw_image('media/boton.gif', (ANCHO_INTERFAZ // 2) - MARGEN_SUPERIOR, (ALTO_INTERFAZ - ALTO_INTERFAZ // 5))
    gamelib.draw_text('Jugar', ANCHO_INTERFAZ // 2, (ALTO_INTERFAZ // 2 + ALTO_INTERFAZ // 3 + 15), anchor='c', size=30)

def dibujar_grilla():
    # Dibujo los bordes del juego.
    gamelib.draw_polygon([0, MARGEN_SUPERIOR, 1350, MARGEN_SUPERIOR, 1350, 1050, 0, 1050], outline='white', fill='white')

    # Dibujo columnas.
    for i in range(ANCHO):
        gamelib.draw_line(0 + i * ANCHO_Y_ALTO_CELDA, MARGEN_SUPERIOR, 0 + i * ANCHO_Y_ALTO_CELDA, 1050, fill='black', width=1)

    # Dibujo filas.
    for i in range(ALTO):
        gamelib.draw_line(0, MARGEN_SUPERIOR + i * ANCHO_Y_ALTO_CELDA, 1350, MARGEN_SUPERIOR + i * ANCHO_Y_ALTO_CELDA, fill='black', width=1)

def dibujar_panel_superior(juego):
    """
    Esta función se encarga de dibujar todo lo que se encuentra en la parte superior del tablero del juego.
    """
    # Dibujo logo del juego
    gamelib.draw_image("media/logo.gif", ANCHO_INTERFAZ // 2 - 200, 0)
    
    # Dibujo boton de teletransportación.
    gamelib.draw_image("media/botonchico.gif", 100, (MARGEN_SUPERIOR / 2) / 2)
    gamelib.draw_text("Teleport", 200, MARGEN_SUPERIOR / 2, size=20)
    
    # Dibujo nivel
    gamelib.draw_text("Nivel:", ANCHO_INTERFAZ - 250, MARGEN_SUPERIOR / 2, size=20)
    gamelib.draw_text(juego[3], ANCHO_INTERFAZ - 200, MARGEN_SUPERIOR / 2, size=20)

def dibujar_juego(juego):
    """
    Esta función se encarga de dibujar la grilla del juego, los escombros que hay en la grilla
    """
    gamelib.draw_rectangle(0, 0, ANCHO_INTERFAZ, ALTO_INTERFAZ, fill='black')
    
    # Dibujo panel superior
    dibujar_panel_superior(juego)
    
    # Dibujo grilla
    dibujar_grilla()
    
    # Dibujo robots.
    robots = juego[1]
    for robot in robots:
        x_celda, y_celda = robot[0], robot[1]
        gamelib.draw_image("media/robot.gif", ANCHO_Y_ALTO_CELDA * x_celda, MARGEN_SUPERIOR + ANCHO_Y_ALTO_CELDA * y_celda)

    # Dibujo escombros
    escombros = buscar_n_en_tablero(3, juego[2])
    for i in range(len(escombros)):
        x_celda, y_celda = escombros[i][0], escombros[i][1]
        gamelib.draw_image("media/escombros.gif", ANCHO_Y_ALTO_CELDA * x_celda, MARGEN_SUPERIOR + ANCHO_Y_ALTO_CELDA * y_celda)
    
    # Dibujo jugador
    jugador = juego[0]
    x_celda, y_celda = jugador[0], jugador[1]
    gamelib.draw_image("media/astronauta.gif", 1 + ANCHO_Y_ALTO_CELDA * x_celda, MARGEN_SUPERIOR + ANCHO_Y_ALTO_CELDA * y_celda)

def dibujar_game_over():
    """
    Esta función dibuja en pantalla un cartel que indica game over en pantalla una vez que ha terminado el juego
    y le pregunta al usuario si quiere volver a jugar.
    """
    gamelib.draw_rectangle(0, 0, ANCHO_INTERFAZ, ALTO_INTERFAZ, fill='black')
    gamelib.draw_text('GAME OVER', ANCHO_INTERFAZ // 2, ALTO_INTERFAZ // 2 - MARGEN_SUPERIOR // 2, size=80, fill='red')
    gamelib.draw_image('media/boton.gif', ANCHO_INTERFAZ // 2 - MARGEN_SUPERIOR, ALTO_INTERFAZ // 2 + 50)
    gamelib.draw_text('Volver', ANCHO_INTERFAZ // 2, ALTO_INTERFAZ // 2 + 80, size=20)
    gamelib.draw_text('a jugar', ANCHO_INTERFAZ // 2, ALTO_INTERFAZ // 2 + 110, size=20)