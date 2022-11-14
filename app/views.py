from distutils import extension
from enum import auto
from multiprocessing import context
from typing import final
from django.shortcuts import render
from app.utils.AlgoritmoDeThompson.functions import createAFN, startAutomato
from app.utils.Automato import Automato
from app.utils.ConvertorPosFixed.functions import addConcatenation, checkExpression, getAlf, posFixedConvert
from app.utils.Stack import Stack
from app.utils.Transition import Transition
from app.utils.conversorAFD.functions import convertAFD
from app.utils.plot.functions import plotAutomato

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

        # Criação do Automato Finito não deterministico, usando o algoritmo de Thompson
        afn = createAFN(posFixExpression, alf)

        # Converter o AFN para AFN
        afd = convertAFD(afn)

        #plotAutomato(afn)

        expression = ''.join(expression)
        
        context = {
            "expression": expression,
            "posfix": posFixExpression,
            "AFN": afn,
            "AFD": afd
        }

    return render(request, 'home.html', context)