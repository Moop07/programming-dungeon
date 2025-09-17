token_table = {
    "+" : ("PLUS", "+"),
    "-" : ("MINUS", "-"),
    "/" : ("DIVIDE", "/"),
    "*" : ("MULTIPLY", "*"),
    "(" : ("OPEN BRACKET", "("),
    ")" : ("CLOSE BRACKET", ")"),
    ";" : ("SEMICOLON", ";"),
    "let" : ("DEFINE VARIABLE", "let"),
    "=" : ("ASSIGN", "="),
    "if" : ("IF", "if"),
    "==" : ("EQUALS", "=="),
    "{" : ("OPEN CURLY", "{"),
    "}" : ("CLOSE CURLY", "}"),
    "for" : ("FOR LOOP", "for"),
    "while" : ("WHILE LOOP", "while"),
    "," : ("COMMA", ","),
    "print" : ("NATIVE FUNCTION", "print"),
    "factorial" : ("NATIVE FUNCTION", "factorial"),
    "sqroot" : ("NATIVE FUNCTION", "sqroot"),
    "move_player_up" : ("NATIVE FUNCTION", "move_player_up"),
    "move_player_down" : ("NATIVE FUNCTION", "move_player_down"),
    "move_player_left" : ("NATIVE FUNCTION", "move_player_left"),
    "move_player_right" : ("NATIVE FUNCTION" , "move_player_right")
}
def tokenise(token_string):
    output = []
    if token_string.isdigit():
        return (("INTEGER", int(token_string)))
    elif token_string in token_table:
        return token_table[token_string]
    else:
        return ("UNDEFINED", token_string)
