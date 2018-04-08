import socket
import threading
from DHCalculator import *
from getIp import *

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

def main():
    print(get_lan_ip())
    dialog = input("Your IP is:",get_lan_ip()"?(y/n)\n>>")
    if(dialog == "y"):
        continue
    elif(dialog == "n"):
        dialog = input("Local IP:\n>>")
    else:
        print("Invalid input!")
        main()
    a = int(input("Type your local key:\n>> "))
    A = str(calculator.calcularA(a))
    print("Waiting for other pear")
    localport = int(input("LocalPORT:"))
    receiver = Handler(dialog,localport)
    remotehost = input("remoteIP:")
    remoteport = int(input("remotePort"))
    sender = Sender("192.168.0.22",remoteport,A)
    treads = [receiver.start(), sender.start()]


if __name__ == "__main__":
    main()
            





            
        
    
