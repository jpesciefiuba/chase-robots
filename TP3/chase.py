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
"""
Modificaciones:
-> Hice las funciones de dibujado, podriamos cambiar/mejorar varias cosas pero por el momento nos sirve como un MVP (Minimum Viable Product).
-> Borre algunas funciones como por ejemplo agregar_escombro o agregar_robot y las reemplace por una unica funcion auxiliar a la que le tenemos que pasar
por parámetro un N para poner en las coordenadas x, y (en el caso de robots serìa 2, etc.)
-> Modifique la funcion trasladar_jugador para que tome las coordenadas x e y donde el usuario clickeo, verifique en que direccion se tiene que mover al jugador
y lo mueva 1 bloque en dicha direccion.
-> Agregué la función teletransportar que cambia las coordenadas del usuario y en el caso de que se lo teletransporte a una celda con escombros, termine el juego.
-> Modifique la funcion generar_jugador para que no solo la podamos usar para generar una posicion aleatoria para el jugador si no que tambien sirva para generar posiciones 
aleatorias para colocar los robots en el tablero.
-> Agregué la función agregar robots para agregar los robots al tablero del juego una vez que empieza el juego.
Cosas que faltan por implementar:
-> IA para mover a los robots
    -> Funcion que detecte cuando 2 robots choquen y ponga un escombro en esa posicion.
"""
# Funciones principales


def crear_juego(nivel=1):
    """
    Esta función inicializa el estado del juego, con la posición del jugador, y la grilla 
    o tablero donde vana a estar los escombros y los robots en un principio va a estar vacia 
    como estamos creando el juego, el mismo no esta temrinado, o sea wqu ela funcion terminado(juego) devuelve False
    """

    jugador = generar_celda_aleatoria()
    tablero = crear_tablero()

    juego = jugador, tablero, nivel
    juego = agregar_robots(juego)
    return juego


def hay_escombro(juego, x, y):
    jugador, tablero, nivel = juego
    return tablero[y][x] == ESCOMBRO


def hay_robot(juego, x, y):
    jugador, tablero, nivel = juego
    return tablero[y][x] == ROBOT


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
    for i in range(10*nivel):
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
    # Proceso las coordenadas y averiguo en que celda clickeo.
    x, y = int(dx//30), int((dy-150)//30)
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


def teletransportar_jugador(juego):
    """
    Esta función se encarga de teletransportar al jugador a una celda aleatoria del tablero.
    """
    jugador, tablero, nivel = juego
    jugador = generar_celda_aleatoria()
    juego = jugador, tablero, nivel
    return juego 

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
        tablero = actualizar_tablero(VACIO, tablero, x, y)
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
    x = random.randint(0, ANCHO - 1)
    y = random.randint(0,ALTO - 1)
    return x, y
#Funciones de dibujado
def dibujar_pantalla_de_inicio():
    """
    Esta función se encarga de dibujar la pantalla de inicio del juego.
    """
    gamelib.draw_image('media/logointro.gif', 275, ALTO_INTERFAZ//25)
    gamelib.draw_image('media/boton.gif', (ANCHO_INTERFAZ//2)-150, (ALTO_INTERFAZ - ALTO_INTERFAZ//5))
    gamelib.draw_text('Jugar', ANCHO_INTERFAZ//2, (ALTO_INTERFAZ//2+ALTO_INTERFAZ//3+15), anchor = 'c', size = 30)
    
def dibujar_grilla():
    #Dibujo los bordes del juego.
    gamelib.draw_polygon([0, 150, 1350, 150, 1350, 1050, 0, 1050], outline='white', fill='white')
    
    #Dibujo columnas.
    for i in range(ANCHO):
        gamelib.draw_line(0+i*ANCHO_Y_ALTO_CELDA, 150, 0+i*ANCHO_Y_ALTO_CELDA, 1050, fill='black', width=1)
        
    #Dibujo filas.
    for i in range(ALTO):
        gamelib.draw_line(0, 150+i*ANCHO_Y_ALTO_CELDA, 1350, 150+i*ANCHO_Y_ALTO_CELDA, fill='black', width=1)
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
        x_celda = robots[i][0]
        y_celda = robots[i][1]
        gamelib.draw_image("media/robot.gif", ANCHO_Y_ALTO_CELDA*x_celda, 150+ANCHO_Y_ALTO_CELDA*y_celda)
    
    #Dibujo escombros
    escombros = buscar_n_en_tablero(3, juego[1])
    for i in range(len(escombros)):
        x_celda = escombros[i][0]
        y_celda = escombros[i][1]
        gamelib.draw_image("media/escombros.gif", ANCHO_Y_ALTO_CELDA*x_celda, 150+ANCHO_Y_ALTO_CELDA*y_celda)
    #Dibujo jugador
    jugador = juego[0]
    x_celda = jugador[0]
    y_celda = jugador[1]
    gamelib.draw_image("media/astronauta.gif", 1+ANCHO_Y_ALTO_CELDA*x_celda, 150+ANCHO_Y_ALTO_CELDA*y_celda)
def dibujar_game_over():
    """
    Esta función dibuja en pantalla un cartel que indica game over en pantalla una vez que ha terminado el juego 
    y le pregunta al usuario si quiere volver a jugar.
    """
    gamelib.draw_rectangle(0, 0, ANCHO_INTERFAZ, ALTO_INTERFAZ, fill='black')
    gamelib.draw_text('GAME OVER', ANCHO_INTERFAZ//2, ALTO_INTERFAZ//2 - MARGEN_SUPERIOR//2, size = 80, fill = 'red')
    gamelib.draw_image('media/boton.gif', ANCHO_INTERFAZ//2-150, ALTO_INTERFAZ//2+50)
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
    
