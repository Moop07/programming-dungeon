# programming-dungeon
Puzzle game developed as part of my A Level Computer Science non exam assessment

Programming Dungeon is a puzzle game where the player must solve coding problems to clear dungeons. The player lacks the ability to control the character directly, instead they must write code for the character to follow. Each level introduces a new concept, and requires the player to build upon what they have learned previously.

The game is currently unfinished and unplayable. The current version features no gameplay, only programmer art of the menu with limited functionality. While you may select levels there is nothing to do other than type into the text box on the left.

The full version will feature 10-20 levels, an endless mode, and complete graphics


Blackadder is a small scale high level language made for the game. Extensive documentation is below, as well as in the tutorial system in the game
Blackadder documentation

operators:  
plus: +  
minus: -  
multiply: *  
division: /  
integer division: //  
equality: ==  
and: and  
or: or  

The blackadder compiler ignores whitespace and new lines, instead using curly brackets {} and semicolons;  
example:  
while True{  
    pass;  
}  

declare any variable using "let". Blackadder does not support specifying the variable type, this is instead inferred from the input  
example:  
let x = 5;  
print(x + 7);  
>> 12  

define a function using "def"  
example:  
def factorial(n){  
    let total = 1;  
    let i = 1;  
    for(i, i<=n, i = i+1){  
        total = total * i;  
    }  
    return total;  
}  
