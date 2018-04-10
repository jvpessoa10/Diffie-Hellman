import socket
import threading
from string import *
from DHCalculator import *
from getIp import *

LOCAL_IP = ""
FIRST_CONNECTION_FLAG = False
calculator = DHCalculator()

class Handler(threading.Thread):
    def __init__(self,local_host,local_port):
        threading.Thread.__init__(self,name="messenger_receiver")
        self.host = local_host
        self.port = local_port
        self.dataRecived = ""

    def listen(self):
        global FIRST_CONNECTION_FLAG
        global G 
        global P
        global A
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host,self.port))
        sock.listen(10)
        while True:
            connection, client_address = sock.accept()
            try:
                full_message = ""
                while True:
                    data = connection.recv(16)
                    full_message +=data.decode("utf-8")
                    if not data:
                        if(A >0):
                            print("A recebido",full_message)
                            break
                        if(FIRST_CONNECTION_FLAG == False):
                            if(full_message.count(",") == 1):
                                self.dataRecived =  full_message.split(",")
                                print("data recebida",self.dataRecived)
                                G = self.dataRecived[0]
                                P = self.dataRecived[1]
                                print("P e G transportados:",G,P)
                            print(P,G)
                            A = calculator.calcularA(int(G),int(P))
                            print("A:",A)
                            
                        else:
                            print("G e P gerados:",G,P)
                            A = calculator.calcularA(int(G),int(P))
                            print("A:",A)
                        
            finally:
                connection.shutdown(2)
                connection.close()
    def run(self):
        self.listen()
        
class Sender(threading.Thread):
    def __init__(self,remote_host,remote_port):
        threading.Thread.__init__(self,name="messenger_sender")
        self.host = remote_host
        self.port = remote_port

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        global FIRST_CONNECTION_FLAG
        global G 
        global P
        global A
        message = ""
        while True:
            
            try:
                s.connect((self.host,self.port))
            except Exception:
                FIRST_CONNECTION_FLAG = True
                G = calculator.generateGP()
                P = calculator.generateGP()
            else:
                print("A antes de enviar:", A)
                if(A > 0):
                    print("Condicional")
                    message = str(A)
                    print("mensagem a ser enviada:",message)
                    s.sendall(message.encode("utf-8"))
                    break
                else:
                    message = str(G)+","+str(P)
                    s.sendall(message.encode("utf-8"))
                s.shutdown(2)
                s.close()
                
            
def execute():
    a = int(input("Type your local key:\n>> "))
    calculator.setA(a)
    localport = int(input("LocalPORT:"))
    remotehost = input("remoteIP:")
    remoteport = int(input("remotePORT:"))
    print("Waiting for another peer")
    receiver = Handler(LOCAL_IP,localport)
    sender = Sender(remotehost,remoteport)
    treads = [sender.start(),receiver.start()]

def main():
    LOCAL_IP = get_lan_ip()
    dialog = input("Your IP is: "+LOCAL_IP+"?(y/n)\n>>")
    if(dialog == "y"):
        execute()
    elif(dialog == "n"):
        LOCAL_IP = input("Local IP:\n>>")
        execute()
    else:
        print("Invalid input!")
        main()




if __name__ == "__main__":
    main()
            





            
        
    
