# Postfix operating math
# suppose you have a postfix operation statement such as '1 2 +' the output of the operation will be 3


def evaluate_postfix(post_fix_expression : str) -> float :
    
    token_list = post_fix_expression.split()
    operator_list = ['+','-','*','/']

    stack = []
    try:
        for token in token_list:
            if token in operator_list:
                num1 = float(stack.pop())
                num2 = float(stack.pop())
                
                if token == operator_list[0]:
                    stack.append((num1 + num2))
                    # print(stack)
                    
                elif token == operator_list[1]:
                    stack.append((num2 - num1))
                    # print(stack)

                elif token == operator_list[2]:
                    stack.append((num1 * num2))
                    # print(stack)

                elif token == operator_list[3]:
                    stack.append((num2 / num1))
                    # print(stack)

            # elif str(int(float(token))).isnumeric():
            #     stack.append(float(token)) 
            else:
                stack.append(token)      
            
        return stack[0]
    except:
        raise IndexError("The Stack is Empty")

def infix_to_postfix(infix_expression : str) -> str :

    infix_list = []
    num = ""
    for i in range(len(infix_expression)):
        if infix_expression[i].isnumeric() or infix_expression[i] == '.':
            num += infix_expression[i]
            if i == len(infix_expression)-1:
                infix_list.append(num)
        elif infix_expression[i] == " ":
            continue
        else:
            if len(num):
                infix_list.append(num)
            infix_list.append(infix_expression[i])
            num = ""
    # print(infix_list)
    
    stack_1 = []
    stack_2 = []


    for element in infix_list:
        if element not in '+-*/()'  :
            stack_1.append(element)
            if len(stack_2):
                operator = stack_2.pop()
                if operator not in ['(',')']:
                    stack_1.append(operator)

        elif element in '+-/*()':
            if element != ')':
                stack_2.append(element)
            elif element == ')' and len(stack_2):
                operator = stack_2.pop()
                if operator not in '()':
                    stack_1.append(operator)

        # print(stack_1,stack_2)
    del stack_2
    postfix_expression = ""
    for element in stack_1 :
        postfix_expression += (element + " ")

    return postfix_expression 

def calculator():
    while True:
        expression = input(">>> ")
        if any( char.isalpha() for char in expression):
            if expression in ["q","Quit","exit",'quit']:
                break
            print("Error !!!")
            continue
        # print(len(expression))
        elif len(expression):
            print(f'{evaluate_postfix(infix_to_postfix(expression))}')
        else:
            continue

if __name__ == "__main__":
    calculator()
    # print(infix_to_postfix("1.2+3.1"))