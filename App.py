import p2pservice
G = 3
P = 5

def calculoDH(a):
    return G**a%P
def main():
    a = input("Digite sua chave secreta:\n>> ")
    A = calculoDH(a)
    print("O valor a ser transmitido e: " + str(A))
    localhost = input("LocalIP:")
    localport = input("LocalPORT:")
    receiver = Receiver(localhost,localport)
    remotehost = input("remoteIP:")
    remoteport = input("remotePort")
    sender = Sender(remotehost,remoteport)
    treads = [receiver.start(), sender.start()]
    
if __name__ == "__main__":
    main()
