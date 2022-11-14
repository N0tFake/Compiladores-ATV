from enum import auto
from app.utils.Automato import Automato
from app.utils.Transition import Transition

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
    """ numStatesAfn1 = afn1.getLastState()
    numStatesAfn2 = afn2.getLastState()
    automato.addState((numStatesAfn1 + 1) if numStatesAfn1 > numStatesAfn2 else (numStatesAfn2 + 1))
    """
    automato.updateInitial(afn1.initial)
    automato.addFinail(afn2.finals[0])
    TransitionConcatenation = Transition(afn1.finals[0], None, afn2.initial)
    automato.addTransition(TransitionConcatenation)
    automato.concatenarTransitions(afn1.transition, afn2.transition)

    return automato

def operatorOr(afn1, afn2):
    print('\033[90m Operador OR')
    finals = [afn1.removeFinal(), afn2.removeFinal()]
    automato = Automato()

    automato.getAlphabet(afn1.alphabet)

    automato.concatenarStates(afn1.states)
    automato.concatenarStates(afn2.states)
    numStates = afn2.getLastState()
    automato.addState(numStates + 1)

    automato.updateInitial(0)
    TransitionInitial = Transition(0, None, {afn1.initial + 1, afn2.initial + 1})
    automato.addTransition(TransitionInitial)

     # ADD transitions
    afns = [afn1, afn2]
    for afn in afns:
        for transition in afn.transition:
            state = transition.state + 1
            symbol = transition.symbol
            Ptransition = transition.transition
            if type(Ptransition) == int:
                NewTransition = Transition(state, symbol, Ptransition + 1)
            else:
                NewTransition = Transition(state, symbol, {Ptransition[0]+1, Ptransition[1]+1})
            
            automato.addTransition(NewTransition)
        

    automato.addFinail(numStates+2)
    TransitionFinal1 = Transition(finals[0]+1, None, numStates+2)
    TransitionFinal2 = Transition(finals[1]+1, None, numStates+2)
    automato.addTransition(TransitionFinal1)
    automato.addTransition(TransitionFinal2)
    print('\033[0m')
    return automato

def operatorKleene(afn):
    print('\033[90m Fecho de Kleene')
    final = afn.removeFinal()
    automato = Automato()
    automato.getAlphabet(afn.alphabet)
    newState = afn.getLastState()

    automato.concatenarStates(afn.states)
    automato.addState(len(afn.states))

    automato.updateInitial(0)
    automato.addFinail(newState+2)
    
    TransitionNewInitial = Transition(automato.initial, None, {afn.initial+1, automato.finals[0]})
    TransitionExFinalForFinal =  Transition(final+1, None, automato.finals[0])
    TransitionFinalForExInitial = Transition(automato.finals[0], None, afn.initial+1)
    automato.addTransition(TransitionNewInitial)
    automato.addTransition(TransitionFinalForExInitial)
    automato.addTransition(TransitionExFinalForFinal)

    for transition in afn.transition:
        state = transition.state + 1
        symbol = transition.symbol
        Ptransition = transition.transition
        if type(Ptransition) == int:
            NewTransition = Transition(state, symbol, Ptransition + 1)
        else:
            _ptransition = []
            for P in Ptransition:    
                _ptransition.append(P+1)
            
            NewTransition = Transition(state, symbol, {_ptransition[0], _ptransition[1]})
        
        automato.addTransition(NewTransition)

    print('\033[0m')
    return automato
    

""" 
oAFN = Automato gerado pelo algoritmo de Thompson
Primeiramente cria um novo automato, chamaremos aqui de nAFN:
- o estado inicial do nAFN irá ser 0;
- No oAFN;
	- Verificar se o estado atual do oAFN tem mais de uma transição;
	- Renomear as transições de acordo com a contagem anterior;
	- Salvar as transições renomeadas no nAFN
- Algomerar as transisões com simbolos repetidos mas com P diferentes;


Transições que contem P para mais de um estado:
Fazer uma transição para cada P, com o mesmo simbolo e o mesmo estado

ler o estado da transição
nova transição:
renomear ele de acordo com a contagem
capturar seu simbolo e salvar na nova transição
capturar o P e salvar em outra variavel e renomear na nova transição de acordo com a contagem

Apartir do P capturado repetir o processo anterior

Se P capturado não conter nenhuma transição, ele é final
"""

def renameStates(afn):
    automato = Automato()
    """ automato.updateInitial(0)
    
    transitionInitial = None
    for transition in afn.transition:
        if transition.state == afn.initial:
            transitionInitial = transition.transition 
            break 
    
    transitions = [{str(afn.initil): True, 'transicao': transitionInitial}] """    

"""     for i in range(len(transitionsOrder)):
        print("Transições: (" + str(transitionsOrder[i].state) + 
        ", " + str(transitionsOrder[i].symbol) +
        ", " + str(transitionsOrder[i].transition) + ")")
 """


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

        if current in alf: # Se atual(current) é um simbolo do alfabeto
            print(f'\033[91m [Alfanumerioco ({current})] ' + str(afn) + '\033[0m')
            afn.append(startAutomato(alf, numStates, current))
            numStates += 2     
        else:
            if current == '+': # Se o atual(current) é um operador OR
                print('\033[91m [Operador +] ' + str(afn) + '\033[0m')
                afn[lastAfn-1] = operatorOr(afn[lastAfn-1], afn[lastAfn])
                numStates += 2
                afn.pop()
            
            elif current == '.': # Se atual(current) é um operador de concatenação
                print('\033[91m [Operador .] ' + str(afn) + '\033[0m')
                afn[lastAfn-1] = operatorConcatenation(afn1=afn[lastAfn-1], afn2=afn[lastAfn])
                afn.pop()
                ...
                
            elif current == '*':  # Se atual(current) é um fecho de Kleene
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

    print('\033[94m')
    renameStates(afn[0])
    print('\033[0m')

    return afn[0]
