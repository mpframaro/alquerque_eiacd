#este ficheiro inicia o jogo e recebe o input do jogador

import time
import pygame
from alquerque.constants import WIDTH, HEIGHT, SQUARE_SIZE, WHITE, BLACK
from alquerque.game import Game
from minimax.algorithm import minimax

FPS=60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Alquerque')

def get_row_col_from_mouse(pos):
    x, y, = pos
    row = y//SQUARE_SIZE
    col = x//SQUARE_SIZE
    return row, col

def mainHvH():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    
    while run:
        clock.tick(FPS)

        if game.winner() != None:
            if game.winner()==WHITE:
                print("As peças BRANCAS ganharam!")
                run=False
            else:
                print("As peças PRETAS ganharam!")
                run=False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()

    pygame.quit()

def mainHvP(profundidadeB, tempoB):
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    tempoInicioJogo = time.time()
    
    while run:
        clock.tick(FPS)

        if game.turn==BLACK:                                                                    #ativa o AI
            tempoJogadaP = time.time()
            value, new_board = minimax(game.get_board(), profundidadeB, True, game)            #o segundo argumento do minimax é a profundidade, quanto maior melhor é o AI
            game.ai_move(new_board)
            if tempoB:
                print("Tempo Peças Pretas = %ss" % (time.time()-tempoJogadaP))

        if game.winner() != None:
            if game.winner()==WHITE:
                print("As peças BRANCAS ganharam!")
                print("Tempo Total de Jogo = %ss" % (time.time()-tempoInicioJogo))
                time.sleep(3)
                run=False
            else:
                print("As peças PRETAS ganharam!")
                print("Tempo Total de Jogo = %ss" % (time.time()-tempoInicioJogo))
                time.sleep(3)
                run=False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()

    pygame.quit()

def mainPvP(profundidadeB, profundidadeW, tempoB, tempoW):
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    tempoInicioJogo = time.time()
    
    while run:
        clock.tick(FPS)

        if game.turn==WHITE:    
            tempoJogadaP = time.time()                                                                  #ativa o AI_White
            value, new_board = minimax(game.get_board(), profundidadeW, False, game)            #o segundo argumento do minimax é a profundidade, quanto maior melhor é o AI
            game.ai_move(new_board)
            if tempoW:
                print("Tempo Peças Brancas = %ss" % (time.time()-tempoJogadaP))

        if game.turn==BLACK:                                                                    #ativa o AI_Black
            tempoJogadaP = time.time()  
            value, new_board = minimax(game.get_board(), profundidadeB, True, game)            #o segundo argumento do minimax é a profundidade, quanto maior melhor é o AI
            game.ai_move(new_board)
            if tempoB:
                print("Tempo Peças Pretas = %ss" % (time.time()-tempoJogadaP))



        if game.winner() != None:
            if game.winner()==WHITE:
                print("As peças BRANCAS ganharam!")
                print("Tempo Total de Jogo = %ss" % (time.time()-tempoInicioJogo))
                time.sleep(3)
                run=False
            else:
                print("As peças PRETAS ganharam!")
                print("Tempo Total de Jogo = %ss" % (time.time()-tempoInicioJogo))
                time.sleep(3)
                run=False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()

    pygame.quit()

def inputs():
    modoJogo = int(input('Insira o modo de jogo (1-HumanoVsHumano, 2-HumanoVsPC, 3-PCVsPC): '))

    if modoJogo==1:
        mainHvH()


    elif modoJogo==2:
        tempoB = int(input('Quer ver o tempo de jogada das peças Pretas (0-Não, 1-Sim)? '))
        if tempoB<0 or tempoB>1:
            print('Valor inválido!')
            time.sleep(3)
        else:
            dificuldade = int(input('Insira a dificuldade do PC (1-Fácil, 2-Médio, 3-Difícil, 4-Extremo(lento)): '))
    
            if dificuldade==1:
                mainHvP(1, tempoB)

            elif dificuldade==2:
                mainHvP(2, tempoB)

            elif dificuldade==3:
                mainHvP(3, tempoB)

            elif dificuldade==4:
                mainHvP(5, tempoB)

            else:  
                print('Valor inválido!')
                time.sleep(3)


    elif modoJogo==3:
        tempoB = int(input('Quer ver o tempo de jogada das peças Pretas (0-Não, 1-Sim)? '))
        if tempoB<0 or tempoB>1:
            print('Valor inválido!')
            time.sleep(3)
        else:
            dificuldadeBlack = int(input('Insira a dificuldade das peças pretas (1-Fácil, 2-Médio, 3-Difícil, 4-Extremo(lento)): '))
            if dificuldadeBlack<1 or dificuldadeBlack>4:
                print('Valor inválido!')
                time.sleep(3)
            else:
                tempoW = int(input('Quer ver o tempo de jogada das peças Brancas (0-Não, 1-Sim)? '))
                if tempoW<0 or tempoW>1:
                    print('Valor inválido!')
                    time.sleep(3)

                dificuldadeWhite = int(input('Insira a dificuldade das peças brancas (1-Fácil, 2-Médio, 3-Difícil, 4-Extremo(lento)): '))
                if dificuldadeWhite<1 or dificuldadeWhite>4:
                    print('Valor inválido!')
                    time.sleep(3)
                else:
                    if dificuldadeBlack==1:
                        dificuldadeBlack=1
                    elif dificuldadeBlack==2:
                        dificuldadeBlack=2
                    elif dificuldadeBlack==3:
                        dificuldadeBlack=3
                    elif dificuldadeBlack==4:
                        dificuldadeBlack=5
                    if dificuldadeWhite==1:
                        dificuldadeWhite=1
                    elif dificuldadeWhite==2:
                        dificuldadeWhite=2
                    elif dificuldadeWhite==3:
                        dificuldadeWhite=3
                    elif dificuldadeWhite==4:
                        dificuldadeWhite=5
                    mainPvP(dificuldadeBlack, dificuldadeWhite, tempoB, tempoW)

    else:
        print('Valor inválido!')
        time.sleep(3)


inputs()
