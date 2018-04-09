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
                    self.dataRecived = full_message
                    global G
                    global P
                    print(G,P)
                    if not data:
                        if(FIRST_CONNECTION_FLAG):
                            print(calculator.G,calculator.P)
                        else:
                            GPRecived = self.dataRecived.split(",")
                            G = GPRecived[0]
                            P = GPRecived[1]
                            print(P,G)
                        break
            finally:
                connection.shutdown(2)
                connection.close()
    def run(self):
        self.listen()
        
class Sender(threading.Thread):
    def __init__(self,remote_host,remote_port,a):
        threading.Thread.__init__(self,name="messenger_sender")
        self.host = remote_host
        self.port = remote_port
        self.a = a

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        global FIRST_CONNECTION_FLAG
        message = ""
        global G
        global P
        while True:
            
            try:
                s.connect((self.host,self.port))
            except Exception:
                FIRST_CONNECTION_FLAG = True
            else:
                if(FIRST_CONNECTION_FLAG):
                    calculator.generateGP()
                    message = str(calculator.G)+","+str(calculator.P)
                s.sendall(message.encode("utf-8"))
                s.shutdown(2)
                s.close()
                break
            
def execute():
    a = int(input("Type your local key:\n>> "))
    localport = int(input("LocalPORT:"))
    remotehost = input("remoteIP:")
    remoteport = int(input("remotePORT:"))
    print("Waiting for another peer")
    receiver = Handler(LOCAL_IP,localport)
    sender = Sender(remotehost,remoteport,a)
    treads = [receiver.start(), sender.start()]

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
            





            
        
    
