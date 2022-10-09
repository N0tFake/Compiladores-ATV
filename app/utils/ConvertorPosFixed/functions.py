from app.utils.Stack import Stack

# Verifica a expressão
def checkExpression(expression):
    pts = 0
    expression = list(expression)
    for elem in expression:
        if elem == '(':
            pts += 1
        elif elem == ')':
            pts -= 1
        
        if pts < 0:
            return False

    for i in range(len(expression)):
        if (expression[i] == '(' and expression[i+1] == '+') or (expression[i] == '(' and expression[i+1] == '*'):
            return False


    if pts == 0:
        return True
    else:
        return False

# TODO Remover comentarios desnessarios
# conversor infixa para posfixa
def posFixedConvert(expression):
    operators = ['+', '.', '*']
    posFixExpression = []

    #stackExpression = Stack()
    stackOperators = Stack()

    #stackExpression.initStackExpression(expression)

    def priority(operator, top):
        if operator == '*':
            pOperator = 4
        elif operator == '+':
            pOperator = 2
        elif operator == '.':
            pOperator = 1
        else: 
            pOperator = 1

        if top == '*':
            pTop = 4
        elif top == '+':
            pTop = 2
        elif top == '.':
            pTop = 1
        else: 
            pTop = 1

        """ if operator == '*':
            pOperator = 4
        elif operator == '+':
            pOperator = 2
        else: 
            pOperator = 1

        if top == '*':
            pTop = 4
        elif top == '+':
            pTop = 2
        else: 
            pTop = 1

        if operator == '.':
            return False """

        return pOperator >= pTop
    
    for elem in expression:
        if elem in operators:
            if stackOperators.isEmpty():
                stackOperators.push(elem)
            else:
                if stackOperators.top() != '(':
                    if priority(elem, stackOperators.top()):
                        top = stackOperators.pop()
                        posFixExpression.append(top)
                
                stackOperators.push(elem)               
        else:
            if elem == '(':
                stackOperators.push(elem)
            elif elem == ')':
                temp = ''
                while temp != '(':
                    temp = stackOperators.pop()
                    if temp == '(': 
                        break
                    posFixExpression.append(temp)
            else:
                posFixExpression.append(elem)

    while not stackOperators.isEmpty():
        elem = stackOperators.pop()
        posFixExpression.append(elem)
    
    return ''.join(posFixExpression)

# Pega o alfabeto da expressão
def getAlf(expression):
    op = ['+', '(', ')', '*', '.']
    alf = []
    for i in expression:
        if not i in op:
            if not i in alf:
                alf.append(i)
    
    return alf

# Adicion o ponto(.) de concatenação
def addConcatenation(expression, alf):
    result = []
    for i in range(len(expression)):
        if i != len(expression)-1: 
            if (   (expression[i] == ')' and expression[i+1] == '(') 
                or (expression[i] == ')' and expression[i+1] in alf) 
                or (expression[i] in alf and expression[i+1] in alf) 
                or (expression[i] in alf and expression[i+1] == '(') 
                or (expression[i] == '*' and expression[i+1] in alf) 
                or (expression[i] == '*' and expression[i+1] == '(')):
                ###
                result.append(expression[i])
                result.append('.')
                ...
            else:
                result.append(expression[i])
        else:
            result.append(expression[i])
    
    print("\033[92m" + str(''.join(result)) + '\033[0m')

    return result