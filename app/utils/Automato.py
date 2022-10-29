class Automato:
    def __init__(self):
        self.alphabet = []
        self.states = []
        self.transition = []
        self.initial = 0
        self.finals = []
    
    def getAlphabet(self, alphabet):
        self.alphabet = alphabet
    
    def addState(self, number):
        def createState(a, b):
            self.states.append(a)
            self.states.append(b)

        if len(self.states) == 0 and number == 0:
            createState(0, 1)
            return [1, 2]
        else:
            createState(number, number+1)
    
    def concatenarStates(self, states):
        for state in states:
            if not state in self.states:
                self.states.append(state)

    def addTransition(self, Transition):
        self.transition.append(Transition)
    
    def concatenarTransitions(self, transitionsA, transitionsB):
        if transitionsB:
            newTransitions = self.transition + transitionsA + transitionsB
        else:
            newTransitions = self.transition + transitionsA 
        
        self.transition = newTransitions

    def getLastState(self):
        return self.states[len(self.states)-1]

    def updateInitial(self, newInitial):
        self.initial = newInitial

    def addFinail(self, final):
        self.finals.append(final)

    def removeFinal(self):
        return self.finals.pop() 
    
    def removeTransition(self, transition):
        for i in self.transition:
            if i == transition:
                self.transition.remove(transition)