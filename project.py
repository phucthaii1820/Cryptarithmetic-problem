from typing import Tuple
import time
start_time = 0
end_time = 0

def readFile(fileName):
    f = open(fileName, "r")
    equation = f.readline()
    f.close()
    return equation

def isValidate(attributes, result, assignment, letters):
    length = 0
    len_1 = len(attributes[0])
    len_2 = len(attributes[1])
    len_3 = len(result)

    if len_2 > len_3 or len_1 > len_3 or abs(max(len_2, len_1) - len_3) > 1:
        return False

    if assignment.get(result[len_3 - 1], None) == 0:
        return False

    for attribute in attributes:
        if assignment.get(attribute[len(attribute) - 1], None) == 0:
            return False
    
    length = max(len_1, len_2)

    if len_3 > length:
        if assignment.get(result[len_3-1]) is not None:
            if assignment.get(result[len_3-1]) != 1:
                return False

    if assignment.get(attributes[0][0]) is not None and assignment.get(attributes[1][0]) is not None and assignment.get(result[0]) is not None:
        if (assignment.get(attributes[0][0]) + assignment.get(attributes[1][0]))%10 != assignment.get(result[0]):
            return False
    
    for index in range(length):
        if len_1 > index:
            if assignment.get(attributes[0][index]) is None:
                continue
        if len_2 > index:
            if assignment.get(attributes[1][index]) is None:
                continue
        if assignment.get(result[index]) is None:
            continue

        if len_1 < index or len_2 < index:
            if len_1 < index and assignment.get(attributes[1][index]) is not None:
                if((assignment.get(attributes[1][index]) + 1) %10 != assignment.get(result[index]) and (assignment.get(attributes[1][index])) %10 != assignment.get(result[index])):
                    return False
            elif len_2 < index and assignment.get(attributes[0][index]) is not None:
                if ((assignment.get(attributes[0][index]) + 1) %10 != assignment.get(result[index]) and (assignment.get(attributes[0][index])) %10 != assignment.get(result[index])):
                    return False
        if len_1 > index and len_2 > index:
            if (assignment.get(attributes[0][index]) + assignment.get(attributes[1][index]) + 1) % 10 != assignment.get(result[index]) and (assignment.get(attributes[0][index]) + assignment.get(attributes[1][index])) % 10 != assignment.get(result[index]):
                return False
    return True


def isManyValidate(attributes, result, assignment, letters):
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    if(elapsed_time > 300): #5 mins
        print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
        print('No solution')
        exit()
    
    length = []
    for i in range(len(attributes)):
        length.append(len(attributes[i]))
    length.append(len(result))

    maxLength = 0
    for i in range(len(length) -1):
        if length[i] > length[-1]:
            return False
        if maxLength < length[i]:
            maxLength = length[i]
    
    if maxLength - length[-1] > 1:
        return False
    

    if assignment.get(result[- 1], None) == 0:
        return False

    for attribute in attributes:
        if assignment.get(attribute[- 1], None) == 0:
            return False

    #kiểm tra nếu độ dài kết quả bằng bất kì phần tử nào thì tổng của các số ngoài cùng < 9
    sum = 0
    if length[-1] == maxLength:
        for i in range(len(attributes)):
            if length[i] == maxLength:
                if assignment.get(attributes[i][-1]) is not None:
                    sum += assignment.get(attributes[i][-1])
        
        if sum > 9:
            return False

    #Nếu độ dài của kết quả lớn hơn tất cả phần tử thì số ngoài cùng của kết quả phài <= biến nhớ
    if length[-1] > maxLength:
        carry = 0

        for i in range(len(length)-1):
            if length[i] == length[-1]-1:
                carry += 1

        if assignment.get(result[-1]) is not None:
            if assignment.get(result[-1]) > carry - 1:
                return False

    #kiểm tra các số trong cùng của các phần tử có giá trị không
    check = True
    for i in range(len(attributes)):
        if assignment.get(attributes[i][0]) is None:
                    check = False

    #kiểm tra tổng % 10 của số cuối của các phần tử có bằng kết quả không
    if check and assignment.get(result[0]) is not None:
        sum = 0
        for i in range(len(attributes)):
            sum += assignment.get(attributes[i][0])
        if sum % 10 != assignment.get(result[0]):
            return False
    
    sum = 0
    carry = 0
    if len(letters) == len(assignment):
        # if not checkEquation(attributes, result, assignment, operator):
        #     return False
        #print(assignment)
        for index in range(maxLength):
            sum = 0
            for i in range(len(attributes)):
                if length[i] > index:
                        sum += assignment.get(attributes[i][index])
            if (sum + carry) % 10 != assignment.get(result[index]):
                return False
            carry = (sum + carry)//10
            
        if carry == 0 and length[-1] > maxLength:
            return False
         
    return True

