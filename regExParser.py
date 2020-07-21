import pygame
import sys
from graphviz import Digraph
from pygame.locals import *

index = 1

def debugPrint(*args):
    toPrint = ''
    
    for thing in args:
        toPrint += str(thing) + ' '
    
    print ('DEBUG: ' + toPrint)


# This is used for expressions of type M*
def starOperator(graph):

    graph.transitionList.append(tuple([graph.initialState, graph.finalState, '&']))
    graph.transitionList.append(tuple([graph.finalState, graph.initialState, '&']))
    return graph


# This is used for expressions of type L|R
def orOperator(graphOne, graphTwo):
    global index
    
    graphResult = graph()
    graphResult.nodesList = graphOne.nodesList + graphTwo.nodesList
    graphResult.transitionList = graphOne.transitionList + graphTwo.transitionList
    
    graphResult.nodesList.append(index)
    graphResult.transitionList.append(tuple([index, graphOne.initialState, '&']))
    graphResult.transitionList.append(tuple([index, graphTwo.initialState, '&']))
    graphResult.initialState = index
    index += 1

    graphResult.nodesList.append(index)
    graphResult.transitionList.append(tuple([graphTwo.finalState, index, '&']))
    graphResult.transitionList.append(tuple([graphOne.finalState, index, '&']))
    graphResult.finalState = index
    index += 1
    
    return graphResult


# This is used for expressions of type LR
def andOperator(graphOne, graphTwo):

    graphResult = graph()
    
    graphResult.initialState = graphOne.initialState
    graphResult.finalState = graphTwo.finalState
    
    graphResult.nodesList = graphOne.nodesList + graphTwo.nodesList
    graphResult.transitionList = graphOne.transitionList + graphTwo.transitionList
    graphResult.transitionList.append(tuple([graphOne.finalState, graphTwo.initialState, '&']))
    
    return graphResult


