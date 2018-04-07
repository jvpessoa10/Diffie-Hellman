class DHCalculator:
    def __init__(self):
        self.G = 3
        self.P = 5
        self.a = 0
    
    def calcularA(self,a):
        self.a = a
        self.A = self.G**a%self.P
        return self.A
    def calcularKey(self,B):
        self.B = B
        return B**self.a%self.P
