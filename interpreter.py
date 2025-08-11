import re

class token:
    def __init__(self, type, value = None):
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
                self.token_list.append(token("PLUS", "+"))
            elif token_string == "-":
                self.token_list.append(token("MINUS", "-"))
            elif token_string == "/":
                self.token_list.append(token("DIVIDE", "/"))
            elif token_string == "*":
                self.token_list.append(token("MULTIPLY", "*"))
            elif token_string == "(":
                self.token_list.append(token("OPEN BRACKET", "("))
            elif token_string == ")":
                self.token_list.append(token("CLOSE BRACKET", ")"))
            elif token_string == ";":
                self.token_list.append(token("SEMICOLON", ";"))
            elif token_string == "let":
                self.token_list.append(token("DEFINE VARIABLE", "let"))
            elif token_string == "=":
                self.token_list.append(token("ASSIGN", "="))
            else:
                self.token_list.append(token("UNDEFINED", token_string))

        self.token_list.append(token("EOF"))

    def get_next_token(self):
        self.token_index += 1
        self.current_token = self.token_list[self.token_index]

    def evaluate_expression(self):
        expression = "" #to store our expression in
        while self.current_token.type not in ["EOF", "SEMICOLON"]: #if it reaches the end it should stop
            #add on the value of the current token
            expression += f"{self.current_token.value} "
            #advance to the next token
            self.get_next_token()

        return eval(expression)

    def interpret(self):
        self.tokeniser()
        self.current_token = self.token_list[self.token_index]

        while self.current_token.type != "EOF":
            #handles defining variables
            if self.current_token.type == "DEFINE VARIABLE":
                self.get_next_token()
                #token type should be undefined until it's defined as a variable
                if self.current_token.type == "UNDEFINED":
                    variable_name = self.current_token.value
                else:
                    raise Exception("Variable name cannot be identical to another token")
                self.get_next_token()
                #the next token must be "="
                if self.current_token.type != "ASSIGN":
                    raise Exception("Expected '=' to follow variable name")
                self.get_next_token()
                #we evaluate the expression on the other side of the equals sign and assign that as our value
                variable_value = self.evaluate_expression()
                #the next token must be ";"
                if self.current_token.type != "SEMICOLON":
                    raise Exception("Expected ';' to follow variable value")
                
                #temporary until variables are fully implemented
                print(f"defining variable {variable_name} with a stored value of {variable_value}")
            self.get_next_token()



my_interpreter = interpreter(input("> "))

my_interpreter.interpret()
