# Regular Expression Parser

### Description

This is a simple Regular Expression parser written in Python. It applies concepts of Automata Theory (started as a homework for the Formal Languages and Automata course - but I cleaned the code and added some extra options), converting the Regular Expression into an expression tree used to build a λ-NFA that is minimised into a DFA - both the λ-NFA and DFA versions will be available, you can see them as .pngs in the source folder. The program also has a GUI that will show you the way the words are verified (avaible only for keyboard input).

### Usage:

    python regExParser.py {-f <filename> | -e expression} [<filename>]

You have to choose one of the first two options, these allow you to take the expression from a file or to enter it from the keyboard. The third option is optional, you can enter the name of a text file if you want to verify it for pattern matches - if you don't write anything for the third parameter the program will let you enter words from the keyboard and the GUI will start.

The expression can use the following operators:

    () - parantheses.
    
    | - the OR operator. If we write L|R, with L and R being two expressions, the words accepted will be the words that are accepted by either L or R.
    
    * - the STAR operator. If we write (E)*, the words accepted are the one that are accepted by 0 or more occurences of E.
    
    Concatenations is done by simply putting two expression togehter.
    
#### Examples of expressions and the words that they generate, in a semi-scientific notation:
    
    abc - {abc}, just a single word
    
    a(bb)*c - {a(b)^(2n)c | n being any natural number greater or equal to 0}
    
    (aa)* - {a^(2n) | n being any natural number greater or equal to 0}
    
    (ab)*|(ba)* - {(ab)^n | n being any natural number greater or equal to 0} U {(ba)^n | n being any natural number greater or equal to 0}
    

    
### Dependecies:
* Python 3+ to run it.
* Graphviz for it to generate the graph image - you must have graphviz installed and added to `PATH`, while also running `pip install graphviz`. 
* Pygame to draw windows and display the graph - just use `pip install pygame`.
