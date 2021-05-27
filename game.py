import socket
import pickle
import time
import random
import os
import pygame


############ CLIENT GLOBALS ############

host = '127.0.0.1'
port = 10000


############ GAME GLOBALS ############


pygame.init()

curr_path = os.path.abspath(os.getcwd())

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Cobrinha')

headImg = pygame.image.load(os.path.join(
    curr_path, "assets", "snake-head.png"))
tailImg = pygame.image.load(os.path.join(
    curr_path, "assets", "snake-tail.png"))
appleImg = pygame.image.load(os.path.join(
    curr_path, "assets", "apple.png"))

pygame.display.set_icon(appleImg)

direction = "up"

block_size = 20
appleThickness = 30

clock = pygame.time.Clock()
FPS = 15

font_path = os.path.join(curr_path, "assets", "PixelEmulator-xq08.ttf")

smallfont = pygame.font.Font(font_path, 18)
medfont = pygame.font.Font(font_path, 42)
largefont = pygame.font.Font(font_path, 60)


############ GAME FUNCTIONS ############


def introScreen():

    gameDisplay.fill(white)
    message_to_screen("Jogo da Cobrinha",
                        green,
                        -150,
                        "large")
    message_to_screen("O objetivo do jogo é comer as maçãs vermelhas",
                        black,
                        -30)
    message_to_screen("Quanto mais maçãs você comer, maior você fica",
                        black,
                        10)
    message_to_screen("Se você se morder ou bater nas paredes, você perde!",
                        black,
                        50)
    message_to_screen("Aperte C para jogar, P para pausar ou Q para sair!",
                        black,
                        140)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_c:
                    gameLoop()

        clock.tick(5)


def score(score):
    text = smallfont.render("Score: " + str(score), True, black)
    gameDisplay.blit(text, [1, 1])


def pause():
    paused = True

    # gameDisplay.fill(white)
    message_to_screen("PAUSADO",
                        green,
                        -100,
                        size="large")
    message_to_screen("Aperte C para continuar ou Q para sair",
                        black,
                        25)
    pygame.display.update()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        clock.tick(5)


def randAppleGen():
    randAppleX = round(random.randrange(0, display_width - appleThickness))
    randAppleY = round(random.randrange(0, display_height - appleThickness))

    return randAppleX, randAppleY


def snake(block_size, snakeList):
    if direction == "right":
        head = pygame.transform.rotate(headImg, 270)
    elif direction == "left":
        head = pygame.transform.rotate(headImg, 90)
    elif direction == "up":
        head = headImg
    else:
        head = pygame.transform.rotate(headImg, 180)

    gameDisplay.blit(head, (snakeList[-1][0], snakeList[-1][1]))

    for XnY in snakeList[:-1]:
        pygame.draw.rect(gameDisplay, green, [
                         XnY[0], XnY[1], block_size, block_size])


