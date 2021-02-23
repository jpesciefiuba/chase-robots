def main():
    juego = inicializar_juego()
    while not juego.terminado():
        juego.inicializar_siguiente_nivel()
        while not juego.nivel_terminado():
            mostrar_estado_juego(juego)
            accion = pedir_accion_al_jugador()
            juego.avanzar_un_step(accion)
    if juego.ganado():
        mostrar_pantalla_ganador()
    else:
        mostrar_pantalla_perdedor()