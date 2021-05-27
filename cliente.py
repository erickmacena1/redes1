import socket
import pickle


def Main():
    # local host IP '127.0.0.1'
    host = '127.0.0.1'

    # Define a porta pela qual vai conectar
    port = 10000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # conecta ao sevidor na rede local
    s.connect((host, port))

    # pedido que vai ser enviado ao servidor
    message = input()
    while True:

        # pedido enviado ao servidor
        s.send(message.encode())
        print('Pedido enviado')

        # primeira resposta recebida do cliente
        data_msg = s.recv(1024)

        # verifica qual mensagem recebida
        if str(data_msg.decode()) == '#01':
            # caso seja a primeira resposta, ele envia o score da partida, armazenando no servidor
            score = input()
            s.send(score.encode())
            print('Enviado score')
            break

        elif str(data_msg.decode()) == '#02':
            # caso seja a segunda resposta, ele pede o scoreboard, printando na tela
            data_sco = s.recv(1024)
            rec_sco = pickle.loads(data_sco)
            print(rec_sco)
            break
        # caso o usuário tenha enviado, um código inválido, ele fecha a conexão
        else:
            print('Código inválido, tente novamente')
            break

    # fecha a conexão
    s.close()

if __name__ == '__main__':
    Main()