class	graph:

    def __init__(self):
    
        self.initialState = 0 # Initial state of the graph
        self.currentState = 0 # Used to check if a word can pass through the graph
        self.finalState = 0 # Final state 
        self.nodesList = list() # List of nodes 
        self.transitionList = list() # List of transitions, lt = [(A - the exit point, B - the entry point, L - the letter or symbol that connects A and B), ...] 


    # Appends a new transition to the graph
    def appendTransition(self, exitPoint, entryPoint, letter):
    
        self.transitionList.append(tuple([exitPoint, entryPoint, letter]))

    
    # Appends a new node to the graph
    def appendNode(self, nod):
    
        self.nodesList.append(nod)

    
    # Draws the single node graph with colored transition
    def graphDraw(self, name = 'graph', transition = None, color = 0):

        if color == 0:
            color = 'black'
        elif color % 3 == 0:
            color = 'red'
        elif color % 3 == 1:
            color = 'green'
        elif color % 3 == 2:
            color = 'blue'
            
        
        drawing = Digraph('automata', filename = name)
        drawing.attr('graph', size = '10, 4!')
        drawing.attr('graph', dpi = '100')
        drawing.attr('graph', rankdir="LR")
        
        drawing.attr('node', shape = 'none')
        drawing.node('', width = '0!')
        
        if (isinstance(self.finalState, list) and self.initialState in self.finalState) or self.initialState == self.finalState:
            drawing.attr('node', shape = 'doublecircle')
            drawing.node(str(self.initialState))
        else:
            drawing.attr('node', shape = 'circle')
            drawing.node(str(self.initialState))
        drawing.edge('', str(self.initialState), style = 'dotted', label = 'START')
            
        drawing.attr('node', shape = 'doublecircle')
        if not isinstance(self.finalState, list) and self.initialState != self.finalState:
            drawing.node(str(self.finalState))
        elif isinstance(self.finalState, list):
            for node in self.finalState:
                drawing.node(str(node))
        drawing.attr('node', shape = 'circle')

        for x in range(len(self.transitionList)):
            if self.transitionList[x] == transition:
                drawing.attr('edge', color = color)
            drawing.edge(str(self.transitionList[x][0]), str(self.transitionList[x][1]), str(self.transitionList[x][2]))
            if self.transitionList[x] == transition:
                drawing.attr('edge', color = 'black')
        
        drawing.render(format = 'png', cleanup = True)
    
    
    # Tries to acces everything that can be accesed using an empty string
    def lambdaSolver(self, node, nodeList):
        
        for transition in self.transitionList:
            if transition[1] not in nodeList and transition[0] == node and transition[2] == '&':
                nodeList.append(transition[1])
                self.lambdaSolver(transition[1], nodeList)
    
    def inverseLambdaSolver(self, target):
        
        returnList = list()
        
        for node in self.nodeList:
            auxList = list()
            self.lambdaSolver(node, auxList)
            
            if node != target and target in auxList:
                returnList.append(node)
        
        return returnList


    # Tries to acces everything starting from a given node, using expression (&)*letter(&)*
    def letterSolver(self, node, nodeList, letter, level = 0):
        global visited
        
        if level == 0:
            visited = list()
        else:
            visited.append(node)
            
        lambdaAcces = list()
        self.lambdaSolver(node, lambdaAcces)
        
        # Here we try to acces letter(&)*
        for transition in self.transitionList:
            if transition[1] not in nodeList and transition[1] not in visited and transition[0] == node and transition[2] == letter:
                nodeList.append(transition[1])
                self.lambdaSolver(transition[1], nodeList)
        
        for element in lambdaAcces:
            if element not in nodeList and element not in visited:
                self.letterSolver(element, nodeList, letter, level + 1)
        
        nodeList.sort()
    
    
    # A function that returns the symbols used in the graph
    def symbols(self):
        
        symbols = list()
        
        for transition in self.transitionList:
            if transition[2] not in symbols:
                symbols.append(transition[2])
        
        return symbols
    
    
    # This function transforms the graph from a λ-NFA to a DFA, and returns the result
    def minimisation(self):
    
        DFA = graph()
        symbols = self.symbols()
        
        DFA.initialState = DFA.currentState = [0]
        index = 0
        DFA.nodesList.append([0])
        
        while index < len(DFA.nodesList):
            exitPoint = DFA.nodesList[index]
            
            for symbol in symbols:
                if symbol != '&':
                    entryPoint = list()
                    
                    for node in exitPoint: 
                        self.letterSolver(node, entryPoint, symbol)
                
                    if len(entryPoint) != 0 and tuple([exitPoint, entryPoint, symbol]) not in DFA.transitionList:
                        DFA.appendTransition(exitPoint, entryPoint, symbol)
                        DFA.appendNode(entryPoint)
                    
                    
            index += 1
        
        DFA.finalState = list()
        for node in DFA.nodesList:
            if self.finalState in node and node not in DFA.finalState:
                DFA.finalState.append(node)
        
        DFA.graphDraw()
        return DFA
    
    
    # This checkWord works only for DFAs. If you apply the algorithm with some expressions (especially the '*' operator without minimisation) you may see a recurssion limit.
    def checkWordRecursion(self, word, roadList):
        '''
        This was used to avoid dangerous behaviour, but it worked out fine
        
        if isinstance(self.finalState, list):
            print ('ERROR: You called the checkWordRecurssion on a multi-state DFA!')
        
        
        
        To catch errors, if you change the code, use something like this:
        
        try:
            self.checkWordRecursion(word, list())
        except RecursionError as re:
            print ('ERROR: Recursion Error - maybe you called the function on a NFA or lambda-NFA?')
        '''
        
        if len(word) == 0:
            if isinstance(self.finalState, list) and self.currentState in self.finalState or self.currentState == self.finalState:
                self.currentState = self.initialState
                return roadList
            else:
                self.currentState = self.initialState
                return False
        

        for index in range(len(self.transitionList)):
            if self.transitionList[index][0] == self.currentState and self.transitionList[index][2] == word[0]:
                self.currentState = self.transitionList[index][1]
                roadList.append(self.transitionList[index])
                possibleRoad = self.checkWordRecursion(word[1:], roadList)
                if possibleRoad:
                    return possibleRoad
        return False
   

    def printGraph(self):
    
        out = open('graph.in', 'w')
        out.write (str(len(self.nodesList)) + '\n')
        out.write (str(self.initialState) + '\n')
        out.write (str(self.finalState) + '\n')
        for transition in self.transitionList:
            out.write (str(transition[0]) + ' ' + str(transition[1]) + ' ' + str(transition[2]) + '\n')
        out.close()
    

