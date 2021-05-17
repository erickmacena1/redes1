# import socket programming library
import socket
  
# import thread module
from _thread import *
import threading
  
print_lock = threading.Lock()
positions = ['1', '2', '3']
scoreboard = []
msg_01 = '#01'
msg_02 = '#02'
msg_05 = '#05'
msg_err = 'Error'
  
# função que adiciona ao scoreboard
def add_to_scoreboard(c):
    while True:
  
        # data received from client
        data = c.recv(1024)
        if not data:
            print('Conexão encerrada')
              
            # lock released on exit
            print_lock.release()
            break
  
        # receber a tupla enviada pelo cliente
        scoreboard.append(data.decode())
        scoreboard.sort()

    # connection closed
    c.close()

#função que envia o scoreboard
def send_scoreboard(c):           

    for x in positions:
        c.send(x.encode())
    for y in scoreboard:
        c.send(y.encode())
  
    # connection closed
    c.close()
  
def select_options(c):
    while True:

        # recebe os dados do cliente, caso não receba nada, ele abre a conexão
        data = c.recv(1024)
        print(data.decode())
        if not data:
            print('Conexão encerrada')
                
            # lock released on exit
            print_lock.release()
            break

        #de acordo com a opção enviada pelo cliente, ele envia para uma outra função
        if data.decode() == '1':
            print('Recieved message 1')
            c.send(msg_01.encode())
            add_to_scoreboard(c)

        elif data.decode() == '2':
            print('Recieved message 2')
            c.send(msg_02.encode())
            send_scoreboard(c)

        else:
            print('Recieved error')
            c.send(msg_err.encode())

        break
    c.close()


def Main():
    host = "localhost"
  
    #atribui à porta 10000
    port = 10000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket acionado a porta", port)
  
    # o socket passa a escutar por conexões
    s.listen(3)
    print("socket está ouvindo")
  
    # loop infinito até o cliente sair
    while True:
  
        # estabelece uma conexão com o cliente
        c, addr = s.accept()
  
        # printa que fechou conexão com o cliente
        print_lock.acquire()
        print('Conectado em :', addr[0], ':', addr[1])
  
        # inicia uma nova thread
        start_new_thread(select_options, (c,))
    s.close()
  
  
if __name__ == '__main__':
    Main()