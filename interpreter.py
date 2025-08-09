import re

class token:
    def __init__(self, type, value = 0):
        self.type = type
        self.value = value

class interpreter:
    def __init__(self, text):
        self.text = re.findall(r'\w+|[^\w\s]', text)
        self.token_list = []
        self.token_index = 0
        self.current_token = None

    def tokeniser(self):
        #token_string refers to the token while it is a string, also known as a lexeme
        for token_string in self.text:
            if token_string.isdigit(): #if the token is a number
                self.token_list.append(token("INTEGER", int(token_string)))
            elif token_string == "+":
                self.token_list.append(token("PLUS"))
            elif token_string == "-":
                self.token_list.append(token("MINUS"))
            elif token_string == "/":
                self.token_list.append(token("DIVIDE"))
            elif token_string == "*":
                self.token_list.append(token("MULTIPLY"))
            else:
                raise ValueError(f'''Could not parse token "{token_string}"''')

        self.token_list.append(token("EOF"))

    def get_next_token(self):
        self.token_index += 1
        self.current_token = self.token_list[self.token_index]

    def evaluate_expression(self):
        self.tokeniser()
        self.current_token = self.token_list[0]
        value = 0

        while self.current_token.type != "EOF":
            #if the token is an operator we apply that operation to the running total
            #if the token is an integer it is added to the total
            #this is because the first integer should be the only one the interpreter doesn't indirectly skip
            match self.current_token.type:
                case "MINUS":
                    self.token_index += 1
                    self.current_token = self.token_list[self.token_index]
                    value -= self.current_token.value
                case "PLUS":
                    self.token_index += 1
                    self.current_token = self.token_list[self.token_index]
                    value += self.current_token.value
                case "INTEGER":
                    value += self.current_token.value
                case "DIVIDE":
                    self.token_index += 1
                    self.current_token = self.token_list[self.token_index]
                    value /= self.current_token.value
                case "MULTIPLY":
                    self.token_index += 1
                    self.current_token = self.token_list[self.token_index]
                    value *= self.current_token.value
            if self.current_token.type != "EOF":
                self.token_index += 1
                self.current_token = self.token_list[self.token_index]

        return value


my_interpreter = interpreter(input("calc> "))

print(my_interpreter.evaluate_expression())
