class native_functions:
    def __init__(self):
        self.terminal = ""

    def factorial(self, finput):
        product = 1
        for i in range(2, finput):
            product *= i
        return product
    
    def sqroot(self, finput):
        guess = (finput/7)+1
        for i in range(5):
            guess = (guess + (finput/guess))/2

    def print(self, finput):
        self.terminal += str(finput)
    
    def update_terminal(self):
        output = self.terminal
        self.terminal = ""
        return output
    
    def get_function_names(self):
        return ["factorial", "sqroot", "print"]
