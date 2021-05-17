# Import socket module
import socket
  
  
def Main():
    # local host IP '127.0.0.1'
    host = '127.0.0.1'
  
    # Define the port on which you want to connect
    port = 10000
  
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  
    # connect to server on local computer
    s.connect((host,port))
  
    # message you send to server
    message = input()
    while True:
  
        # message sent to server
        s.send(message.encode())
        print('Enviado messagem')
  
        # message received from server
        data_msg = s.recv(1024)

        if str(data_msg.decode()) == '#01':
            score = input()
            s.send(score.encode())
            print('Enviado score')
            break
        
        if str(data_msg.decode()) == '#02':
            data_ans1 = s.recv(1024)
            scoreboard = eval(data_ans1.decode())

            data_ans2 = s.recv(1024)
            positions = eval(data_ans2.decode())

            for a, b in zip(positions, scoreboard):
                print(a, b)
                
            break

    s.close()   
  
if __name__ == '__main__':
    Main()