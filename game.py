import pygame
import time
import random

# Toda aplicação precisa desse init, que retorna algumas informações sobre os arquivos da biblioteca, mas nada importante até então
pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)

display_width = 800
display_height = 600

# Criação da tela principal e título da janela
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Snake')

# Variável que vai ditar a quantidade de vezes que nosso loop vai iterar por segundo
clock = pygame.time.Clock()
FPS = 30

font = pygame.font.SysFont(None, 25)

def message_to_screen(msg,color):
    screen_text = font.render(msg, True, color)
    # blit é o método que desenha textos na tela, semelhante ao draw e fill
    gameDisplay.blit(screen_text, [display_width/2, display_height/2])

def gameLoop():
    gameExit = False
    gameOver = False

    block_size = 10

    # localização da cabeça da cobra ( ͡° ͜ʖ ͡°)
    lead_x = display_width / 2
    lead_y = display_height / 2

    # Controle de movimento da cobra ( ͡° ͜ʖ ͡°)
    lead_x_change = 0
    lead_y_change = 0

    # Posição inicial da maçã
    randAppleX = round(random.randrange(0, display_width - block_size) / 10) * 10
    randAppleY = round(random.randrange(0, display_height - block_size) / 10) * 10

    while not gameExit:

        while gameOver:
            gameDisplay.fill(white)
            message_to_screen("You Died, press C to play again or Q to quit", red)
            # update é o metodo que, depois das alterações serem ditadas, desenha uma tela inteira (Frame)
            pygame.display.update()

            # Maneira como nós gerenciamos eventos (Mouse, Ponteiros, Teclas, Pressionar, Soltar...)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            # Verifica qual tecla foi pressionada e muda as variáveis de controle de movimento
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    lead_y_change = block_size
                    lead_x_change = 0
        
        # Altera a posição da cobra a cada loop, pois ela tem que se mover sem parar
        lead_x += lead_x_change
        lead_y += lead_y_change

        # Limita a área do jogo
        if lead_x == display_width or lead_x == -block_size  or lead_y == 600 or lead_y == -block_size:
            gameOver = True

        # Limpa a tela preenchendo o background por cima de tudo
        gameDisplay.fill(white)
        # Desenha a comida
        pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, block_size, block_size])
        # Desenha a cobra
        pygame.draw.rect(gameDisplay, green, [lead_x, lead_y, block_size, block_size])
        # Atualiza o Frame em sí
        pygame.display.update()

        if lead_x == randAppleX and lead_y == randAppleY:
            print("om nom nom")

        # Controle de FRAMES
        clock.tick(FPS)

    message_to_screen("You Lose, go outside you fool", red)
    pygame.display.update()
    time.sleep(2)
    pygame.quit()
    quit()

gameLoop()