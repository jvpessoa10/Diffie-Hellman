from math import sqrt
from itertools import count, islice

    
G = 0
P = 0
class DHCalculator:
    def __init__(self):
        self.B = 0

    def isPrime(self,n):
        return n > 1 and all(n%i for i in islice(count(2), int(sqrt(n)-1)))
    def generateGP(self):
        global G
        global P

        import random
        minN = 1000
        maxN = 10000
        cached_primes = [i for i in range(minN,maxN) if self.isPrime(i)]

        G = random.choice([i for i in cached_primes if minN<i<maxN])
        P = random.choice([i for i in cached_primes if G<i<maxN])
        
    def defineGP(a,b):
        global G
        global P
        G = a
        P = b


    def calcularA(self,a):
        self.a = a
        self.A = G**a%P
        return self.A

    def calcularKey(self,B):
        self.B = B
        return B**self.a%P