def isManyValidateTest(attributes, result, assignment, letters, operator):
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    if(elapsed_time > 300): #5 mins
        print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
        print('No solution')
        exit()
    
    length = []
    for i in range(len(attributes)):
        length.append(len(attributes[i]))
    length.append(len(result))

    maxLength = 0
    for i in range(len(length) -1):
        # if length[i] > length[-1]:
        #     return False
        if maxLength < length[i]:
            maxLength = length[i]
    
    # if maxLength - length[-1] > 1:
    #     return False
    

    if assignment.get(result[- 1], None) == 0:
        return False

    for attribute in attributes:
        if assignment.get(attribute[- 1], None) == 0:
            return False

    #checked
    #kiểm tra nếu độ dài kết quả bằng bất kì phần tử nào thì tổng của các số ngoài cùng < 9
    sum = 0
    if length[-1] == maxLength:
        for i in range(len(attributes)):
            if length[i] == maxLength:
                if assignment.get(attributes[i][-1]) is not None:
                    if operator[i] == '+':
                        sum += assignment.get(attributes[i][-1])
                    else:
                        sum -= assignment.get(attributes[i][-1])
        
        if sum > 9 or sum < 0:
            return False


    #checked
    #Nếu độ dài của kết quả lớn hơn tất cả phần tử thì số ngoài cùng của kết quả phài <= biến nhớ
    if length[-1] > maxLength:
        carry = 0

        for i in range(len(length)-1):
            if length[i] == length[-1]-1 and operator[i] == '+':
                carry += 1

        if assignment.get(result[-1]) is not None:
            if assignment.get(result[-1]) > carry - 1:
                return False

    #kiểm tra các số trong cùng của các phần tử có giá trị không
    check = True
    for i in range(len(attributes)):
        if assignment.get(attributes[i][0]) is None:
                    check = False

    #checked
    #kiểm tra tổng % 10 của số cuối của các phần tử có bằng kết quả không
    if check and assignment.get(result[0]) is not None:
        sum = 0
        for i in range(len(attributes)):
            if operator[i] == '+':
                sum += assignment.get(attributes[i][0])
            else:
                sum -= assignment.get(attributes[i][0])
            
            if sum < 0:
                sum += 10

        if sum % 10 != assignment.get(result[0]):
            return False
    
    sum = 0
    carry = 0
    if len(letters) == len(assignment):
        if not checkEquation(attributes, result, assignment, operator):
            return False
        # for index in range(maxLength):
        #     sum = carry
        #     carry = 0
        #     for i in range(len(attributes)):
        #         if length[i] > index:
        #             if operator[i] == '+':
        #                 sum += assignment.get(attributes[i][index])
        #             else:
        #                 sum -= assignment.get(attributes[i][index])

        #             if sum < 0:
        #                 carry -= 1
        #                 sum += 10
        #     if length[-1] > index:
        #         if sum % 10 != assignment.get(result[index]):
        #             return False
        #     else:
        #         if sum != 0:
        #             return False
        #     if carry == 0:
        #         carry = sum //10
            
        # if carry == 0 and length[-1] > maxLength:
        #     return False
         
    return True



