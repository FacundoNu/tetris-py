import os.path as path
import tetris
import gamelib

ESPERA_DESCENDER = 16


def main():
    # Inicializar el estado del juego
    gamelib.resize(660, 920)
    puntaje = 0
    juego = tetris.crear_juego(tetris.generar_pieza())
    pieza_nueva = tetris.generar_pieza()
    scores_actuales = tetris.scores_actuales()

    timer_bajar = ESPERA_DESCENDER
    while gamelib.loop(fps=30):
        gamelib.draw_begin()
        gamelib.draw_rectangle(0, 0, 660, 920, outline='white', fill='grey')
        gamelib.draw_rectangle(10, 10, 460, 910, outline='white', fill='black')
        gamelib.draw_text('Próxima pieza', 560, 30, size = 15, fill = "black")
        gamelib.draw_text('Puntaje:', 560, 300, size = 20, fill = "black")
        gamelib.draw_text(puntaje, 560, 350, size = 18, fill = "black")
        for coordenada_x, coordenada_y in pieza_nueva:
            gamelib.draw_rectangle(485 + (coordenada_x * 50), 50 + (coordenada_y * 50), 535 + (coordenada_x * 50), 100 + (coordenada_y * 50), fill = "white")
        for linea in range(len(juego)):
            for columna in range(len(juego[0])):
                if juego[linea][columna] == "P":
                    gamelib.draw_rectangle(10 + columna * 50, 10 + linea * 50, 10 + columna * 50 + 50, 10 + linea * 50 + 50)
                if juego[linea][columna] == "X":
                    gamelib.draw_rectangle(10 + columna * 50, 10 + linea * 50, 10 + columna * 50 + 50, 10 + linea * 50 + 50, fill = "grey")
        gamelib.draw_text('TOP 10:', 560, 420, size = 20, fill = "black")
        if path.exists("puntajes.txt"):
            for indices_jugadores in range(len(scores_actuales)):
                gamelib.draw_text(f'{scores_actuales[indices_jugadores][0]}', 500, (460 + (30 * indices_jugadores)), size = 15, fill = "black")
                gamelib.draw_text(f'{scores_actuales[indices_jugadores][1]}', 600, (460 + (30 * indices_jugadores)), size = 15, fill = "black")

        
        if tetris.terminado(juego):
            nombre_jugador = gamelib.input("Game Over, ingresa tu nombre: ")
            nombres = []
            if path.exists("puntajes.txt"):
                for jugadores in scores_actuales:
                    nombres.append(jugadores[0])
                while nombre_jugador in nombres:
                    nombre_jugador = gamelib.input("Este nombre ya fue utilizado, usa otro: ")
                


        # Dibujar la pantalla
        gamelib.draw_end()
        
        if not tetris.terminado(juego):
            for event in gamelib.get_events():
              if not event:
                  break
              if event.type == gamelib.EventType.KeyPress:
                  tecla = event.key
                  # Actualizar el juego, según la tecla presionada 
                  if tecla == 'w':
                      juego, _ = tetris.rotar(juego, tetris.PIEZAS)
                  
                  if tecla == 's':
                      puntaje += 1
                      juego, cambiar_pieza, puntaje_borrado = tetris.avanzar(juego, pieza_nueva)
                      puntaje += puntaje_borrado
                      if cambiar_pieza:
                          pieza_nueva = tetris.generar_pieza()
                    
                      
                      
                      
                      
                  if tecla == 'a':
                      juego = tetris.mover(juego, tetris.IZQUIERDA)
                  if tecla == 'd':
                      juego = tetris.mover(juego, tetris.DERECHA)
                  
                  if tecla == 'g':
                      puntaje_guardado, pieza_guardada = tetris.guardar(juego, puntaje, pieza_nueva)
                      
                  if tecla == 'c':
                      juego = tetris.cargar(juego)
                      puntaje = puntaje_guardado
                      pieza_nueva = pieza_guardada
                      


            
            timer_bajar -= 1
            if timer_bajar == 0:
                
                juego, cambiar_pieza, puntaje_borrado = tetris.avanzar(juego, pieza_nueva)
                puntaje += puntaje_borrado
                
                
                if cambiar_pieza:
                    pieza_nueva = tetris.generar_pieza()
                    

                
                timer_bajar = ESPERA_DESCENDER
                # Descender la pieza automáticamente

        else:
            diccionario = tetris.best_scores(nombre_jugador, puntaje)
            tetris.escribir_puntajes(diccionario)
            break
            
            
            

gamelib.init(main)