# import socket programming library
import socket
  
# import thread module
from _thread import *
import threading
  
print_lock = threading.Lock()
positions = ['1°', '2°', '3°']
scoreboard = []
  
# função que adiciona ao scoreboard
def add_to_scoreboard(c):
    while True:
  
        # data received from client
        data = c.recv(1024)
        if not data:
            print('Bye')
              
            # lock released on exit
            print_lock.release()
            break
  
        # receber a tupla enviada pelo cliente
        scoreboard.append(data)

        c.send('#05')
    # connection closed
    c.close()

#função que envia o scoreboard
def send_scoreboard(c):
    while True:
  
        # data received from client
        data = c.recv(1024)
        if not data:
            print('Bye')
              
            # lock released on exit
            print_lock.release()
            break
  
        # send back reversed string to client
        c.send(positions, scoreboard)
  
    # connection closed
    c.close()
  
def select_options(c):
    while True:

        # recebe os dados do cliente, caso não receba nada, ele abre a conexão
        data = c.recv(1024)
        if not data:
            print('Bye')
                
            # lock released on exit
            print_lock.release()
            break

        #de acordo com a opção enviada pelo cliente, ele envia para uma outra função
        if data == '1':
            c.send('#01')
            add_to_scoreboard(data)
        elif data == '2':
            c.send('#02')
            send_scoreboard(c)
        else:
            c.send('Error 01')
            c.close()


def Main():
    host = "localhost"
  
    #atribui à porta 10000
    port = 10000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)
  
    # o socket passa a escutar por conexões
    s.listen(3)
    print("socket is listening")
  
    # loop infinito até o cliente sair
    while True:
  
        # estabelece uma conexão com o cliente
        c, addr = s.accept()
  
        # printa que fechou conexão com o cliente
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])
  
        # inicia uma nova thread
        start_new_thread(select_options, (c,))
    s.close()
  
  
if __name__ == '__main__':
    Main()