def stringToDec(string, assignment):
    length = len(string)
    dec = 0
    for index in range(length):
        dec += assignment[string[index]] * (10**(index))
    return dec

def checkEquation(attributes, result, assignment, operator):
    Attri = 0
    for i in range(len(attributes)):
        if operator[i] == '+':
            Attri += stringToDec(attributes[i], assignment)
        else :
            Attri -= stringToDec(attributes[i], assignment)
    
    total = stringToDec(result, assignment)

    return Attri == total

def countAssignRight(digits):
    count = 0
    for index in digits:
        if index == True:
            count += 1
    return count

def solveCrypta(letters, assignment, possibleDigits, attributes, result, operator):

    if countAssignRight(possibleDigits) == len(letters):
        if (checkEquation(attributes, result, assignment, operator)) == True:
            print(assignment)
            return True
        return False

    for char in letters:
        if char not in assignment:
            letter = char
            break

    for value in range (len(possibleDigits)):
        if possibleDigits[value] == False: 
            assignment = assignment.copy()
            assignment[letter] = value
            if isManyValidate(attributes, result, assignment, letters) == True:
                possibleDigits[value] = True
                check = solveCrypta(letters, assignment, possibleDigits, attributes, result, operator)
                if check == True:
                    return True
            possibleDigits[value] = False
                
def convertSubtract(attributes, result):
    temp = attributes[0]
    attributes[0] = result
    result = temp
    return result

def convertEquation(equation):
    newEquation = []
    roundBracket = []
    checkSubtract = False
    

    for index in range(len(equation)):
        if equation[index] == '(':
            if index == 0:
                roundBracket.append(equation[index])
                continue
            else:
                if equation[index - 1] == '-':
                    roundBracket.append(equation[index])
                    newEquation.pop()
                    checkSubtract = True
                    continue
                elif equation[index - 1] == '+':
                    roundBracket.append(equation[index])
                    continue
        elif equation[index] == ')':
            if roundBracket is not None:
                roundBracket.pop()
                checkSubtract = False
                continue
        if roundBracket is not None and checkSubtract == True:
            if equation[index] == '-':
                newEquation.append('+')  
                continue
            elif equation[index] == '+':
                newEquation.append('-') 
                continue
        newEquation.append(equation[index])     
    return ''.join(str(ele) for ele in newEquation)

def arrayOperator(equation):
    operator = []
    operator.append('+')
    for index in range(len(equation)):
        if not equation[index].isalpha():
            operator.append(equation[index])
    return operator

def findMaxLength(attributes, result):
    maxLength = len(result)

    for attribute in attributes:
        if len(attribute) > maxLength:
            maxLength = len(attribute)
    return maxLength
        

if __name__ == "__main__":
    equation = readFile("input.txt")
    attributes, result = equation.split('=')

    #Except round brackets
    equation = convertEquation(attributes)
    print(equation)

    #An operation array
    operator = arrayOperator(equation)
    print(operator)

    letters = []
    option = input("Enter operator: ")
    
    #Take attributes of equation
    if option == 'plus':
        attributes = attributes.upper().split('+')
    elif option == 'subtract':
        attributes = attributes.upper().split('-')
        result = convertSubtract(attributes, result)

    #Reverse attributes' elements
    for i in range(len(attributes)):
        attributes[i] = attributes[i][::-1]

    #Reverse result element
    result = result[::-1]

    #Take unique letters
    maxLength = findMaxLength(attributes, result)
    for i in range(maxLength):
        for attribute in attributes:
            if len(attribute) > i and attribute[i] not in letters:
                letters.append(attribute[i])
        if  len(result) > i and result[i] not in letters:
            letters.append(result[i])
    
    possibleDigits = [False] * 10
    start_time = time.time()
    if(not solveCrypta(letters, {}, possibleDigits, attributes, result, operator)):
        print("hehe")
    end_time = time.time()
    elapsed_time = end_time - start_time
    print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")

    
    
    