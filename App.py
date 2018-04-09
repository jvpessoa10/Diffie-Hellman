import socket
import threading
from DHCalculator import *
from getIp import *
LOCAL_IP = ""

calculator = DHCalculator()

class Handler(threading.Thread):
    def __init__(self,local_host,local_port):
        threading.Thread.__init__(self,name="messenger_receiver")
        self.host = local_host
        self.port = local_port
        self.dhRecived = ""

    def listen(self):
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
                    self.dhRecived = full_message
                    if not data:
                        print("key:",calculator.calcularKey(int(self.dhRecived)))
                        break
            finally:
                connection.shutdown(2)
                connection.close()
    def run(self):
        self.listen()
        
class Sender(threading.Thread):
    def __init__(self,remote_host,remote_port,dh):
        threading.Thread.__init__(self,name="messenger_sender")
        self.host = remote_host
        self.port = remote_port
        self.dh = dh

    def run(self):
        message = self.dh
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                s.connect((self.host,self.port))
            except:
                continue
            else:
                s.sendall(message.encode("utf-8"))
                s.shutdown(2)
                s.close()
                break
            
def execute():
    a = int(input("Type your local key:\n>> "))
    A = str(calculator.calcularA(a))
    localport = int(input("LocalPORT:"))
    remotehost = input("remoteIP:")
    remoteport = int(input("remotePORT:"))
    print("Waiting for other pear")
    receiver = Handler(LOCAL_IP,localport)
    sender = Sender(remotehost,remoteport,A)
    treads = [receiver.start(), sender.start()]

def main():
    LOCAL_IP = get_lan_ip()
    dialog = input("Your IP is: "+str(LOCAL_IP)+"?(y/n)\n>>")
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
            





            
        
    
