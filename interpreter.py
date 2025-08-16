import re
from native_functions import native_functions
native = native_functions()


class token:
    def __init__(self, type, value = None):
        self.type = type
        self.value = value

class interpreter:
    def __init__(self, text):
        self.text = re.findall(r'<=|==|\w+|[^\w\s]', text)
        self.token_list = []
        self.token_index = 0
        self.current_token = None
        self.terminal = ""
        self.variables = {}
        self.native_function_names = native.get_function_names()

        #only used when the interpreter is in a loop
        self.loops = 0
        self.loop_condition_ends = []
        self.loop_condition_starts = []
        self.loop_starts = []

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
            elif token_string == "if":
                self.token_list.append(token("IF"))
            elif token_string == "==":
                self.token_list.append(token("EQUALS", "=="))
            elif token_string == "{":
                self.token_list.append(token("OPEN CURLY"))
            elif token_string == "}":
                self.token_list.append(token("CLOSE CURLY"))
            elif token_string == "for":
                self.token_list.append(token("FOR LOOP"))
            elif token_string == "while":
                self.token_list.append(token("WHILE LOOP"))
            elif token_string == ",":
                self.token_list.append(token("COMMA"))
            elif token_string in self.native_function_names:
                if token_string == "print":
                    self.token_list.append(token("NATIVE FUNCTION", native.print))
                elif token_string == "factorial":
                    self.token_list.append(token("NATIVE FUNCTION", native.factorial))
                elif token_string == "sqroot":
                    self.token_list.append(token("NATIVE FUNCTION", native.sqroot))
            else:
                self.token_list.append(token("UNDEFINED", token_string))

        self.token_list.append(token("EOF"))

    def get_next_token(self):
        #print(self.current_token.value)
        self.token_index += 1
        if self.current_token.type != "EOF":
            self.current_token = self.token_list[self.token_index]
        #print(self.current_token.type)

    def evaluate_expression(self, in_brackets = False):
        expression = "" #to store our expression in
        open_brackets = 0
        while self.current_token.type not in ["EOF", "SEMICOLON", "OPEN CURLY", "COMMA"]: #if it reaches the end it should stop
            if self.current_token.type == "OPEN BRACKET":
                open_brackets += 1
                if in_brackets and open_brackets == 1:
                    self.get_next_token()
                    continue
            elif self.current_token.type == "CLOSE BRACKET":
                open_brackets -= 1
                self.get_next_token()
                break
            if not in_brackets or open_brackets >= 1:
                #add on the value of the current token
                #if the token is a function call we use a recursive function call
                if self.current_token.type == "NATIVE FUNCTION":
                    value = self.handle_native_function(self.current_token.value)
                    expression += f"{value} "
                #if the token is a variable we look up its value in self.variables
                elif self.current_token.type == "VARIABLE":
                    expression += f"{self.variables[self.current_token.value]} "
                else:
                    expression += f"{self.current_token.value} "
                #advance to the next token
                self.get_next_token()

        return eval(expression)
    
    def update_terminal(self):
        self.terminal = native.update_terminal()
        if self.terminal != "":
            print(self.terminal)
            self.terminal = ""

    def handle_native_function(self, function):
        self.get_next_token()
        value = function(self.evaluate_expression(in_brackets = True))
        if self.current_token.type == "CLOSE BRACKET":
            self.get_next_token()
        return value

    def interpret(self):
        self.tokeniser()
        self.current_token = self.token_list[self.token_index]

        while self.current_token.type != "EOF":

            if self.loops > 0:
                if self.token_index == self.loop_condition_ends[-1] -1:
                    self.get_next_token()

            #handles defining variables
            if self.current_token.type == "NATIVE FUNCTION":
                self.handle_native_function(self.current_token.value)
            
            elif self.current_token.type == "DEFINE VARIABLE":
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
                #print(f"defining variable {variable_name} with a stored value of {variable_value}")
                #update the list of tokens as we now know what type of token this name refers to
                for i in self.token_list:
                    if i.value == variable_name:
                        i.type = "VARIABLE"
                #store the variable's name and current value with a key value pair in self.variables
                self.variables.update({variable_name : variable_value})
            
            elif self.current_token.type == "VARIABLE":
                variable_name = self.current_token.value
                self.get_next_token()
                if self.current_token.type != "ASSIGN":
                    #print(self.token_index)
                    raise Exception("Expected '=' to follow variable name")
                self.get_next_token()
                variable_value = self.evaluate_expression()
                if self.current_token.type == "SEMICOLON":
                    pass
                elif self.loops > 0 and self.current_token.type in ("CLOSE BRACKET", "OPEN CURLY"):
                    # for-loop increment ends at ')' (and after 2a we’re actually at '{')
                    pass
                else:
                    raise Exception("Expected ';' to follow variable value")
                self.variables.update({variable_name : variable_value})
            
            elif self.current_token.type == "IF":
                self.get_next_token()
                condition = self.evaluate_expression()
                #if the condition is false we skip over the code entirely
                if condition == False:
                    #since the expression will open with a curly bracket we set open_curlies to 1
                    open_curlies = 1
                    self.get_next_token()
                    #this iterates all the way to the end of the expression
                    while open_curlies > 0:
                        if self.current_token.type == "OPEN CURLY":
                            open_curlies += 1
                        elif self.current_token.type == "CLOSE CURLY":
                            open_curlies -= 1
                            if open_curlies == 0:
                                break
                        elif self.current_token.type == "EOF":
                            raise Exception("If statement was never closed")
                        self.get_next_token()
            
            elif self.current_token.type == "FOR LOOP":
                self.loops += 1
                #correct syntax for a for loop is for (variable = start point, condition, loop operation){code}
                self.get_next_token()
                if self.current_token.type != "OPEN BRACKET":
                    raise Exception("for loop information must be enclosed in parentheses ()")
                self.get_next_token()
                variable_name = self.current_token.value
                self.get_next_token()
                if self.current_token.type != "ASSIGN":
                    raise Exception("Expected '=' to follow variable name")
                self.get_next_token()
                variable_value = self.evaluate_expression()
                self.variables.update({variable_name : variable_value})
                for i in self.token_list:
                    if i.value == variable_name:
                        i.type = "VARIABLE"
                if self.current_token.type != "COMMA":
                    raise Exception("for loop terms must be separated by commas")
                self.get_next_token()
                self.loop_condition_starts.append(self.token_index)
                loop_condition = ""
                while self.current_token.type != "COMMA":
                    loop_condition += str(self.current_token.value)
                    self.get_next_token()
                self.get_next_token()
                #we're now at the starting point of the loop, but we need to skip over the loop operation the first time around
                self.loop_starts.append(self.token_index)
                while self.current_token.type != "CLOSE BRACKET":
                    self.get_next_token()
                self.get_next_token()
                self.get_next_token()
                self.loop_condition_ends.append(self.token_index)
                self.token_index -= 1
                self.current_token = self.token_list[self.token_index]

            elif self.current_token.type == "WHILE LOOP":
                #correct syntax for a while loop is while(condition){code}
                self.loops += 1
                self.get_next_token()
                if self.current_token.type != "OPEN BRACKET":
                    raise Exception("while loop information must be enclosed in parentheses ()")
                self.get_next_token()
                self.loop_condition_starts.append(self.token_index)
                while self.current_token.type != "CLOSE BRACKET":
                    self.get_next_token()
                self.loop_condition_ends.append(self.token_index)
                self.get_next_token()
                self.loop_starts.append(self.token_index)

            
            elif self.current_token.type == "CLOSE CURLY":
                if self.loops > 0:
                    self.token_index = self.loop_condition_starts[-1]
                    self.current_token = self.token_list[self.token_index]
                    if self.evaluate_expression():
                        self.token_index = self.loop_starts[-1]-1
                        self.current_token = self.token_list[self.token_index]
                    else:
                        self.loop_condition_starts.pop()
                        self.loop_condition_ends.pop()
                        self.loop_starts.pop()
                        self.loops -= 1
                        open_curlies = 0
                        #this iterates all the way to the end of the loop
                        while self.current_token.type != "EOF":
                            if self.current_token.type == "OPEN CURLY":
                                open_curlies += 1
                            elif self.current_token.type == "CLOSE CURLY":
                                open_curlies -= 1
                                if open_curlies == 0:
                                    break
                            elif self.current_token.type == "EOF":
                                raise Exception("Loop was never closed")
                            self.get_next_token()
                        
                        

            elif self.current_token.type == "UNDEFINED":
                raise Exception(f"'{self.current_token.value}' is not defined")

            self.update_terminal()
            self.get_next_token()


file = open("player_code.txt", "rt")
code = file.read()

my_interpreter = interpreter(code)
my_interpreter.interpret()

file.close()
