# Regular Expression Parser - TBC

### Description

This is a simple Regular Expression parser written in Python. It applies concepts of Automata Theory (started as a homework for the Formal Languages and Automata course), converting the Regular Expression into an expression tree used to build a λ-NFA that is minimised into a DFA. It also has a GUI that will show you the way the words are verified (avaible only for keyboard input).

### Usage:

    python regExParser.py {-f <filename> | -e expression} [<filename>]

The first two options are if you want to take the expression from a file or to enter it from the keyboard. The third option is the optional, if you want to verify a file from the keyboard.

### Dependecies:
* Python 3+ to run it.
* Graphviz for it to generate the graph image.
* Pygame to draw windows and display the graph.
