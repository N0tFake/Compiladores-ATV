class Automato:
    def __init__(self):
        self.alphabet = []
        self.states = []
        self.transition = []
        self.initial = 0
        self.finals = []
    
    def getAlphabet(self, alphabet):
        self.alphabet = alphabet
    
    def addState(self):
        def createState(a, b):
            self.states.append(a)
            self.states.append(b)

        if len(self.states) == 0:
            createState(1, 2)
            return [1, 2]
        else:
            last = self.states[len(self.states)-1]
            createState(last + 1, last + 2)
            return [last + 1, last + 2]
    
    def addTransition(self, Transition):
        self.transition.append(Transition)
    
    def getLastState(self):
        return self.states[len(self.states)-1]

    def updateInitial(self, newInitial):
        self.initial = newInitial

    def addFinail(self, final):
        self.finals.append(final)

    def removeFinal(self):
        if len(self.finals) > 1:
            final2 = self.finals.pop()
            final1 = self.finals.pop()
            return [final1, final2]
        
        return self.finals.pop(0)

    
    def removeTransition(self, transition):
        for i in self.transition:
            if i == transition:
                self.transition.remove(transition)