from enum import auto
from app.utils.Automato import Automato
from app.utils.Transition import Transition


def startAutomato(alf):
    automato = Automato()
    automato.getAlphabet(alf)
    automato.addState()
    fTransition = Transition(1, 'a', 2)
    automato.addTransition(fTransition)
    automato.updateInitial(1)
    automato.addFinail(2)
    
    return automato

def createConjuct(automato, symbol):
    states = automato.addState()
    newTransition = Transition(states[0], symbol, states[1])
    automato.addTransition(newTransition)
    automato.addFinail(states[1])

    return [automato, newTransition]

def operandoOr(automato):
    states = automato.addState()
    automato.updateInitial(states[0])
    orInitialTransition = Transition(states[0], None, [1, 3])
    finals = automato.removeFinal()
    automato.addFinail(states[1])
    orFinal1Transition = Transition(finals[0], None, states[1])
    orFinal2Transition = Transition(finals[1], None, states[1])
    automato.addTransition(orInitialTransition)
    automato.addTransition(orFinal1Transition)
    automato.addTransition(orFinal2Transition)

    return automato

def operatorConcatenation(automato, transition):
    finals = automato.removeFinal()
    concatenationTransition = Transition(finals[0], 'c', finals[1])
    automato.addFinail(finals[1])
    automato.addTransition(concatenationTransition)
    automato.removeTransition(transition)

def operatorKleene(automato):
    final = automato.removeFinal()
    exInitial = automato.initial
    states = automato.addState()
    automato.updateInitial(states[0])
    automato.addFinail(states[1])
    kleeneFinalTransition = Transition(final, None, states[1])
    kleeneFinalExInitialTransition = Transition(states[1], None, exInitial)
    kleeneInitalTransition = Transition(states[0], None, exInitial)
    kleeneInitalFinalTransitione = Transition(states[0], None, states[1])
    automato.addTransition(kleeneInitalTransition)
    automato.addTransition(kleeneInitalFinalTransitione)
    automato.addTransition(kleeneFinalTransition)
    automato.addTransition(kleeneFinalExInitialTransition)

    return automato

def createAFN(expression, alf):
    # Inicia o Automato
    automato = startAutomato(alf)

    for i in expression:
        # Cria novo conjunto de estados, caso ler um simbolo do alfabeto
        if i in alf:
            output = createConjuct(automato, i)
            automato = output[0]
        else:
            # Ler o um operando
            if i == '+': # caso seja '+'
                automato = operandoOr(automato)
            elif i == '.': # Caso seja '.'
                # ! REVISAR A LOGICA
                ...
            elif i == '*': # Caso seja '*'
                automato = operatorKleene(automato)

    return automato
