import re

class token:
    def __init__(self, type, value = None):
        self.type = type
        self.value = value

class interpreter:
    def __init__(self, text):
        self.text = re.findall(r'\w+|[^\w\s]', text)
        print(self.text)
        self.token_list = []
        self.current_token = None
    
    def tokeniser(self):
        #token_string refers to the token while it is a string, also known as a lexeme
        for token_string in self.text:
            if token_string.isdigit(): #if the token is a number
                self.token_list.append(token("INTEGER", int(token_string)))
            elif token_string == "+":
                self.token_list.append(token("PLUS"))
            else:
                raise ValueError(f'''Could not parse token "{token_string}"''')
|
    def get_next_token(self):
        del self.token_list[0]
        return self.token_list[0]

    def evaluate_expression(self):
        #for now this can only handle INT + INT expressions#
        self.tokeniser()
        self.current_token =self.token_list[0]

        #get the left number and move to the next token
        left = self.current_token
        self.current_token = self.get_next_token()

        #get the operator and move to the next token
        operator = self.current_token
        self.current_token = self.get_next_token()

        #finally, get the right number and last token
        right = self.current_token

        if operator.type == "PLUS":
            result = left.value + right.value
        return result


my_interpreter = interpreter("2 - 2")

print(my_interpreter.evaluate_expression())