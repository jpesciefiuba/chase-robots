#CONSTANTES DE DIMENSIONES
ALTO    = 30
ANCHO   = 45

ANCHO_INTERFAZ = 1500
ALTO_INTERFAZ = 1000

import gamelib

def dibujar_pantalla_de_inicio():
    """
    Esta función se encarga de dibujar la pantalla de inicio del juego. A partir de ella, el jugador podrá iniciar una partida.
    """
    gamelib.draw_image('media/logo.gif', ANCHO_INTERFAZ//2, ALTO_INTERFAZ//3)
    gamelib.draw_text('Bienvenido', ANCHO_INTERFAZ//2, 250)

    #Dibujo los botones
    gamelib.draw_image('media/botonazul.gif',55, 280)
    gamelib.draw_text('Jugar', 115, 310)
    gamelib.draw_image('media/botonrosa.gif', 220, 280)
    gamelib.draw_text('Cargar', 285, 300)
    gamelib.draw_text('partida', 285, 320)

def main():
    gamelib.resize(1500, 1000)

    gamelib.draw_begin()
    gamelib.draw_text('Hello world!', 150, 150)
    dibujar_pantalla_de_inicio()
    gamelib.draw_end()

    gamelib.wait(gamelib.EventType.KeyPress)

gamelib.init(main)