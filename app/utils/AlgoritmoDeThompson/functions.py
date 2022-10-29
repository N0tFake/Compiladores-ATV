from enum import auto
from app.utils.Automato import Automato
from app.utils.Transition import Transition

# oLer um simbolo e o seu proximo 
# -> Caso o prox seja uma letra do alfabeto ler o prox 
# indentificar o operando do prox
# se for +, fazer A+B
# se ., fazer A.B
# -> Caso o prox seja um operando
# se for um *, fazer sua estrutura
# 
# Na proxima interação se o simbolo lido for uma letra e seu proximo tb for, ou um *
# Criar novo automato
# Fazer até acha a mesma condição
# 
# Se tiver 2 ou mais automatos, e o simbolo lido for um . ou +
# Juntar o ultimo automato com o ultimo-1, fazendo a operação lidas
#

def startAutomato(alf, end, symbol):
    automato = Automato()
    automato.getAlphabet(alf)
    automato.addState(end)
    fTransition = Transition(end, symbol, end+1)
    automato.addTransition(fTransition)
    automato.updateInitial(end)
    automato.addFinail(end+1)
    
    return automato

def operatorConcatenation(afn1, afn2):
    automato = Automato()
    
    automato.getAlphabet(afn1.alphabet)

    automato.concatenarStates(afn1.states)
    automato.concatenarStates(afn2.states)
    
    numStatesAfn1 = afn1.getLastState()
    numStatesAfn2 = afn2.getLastState()
    automato.addState((numStatesAfn1 + 1) if numStatesAfn1 > numStatesAfn2 else (numStatesAfn2 + 1))
    automato.updateInitial(afn1.initial)
    automato.addFinail(afn2.finals[0])
    TransitionConcatenation = Transition(afn1.finals[0], None, afn2.initial)
    automato.addTransition(TransitionConcatenation)
    automato.concatenarTransitions(afn1.transition, afn2.transition)

    return automato

def operatorOr(afn1, afn2):
    print('\033[90m')
    finals = [afn1.removeFinal(), afn2.removeFinal()]
    automato = Automato()

    automato.getAlphabet(afn1.alphabet)

    automato.concatenarStates(afn1.states)
    automato.concatenarStates(afn2.states)
    numStates = afn2.getLastState()
    automato.addState(numStates + 1)

    print('finals: ', finals)
    print('numStates: ', numStates)

    automato.updateInitial(numStates+1)
    TransitionInitial1 = Transition(numStates+1, None, afn1.initial)
    TransitionInitial2 = Transition(numStates+1, None, afn2.initial)
    automato.addTransition(TransitionInitial1)
    automato.addTransition(TransitionInitial2)

    automato.concatenarTransitions(afn1.transition, afn2.transition)

    automato.addFinail(numStates+2)
    TransitionFinal1 = Transition(finals[0], None, numStates+2)
    TransitionFinal2 = Transition(finals[1], None, numStates+2)
    automato.addTransition(TransitionFinal1)
    automato.addTransition(TransitionFinal2)
    print('\033[0m')
    return automato

def operatorKleene(afn):
    final = afn.removeFinal()
    automato = Automato()
    automato.getAlphabet(afn.alphabet)
    newState = afn.getLastState()

    automato.concatenarStates(afn.states)
    automato.addState(len(afn.states))

    automato.updateInitial(newState+1)
    automato.addFinail(newState+2)
    TransitionInitialForExInitial = Transition(automato.initial, None, afn.initial)
    TransitionExFinalForFinal =  Transition(final, None, automato.finals[0])
    TransitionInitialForFinal = Transition(automato.initial, None, automato.finals[0])
    TransitionFinalForExInitial = Transition(automato.finals[0], None, afn.initial)
    automato.addTransition(TransitionInitialForFinal)
    automato.addTransition(TransitionFinalForExInitial)
    automato.addTransition(TransitionInitialForExInitial)
    automato.addTransition(TransitionExFinalForFinal)
    automato.concatenarTransitions(transitionsA=afn.transition, transitionsB=None)

    return automato

def createAFN(expression, alf):
    # Inicia o Automato
    afn = []
    numStates = 0

    length = len(expression) - 1
    cont = 0
    current = expression[0]

    while length >= cont:
        current = expression[cont]
        lastAfn = len(afn)-1

        if current in alf: # Se proximo(next) é um simbolo do alfabeto
            print(f'\033[91m [Alfanumerioco ({current})] ' + str(afn) + '\033[0m')
            afn.append(startAutomato(alf, numStates, current))
            numStates += 2
            #next = expression[cont]            
        else:
            if current == '+': # Se o proximo(next) é um operador OR
                print('\033[91m [Operador +] ' + str(afn) + '\033[0m')
                afn[lastAfn-1] = operatorOr(afn[lastAfn-1], afn[lastAfn])
                numStates += 2
                afn.pop()
            
            elif current == '.': # Se proximo(next) é um operador de concatenação

                print("\033[91m" + 
                    "Tamnho da lista de afn: " + str(len(afn)) +
                    "\nAlfabeto: " + str(afn[lastAfn].alphabet) +
                    "\nInicial: " + str(afn[lastAfn].initial) +
                    "\nFinal: " + str(afn[lastAfn].finals) +
                    "\nStates: " + str(afn[lastAfn].states) 
                ) 

                for i in range(len(afn[lastAfn].transition)):
                    print("Transições: (" + str(afn[lastAfn].transition[i].state) + 
                    ", " + str(afn[lastAfn].transition[i].symbol) +
                    ", " + str(afn[lastAfn].transition[i].transition) + ")")

                print("\033[0m")

                print('\033[91m [Operador .] ' + str(afn) + '\033[0m')
                afn[lastAfn-1] = operatorConcatenation(afn1=afn[lastAfn-1], afn2=afn[lastAfn])
                afn.pop()
                ...
                
            elif current == '*':  # Se proximo(next) é um fecho de Kleene
                print('\033[91m [Operador *] ' + str(afn) + '\033[0m')
                afn[lastAfn] = operatorKleene(afn[lastAfn])
                numStates += 2

        cont += 1

    print("\033[93m" + 
        "Tamnho da lista de afn: " + str(len(afn)) +
        "\nAlfabeto: " + str(afn[0].alphabet) +
        "\nInicial: " + str(afn[0].initial) +
        "\nFinal: " + str(afn[0].finals) +
        "\nStates: " + str(afn[0].states) 
    ) 
    
    for i in range(len(afn[0].transition)):
        print("Transições: (" + str(afn[0].transition[i].state) + 
        ", " + str(afn[0].transition[i].symbol) +
        ", " + str(afn[0].transition[i].transition) + ")")
    
    print("\033[0m")

    return afn[0]
