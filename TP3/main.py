import gamelib
import chase

#CONSTANTES DE DIMENSIONES
ALTO    = 30
ANCHO   = 45

#CONSTANTES DE DIRECCIONES
IZQUIERDA   = -1
DERECHA     =  1
ARRIBA      =  1
ABAJO       = -1

#CONSTANTES DE PERSONAJES 
VACIO       = 0
JUGADOR     = 1
ROBOT       = 2
ESCOMBRO    = 3
ESPERA_DESCENDER = 20

#CONSTANTES DE DIBUJADO
ANCHO_INTERFAZ = 1350
ALTO_INTERFAZ = 1050
ANCHO_Y_ALTO_CELDA = 30
MARGEN_SUPERIOR = 150

def main():
    gamelib.resize(chase.ANCHO_INTERFAZ, chase.ALTO_INTERFAZ)
    gamelib.title("Chase")
    
    while gamelib.is_alive():
        #Dibujo pantalla de inicio
        gamelib.draw_begin()
        chase.dibujar_pantalla_de_inicio()
        gamelib.draw_end()
        timer_bajar = ESPERA_DESCENDER

        # Esperamos hasta que ocurra un evento
        ev = gamelib.wait()
        
        if not ev:
            #El usuario cerró la ventana.
            break
            
        if ev.type == gamelib.EventType.KeyPress and ev.key == 'Escape':
            # El usuario presionó la tecla Escape, cerrar la aplicación.
            break
            
        if ev.type == gamelib.EventType.ButtonPress:
            # El usuario presionó un botón del mouse
            x, y = ev.x, ev.y # averiguamos la posición donde se hizo click
            
            if (x >= ((ANCHO_INTERFAZ//2)-150) and x <= (((ANCHO_INTERFAZ//2)-150)+300)) and (y >= (ALTO_INTERFAZ - ALTO_INTERFAZ//5) and y <= ((ALTO_INTERFAZ - ALTO_INTERFAZ//5)+100)):
                #Creo un un nuevo juego.
                juego = chase.crear_juego()
                chase.agregar_robots(juego)
                while gamelib.loop(fps=30):
                    if not chase.terminado(juego):
                        gamelib.draw_begin()
                        chase.dibujar_juego(juego)
                        gamelib.draw_end()
                        ev = gamelib.wait()
                        if ev.type == gamelib.EventType.ButtonPress:
                            x, y = ev.x, ev.y
                            if (x >= 0 and x <= ANCHO_INTERFAZ) and (y >= MARGEN_SUPERIOR and y <= ALTO_INTERFAZ):
                                jugador, tablero, puntaje = juego
                                jugador = chase.trasladar_jugador(jugador, ev.x, ev.y)
                                juego = jugador, tablero, puntaje
                                juego = chase.perseguir_a_jugador(juego)

                            if (x >= 100 and x <= 300) and (y >= ((MARGEN_SUPERIOR/2)/2) and y <= (MARGEN_SUPERIOR/2)/2+75):
                                juego = chase.teletransportar_jugador(juego) 

                        timer_bajar -= 1
                        if timer_bajar == 0:
                            timer_bajar = ESPERA_DESCENDER
                            # Descender la pieza automáticamente
                            juego = chase.perseguir_a_jugador(juego)
                                
                    elif chase.terminado(juego):
                        gamelib.draw_begin()    
                        chase.dibujar_game_over()
                        gamelib.draw_end()
                        ev = gamelib.wait()

                        if ev.type == gamelib.EventType.ButtonPress:
                            # El usuario presionó un botón del mouse
                            x, y = ev.x, ev.y                          
                            #Verifico si el usuario quiere volver a jugar
                            if (x >= (ANCHO_INTERFAZ//2-150) and x <= ((ANCHO_INTERFAZ//2-150)+200)) and (y >= (ALTO_INTERFAZ//2+50) and y <= ((ALTO_INTERFAZ//2+50)+75)):
                                juego = chase.crear_juego()
                                chase.agregar_robots(juego)
                                
        
gamelib.init(main)