def text_objects(text, color, size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    else:
        textSurface = largefont.render(text, True, color)

    return textSurface, textSurface.get_rect()


def message_to_screen(msg, color, y_displace=0, size="small"):
    textSurf, textRect = text_objects(msg, color, size)

    textRect.center = (display_width / 2), (display_height / 2) + y_displace
    gameDisplay.blit(textSurf, textRect)


def score_to_screen(scoreList=[]):
    scoreLen = len(scoreList)

    if scoreLen == 0:
        message_to_screen("Sem pontuações...", red)
    else:
        for i in range(scoreLen):
            message_to_screen("TOP " + str(i + 1) + " - " + str(scoreList[i]),
                          red,
                          y_displace=(i * 35))


def serverComunication(msg, score=-1):
    resposta = ["status", "valor"]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((host, port))
    
    s.send(str(msg).encode())

    data_msg = s.recv(1024)

    msg_decoded = ''

    try:
        msg_decoded = data_msg.decode()
        resposta[0] = "OK"
    except:
        resposta[0] = "DECERR"
        resposta[1] = [score, "Decode Error"]
        return resposta

    if msg_decoded == '#01':
        # caso seja a primeira resposta, ele envia o score da partida, armazenando no servidor
        s.send(str(score).encode().strip())
        resposta[1] = "Score Enviado"
            
    elif msg_decoded == '#02':
        # caso seja a segunda resposta, ele pede o scoreboard, printando na tela
        data_sco = s.recv(1024)
        rec_sco = pickle.loads(data_sco)
        resposta[1] = rec_sco[:4]
        
    # caso o usuário tenha enviado, um código inválido, ele fecha a conexão
    else:
        resposta[0] = "Invalido"
        resposta[1] = "Invalido"
            
    s.close()

    return resposta

def scoreScreen(score):
    resposta1 = serverComunication(1, score)
    
    resposta2 = serverComunication(2)

    scoreList = resposta2[1]
    gameDisplay.fill(white)

    if resposta1[0] != "OK":
        message_to_screen("Erro",
                        green,
                        -200,
                        "large")
        message_to_screen("Inesperado",
                        green,
                        -110,
                        "large")
        message_to_screen(":(",
        green,
        -30,
        "large")

    else:
        message_to_screen("MELHORES",
                        green,
                        -200,
                        "large")

        message_to_screen("PONTUAÇÕES",
                        green,
                        -110,
                        "large")

        score_to_screen(scoreList)

        message_to_screen("Aperte C para tentar se superar",
                        black,
                        150)

        message_to_screen("Aperte Q para sair ou I para voltar a tela inicial",
                        black,
                        190)

    pygame.display.update()

    gameScore = True
    while gameScore:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_c:
                    gameScore = False
                    gameLoop()
                if event.key == pygame.K_i:
                    gameScore = False
                    introScreen()

        clock.tick(5)


def gameLoop():
    global direction

    direction = "up"
    gameExit = False
    gameOver = False

    lead_x = display_width / 2
    lead_y = display_height / 2

    lead_x_change = 0
    lead_y_change = 0

    snakeList = []
    snakeLength = 1

    randAppleX, randAppleY = randAppleGen()

    while not gameExit:

        while gameOver:
            gameDisplay.fill(white)
            message_to_screen("VOCÊ PERDEU",
                              red,
                              y_displace=-100,
                              size="large")

            message_to_screen("Aperte C para jogar de novo ou Q para sair",
                              black,
                              y_displace=50)
            message_to_screen("Para enviar ao servidor aperte E",
                              black,
                              y_displace=90)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = False
                    gameExit = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_e:
                        scoreScreen(snakeLength - 1)
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = "left"
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    direction = "right"
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    direction = "up"
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    direction = "down"
                    lead_y_change = block_size
                    lead_x_change = 0

                elif event.key == pygame.K_p:
                    pause()

        lead_x += lead_x_change
        lead_y += lead_y_change

        if lead_x == display_width or lead_x == -block_size or lead_y == 600 or lead_y == -block_size:
            gameOver = True

        gameDisplay.fill(white)

        gameDisplay.blit(appleImg, (randAppleX, randAppleY))

        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLength:
            del snakeList[0]

        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True

        snake(block_size, snakeList)

        score(snakeLength - 1)

        pygame.display.update()

        if lead_x > randAppleX and lead_x < randAppleX + appleThickness or lead_x + block_size > randAppleX and lead_x + block_size < randAppleX + appleThickness:
            if lead_y > randAppleY and lead_y < randAppleY + appleThickness:
                randAppleX, randAppleY = randAppleGen()
                snakeLength += 1
            elif lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + appleThickness:
                randAppleX, randAppleY = randAppleGen()
                snakeLength += 1

        clock.tick(FPS)

    gameDisplay.fill(white)
    message_to_screen("FIM", green, size="large")
    pygame.display.update()
    time.sleep(2)
    pygame.quit()
    quit()


############ GAME START ############

if __name__ == "__main__":
    introScreen()