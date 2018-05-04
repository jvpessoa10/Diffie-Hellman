from math import sqrt
from itertools import count, islice

    

class DHCalculator:
    def __init__(self):
        self.a = 0
        self.B = 0
        self.P = 0
        
    
    def isPrime(self,n):
        return n > 1 and all(n%i for i in islice(count(2), int(sqrt(n)-1)))
    def generateGP(self):

        import random
        minN = 1000
        maxN = 10000
        cached_primes = [i for i in range(minN,maxN) if self.isPrime(i)]

        return random.choice([i for i in cached_primes if minN<i<maxN])

    def setA(self,a):
        self.a = a

    def calcularA(self,G,P):
        #retorna A
        return G**self.a%P

    def calcularKey(self,B,P):
        return B**self.a%self.P
