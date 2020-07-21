from graphviz import Digraph
from time import sleep
import sys
import pygame
from pygame.locals import *

index = 1

def starOperator(graph):

    graph.transitionList.append(tuple([graph.initialState, graph.finalState, '&']))
    graph.transitionList.append(tuple([graph.finalState, graph.initialState, '&']))
    return graph


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


    def appendTransition(self, exitPoint, entryPoint, letter):
        self.transitionList.append(tuple(exitPoint, entryPoint, letter))


    def appendNode(self, nod):
        self.nodesList.append(nod)


    def graphDraw(self):

        drawing = Digraph('automata', filename = 'graph')
        drawing.attr('graph', size = '10, 4!')
        drawing.attr('graph', dpi = '100')
        drawing.attr('graph', rankdir="LR")
        
        drawing.attr('node', shape = 'none')
        drawing.node('', width = '0!')
        
        if self.initialState == self.finalState:
            drawing.attr('node', shape = 'doublecircle')
            drawing.node(str(self.initialState))
        else:
            drawing.attr('node', shape = 'circle')
            drawing.node(str(self.initialState))
        drawing.edge('', str(self.initialState), style = 'dotted', label = 'START')

        drawing.attr('node', shape = 'doublecircle')
        if self.initialState != self.finalState:
            drawing.node(str(self.finalState))
        drawing.attr('node', shape = 'circle')
        
        for x in range(len(self.transitionList)):
            drawing.edge(str(self.transitionList[x][0]), str(self.transitionList[x][1]), str(self.transitionList[x][2]))
        
        drawing.render(format = 'png')
    
    def graphDrawTransition(self, transition, color):

        if color % 3 == 0:
            color = 'red'
        elif color % 3 == 1:
            color = 'green'
        elif color % 3 == 2:
            color = 'blue'
            
        
        drawing = Digraph('automata', filename = 'graph')
        drawing.attr('graph', size = '10, 4!')
        drawing.attr('graph', dpi = '100')
        drawing.attr('graph', rankdir="LR")
        
        drawing.attr('node', shape = 'none')
        drawing.node('', width = '0!')
        
        if self.initialState == self.finalState:
            drawing.attr('node', shape = 'doublecircle')
            drawing.node(str(self.initialState))
        else:
            drawing.attr('node', shape = 'circle')
            drawing.node(str(self.initialState))
        drawing.edge('', str(self.initialState), style = 'dotted', label = 'START')
        
        drawing.attr('node', shape = 'doublecircle')
        if self.initialState != self.finalState:
            drawing.node(str(self.finalState))
        drawing.attr('node', shape = 'circle')
        
        for x in range(len(self.transitionList)):
            if self.transitionList[x] == transition:
                drawing.attr('edge', color = color)
            drawing.edge(str(self.transitionList[x][0]), str(self.transitionList[x][1]), str(self.transitionList[x][2]))
            if self.transitionList[x] == transition:
                drawing.attr('edge', color = 'black')
        
        drawing.render(format = 'png')
    
    def checkWord(self, word, roadList):
        if len(word) == 0:
            if self.currentState == self.finalState:
                self.currentState = self.initialState
                return roadList
            else:
                self.currentState = self.initialState
                return False
        
        for index in range(len(self.transitionList)):
            if self.transitionList[index][0] == self.currentState:
                if self.transitionList[index][2] == word[0]:
                    self.currentState = self.transitionList[index][1]
                    roadList.append(self.transitionList[index])
                    possibleRoad = self.checkWord(word[1:], roadList)
                    if possibleRoad:
                        return possibleRoad
                elif self.transitionList[index][2] == '&':
                    self.currentState = self.transitionList[index][1]
                    roadList.append(self.transitionList[index])
                    possibleRoad = self.checkWord(word, roadList)
                    if possibleRoad:
                        return possibleRoad
        return False
    
    def printGraph(self):
        out = open('graph.in', 'w')
        out.write (str(len(self.nodesList)) + '\n')
        out.write (str(self.initialState) + '\n')
        out.write (str(self.finalState) + '\n')
        for muchie in self.transitionList:
            print (muchie)
            out.write (str(muchie[0]) + ' ' + str(muchie[1]) + ' ' + str(muchie[2]) + '\n')
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
        The expression tree will look like something like:
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
    
    def rezolve(self):
        if self.check(self.expression):
            print ('Expression is not valid!')
            return -1
        
        tree = self.constructTree(self.expression)
        graph = self.buildGraph(tree)
        graph.nodesList.append(0)
        graph.transitionList.append(tuple([0, graph.initialState, '&']))
        graph.initialState = 0
        graph.graphDraw()
        graph.printGraph()

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
                        roadList = graph.checkWord(word, list())
                        transitionIndex = 0
                        if roadList:
                            print ('Cuvant acceptat!')
                        else:
                            print ('Cuvant neacceptat!')
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
                    graph.graphDrawTransition(roadList[0], transitionIndex)
                    roadList = roadList[1:]
                    transitionIndex += 1
                    
            
            
# The main function
if __name__ == "__main__":
    if (len(sys.argv) != 3):
        print ('Usage: python ' + str(sys.argv[0]) + ' {-f <filename> | -e expression}')
    elif (sys.argv[1] == '-f'):
        file = open(sys.argv[2], 'r')
        ex = expression(file.readline())
        ex.rezolve()
        file.close()
    elif (sys.argv[1] == '-e'):
        ex = expression(sys.argv[2])
        ex.rezolve()
