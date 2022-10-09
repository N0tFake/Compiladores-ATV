from enum import auto
from multiprocessing import context
from typing import final
from django.shortcuts import render
from app.utils.AlgoritmoDeThompson.functions import createAFN, startAutomato
from app.utils.Automato import Automato
from app.utils.ConvertorPosFixed.functions import addConcatenation, checkExpression, getAlf, posFixedConvert
from app.utils.Stack import Stack
from app.utils.Transition import Transition

# Create your views here.
def home(request):
    context = {}
    return render(request, 'home.html', context)

def expression(request):
    expression = request.GET['input']

    correct = checkExpression(expression)

    if expression == '':  # Expressão vazia
        context = {"inputEmpty": True}
    elif expression == '&': # Palavra Vazia
        context = {
            "expression": expression,
            "posfix": expression
        }
    elif not correct: 
        context = { "expError": True }
    else: # Expressão
        expression = list(expression)
        alf = getAlf(expression)
        if not '.' in expression:
            expressionCon = addConcatenation(expression, alf)
        else:
            expressionCon = expression

        posFixExpression = posFixedConvert(expressionCon)
        expression = ''.join(expression)


        # ! CODIGO COM PROBLEMA NO OPERADOR DE CONCATENAÇÂO
        # Inicia o automato
        #automato = createAFN(expression, alf)
        
        context = {
            "expression": expression,
            "posfix": posFixExpression
        }

        """ print("\033[93m" + 
            "Alfabeto: " + str(automato.alphabet) +
            "\nInicial: " + str(automato.initial) +
            "\nFinal: " + str(automato.finals))
        
        for i in range(len(automato.transition)):
            print("Transições: (" + str(automato.transition[i].state) + 
            ", " + str(automato.transition[i].symbol) +
            ", " + str(automato.transition[i].transition) + ")")
        
        print("\033[0m") """



    return render(request, 'home.html', context)