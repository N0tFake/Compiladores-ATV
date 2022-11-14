from app.utils.Automato import Automato
from app.utils.Transition import Transition

import sys

def fechoE(currentState, transitions):
    output = [currentState]
    for eTransitions in transitions:
        if eTransitions.state == currentState and eTransitions.symbol == None:
            if type(eTransitions.transition) == int:
                output = list(set(output) | set(fechoE(eTransitions.transition, transitions)))
            else:
                for et in eTransitions.transition:
                    output = list(set(output) | set(fechoE(et, transitions)))
                #print(eTransitions.state, eTransitions.symbol, eTransitions.transition)
            
    return output

def convertAFD(afn):
    print('\033[90mConvertAFD ---------------------------------------------------------------------->')
    
    fechoE_list = []
    for transition in afn.transition:
        fecho = fechoE(transition.state, afn.transition)
        fechoE_list.append({
            'fecho': transition.state,
            'transitions': fecho
        })
    
    fechoE_list.append({
        'fecho': afn.finals[0],
        'transitions': afn.finals[0]
    })

    print('Fechos: \n', fechoE_list)
    print('\033[0m')

    return "Em produção"