class	expression:
    specialCh = '()|*' # Special characters
    operations = '|*' # Operations, | - or operator, * - star operator
    parantheses = '()' # Parantheses
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@!?' # The alphabet that can be used in the expression
    
    def __init__(self, expressionText):
    
        self.expression = expressionText
    
    def check(self, expression):
    
        stack = list()
        
        if len(expression) == 0:
            return 1
            
        if expression[0] not in self.alphabet or expression[0] not in self.parantheses:
            return 0
        
        if expression[len(expression) - 1] not in self.alphabet or expression[len(expression) - 1] not in self.parantheses or expression[len(expression) - 1] != '*':
            return 0

        for index in len(self.expression):
            if self.expression[index] not in self.alphabet:
                if self.expression[index] == '(':
                    stack.append(self.expression[index])
                elif self.expression[index] == ')':
                    if stack[len(stack) - 1] == '(':
                        stack.pop()
                elif self.expression[index] == '*':
                    if index < (len(self.expression) - 1) and self.expression[index + 1] not in alphabet or self.expression[index + 1] not in parantheses:
                        return 0
                elif self.expression[index] == '|':
                    if index < (len(self.expression) - 1) and self.expression[index + 1] not in alphabet or self.expression[index + 1] not in parantheses:
                        return 0
        if (len(stack) != 0):
            return 0
        else:
            return 1
    
    def findCharacter(self, string, caracter, surplus = 0):
    
        try:
            poz = string.index(caracter)
            return poz + surplus
        except:
            return -1
    
    def findPair(self, string, poz_init):
    
        stack = list()
        stack.append('(')
        
        for index in range(len(string)):
            if string[index] == '(':
                stack.append('(')
            elif string[index] == ')':
                stack.pop()
            if len(stack) == 0:
                return (index + poz_init + 1)
        
        return -1
        
    def constructTree(self, expression):
        ''' 
        The expression tree will look like the example below:
        [E0, +, [E1, +, [[E2, +, E3] | [E4, + [*, E5]]]]]
        Operations:
        1. L + R (L AND R)
        2. M* (M should be encountered at least 0 times)
        3. L | R (L OR R)
        '''
        
        # Simple expression (no parantheses or operators)
        simple = 1
        
        for letter in self.specialCh:
            if letter in expression:
                simple = 0
                break
        
        if simple == 1:
            return expression
        
        # This thing deals with some special case where we use '|' operator
        if '|' in expression:
            poz = self.findCharacter(expression, '|')
            while (poz != -1):
                if expression[:poz].count('(') == expression[:poz].count(')') and expression[poz + 1:].count('(') == expression[poz + 1:].count(')'):
                    left = self.constructTree(expression[:poz])
                    right = self.constructTree(expression[poz + 1:])
                    return [left, '|', right]
                poz = self.findCharacter(expression[poz + 1:], '|', poz + 1)
            
            
        # Parsing the expression character by chraracter
        # We will use L(eft), M(iddle) and R(ight) to explain the process of parsing the expression
        for index in range(len(expression)):
            if expression[index] in self.specialCh:
                # An expression of type L(M)R is represented by [L, '+', [M, '+', R]]
                if expression[index] == '(':
                    jndex = self.findPair(expression[index + 1:], index)
                    left = self.constructTree(expression[: index])
                    middle = self.constructTree(expression[index + 1 : jndex])
                    
                    if jndex < len(expression) - 2 and expression[jndex + 2] == '|' and expression[jndex + 1] == '*':
                        right = self.constructTree(expression[jndex + 3])
                        middle = ['*', middle]
                        if len(left) == 0 and len(right) != 0: # (M)*|R
                            return [middle, '|', right]
                        else:                                  # L(M)*|R
                            return [left, '+', [middle, '|', right]]
                    elif jndex < len(expression) - 1 and expression[jndex + 1] == '*': 
                        right = self.constructTree(expression[jndex + 2 :])
                        middle = ['*', middle]
                    elif jndex < len(expression) - 1 and expression[jndex + 1] == '|':
                        right = self.constructTree(expression[jndex + 2: ])
                        if len(left) == 0 and len(right) != 0: # (M)*R
                            return [middle, '|', right]
                        else:                                  # L(M)|R
                            return [[left, '+', middle], '|', right]
                    else:
                        right = self.constructTree(expression[jndex + 1 :])

                    if len(left) == 0 and len(right) != 0: # (M)|R
                            return [middle, '+', right]
                    elif len(right) == 0 and len(left) != 0: # M(R)
                        return [left, '+', middle]
                    elif len(left) == 0 and len(right) == 0: # (M)
                        return middle
                    else:                                    # L(M)R
                        return [[left, '+', middle], '+', right]
                    
                # M* is represented by ['*', M]
                elif expression[index] == '*':
                    if index < len(expression) - 1 and expression[index + 1] == '|':
                        left = self.constructTree(expression[: index - 1])
                        middle = ['*', expression[index - 1]]
                        right = self.constructTree(expression[index + 2 :])
                        
                        if len(left) == 0: # L*|R
                            return [middle, '|', right]
                        else: # LM*|R
                            return [[left, '+', middle], '|', right]
                    else:
                        left = self.constructTree(expression[: index - 1])
                        middle = ['*', expression[index - 1]]
                        right = self.constructTree(expression[index + 1:])
                        
                        if len(right) == 0 and len(left) == 0:
                            return middle
                        elif len(right) == 0: # LM*
                            return [left, '+', middle]                            
                        elif len(left) == 0: # M*R
                            return [middle, '+', right]
                        else:                # LM*R
                            return [left, '+', [middle, '+', right]]
                elif expression[index] == '|':
                    left = self.constructTree(expression[: index])
                    right = self.constructTree(expression[index + 1:])
                    return [left, '|', right]

        
    def buildGraph(self, tree):
        global index
        
        if isinstance(tree, str):
            graf = graph()
            graf.nodesList.append(index)
            graf.initialState = index
            for letter in tree:
                graf.transitionList.append(tuple([index, index + 1, letter]))
                graf.nodesList.append(index + 1)
                index += 1
            graf.finalState = index
            index += 1
            return graf

        if tree[1] == '+':
            left = self.buildGraph(tree[0])
            right = self.buildGraph(tree[2])
            return andOperator(left, right)
        if tree[1] == '|':
            left = self.buildGraph(tree[0])
            right = self.buildGraph(tree[2])
            return orOperator(left, right)
        if tree[0] == '*':
            graf = self.buildGraph(tree[1])
            graf = starOperator(graf)
            return graf
    
    def rezolve(self, filename = ''):
        
        if self.check(self.expression):
            print ('Expression is not valid!')
            return -1
        
        tree = self.constructTree(self.expression)
        graph = self.buildGraph(tree)
        graph.nodesList.append(0)
        graph.transitionList.append(tuple([0, graph.initialState, '&']))
        graph.initialState = 0
        graph.graphDraw('not-minimised')
        graph.printGraph()

        word = ''
        graph = graph.minimisation()
        graph.graphDraw()
        
        if (filename != ''):
            
            file = open(filename, 'r')
            line = file.readline()
            linesNo = 1
            
            while line:
                line = line.split()
                appearances = 0
                
                for word in line:
                    if graph.checkWordRecursion(word, list()):
                        appearances += 1
                
                if appearances:
                    print ('Found ' + str(appearances) + ' matches on line ' + str(linesNo) + '.')
                line = file.readline()
                linesNo += 1
            
            file.close()
                    
            
        else:
            pygame.init()
            white = (255, 255, 255)
            display_surface = pygame.display.set_mode((1000, 600))
            pygame.display.set_caption('RegExp2NFA')
                
            image = pygame.image.load('graph.png')
            display_surface.blit(image, (0, 0))
            pygame.display.update()
            tickTime = pygame.time.get_ticks()
            word = ''
            previousWord = ''
            roadList = list()
            while True:
                display_surface.fill(white)
                display_surface.blit(image, (0, 0))
                for event in pygame.event.get():
                    if event.type == KEYDOWN and roadList != False and len(roadList) == 0:
                        if event.unicode.isalpha():
                            word += event.unicode
                        elif event.key == K_BACKSPACE:
                            word = word[:-1]
                        elif event.key == K_RETURN:
                            roadList = graph.checkWordRecursion(word, list())
                            transitionIndex = 1
                            if roadList:
                                print ('Word matched!')
                            else:
                                print ('No match found, sorry!')
                                roadList = list()
                            word = ""
                    elif event.type == QUIT:
                        pygame.quit() 
                        quit()
                        
                if roadList != False and len(roadList) == 0 and len(word) > 0 and word != previousWord:
                    print (word)
                    previousWord = word
                
                pygame.display.update()
                if (pygame.time.get_ticks() > tickTime + 1000):
                    image = pygame.image.load('graph.png')
                    display_surface.blit(image, (0, 0))
                    pygame.display.update()
                    tickTime = pygame.time.get_ticks()
                    if len(roadList) == 0:
                        graph.graphDraw()
                    if roadList != False and len(roadList) > 0:
                        graph.graphDraw('graph', roadList[0], transitionIndex)
                        roadList = roadList[1:]
                        transitionIndex += 1


# The main function
if __name__ == "__main__":
    if (len(sys.argv) != 3 and len(sys.argv) != 4):
        print ('Usage: python ' + str(sys.argv[0]) + ' {-f <filename> | -e expression} [<filename>]')
    elif (sys.argv[1] == '-f'):
        file = open(sys.argv[2], 'r')
        ex = expression(file.readline())
        if (len(sys.argv) == 4):
            ex.rezolve(sys.argv[3])
        else:
            ex.rezolve()
        file.close()
    elif (sys.argv[1] == '-e'):
        ex = expression(sys.argv[2])
        if (len(sys.argv) == 4):
            ex.rezolve(sys.argv[3])
        else:
            ex.rezolve()
        
