class DHCalculator:
    def __init__(self):
        self.G = 3527
        self.P = 4409
    
    def calcularA(self,a):
        self.a = a
        self.A = self.G**a%self.P
        return self.A
    def calcularKey(self,B):
        self.B = B
        return B**self.a%self.P
