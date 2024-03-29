from typing import Tuple
import time
count = 0

start_time = 0
end_time = 0

#Read input data from file
def readFile(fileName):
    f = open(fileName, "r")
    equation = f.readline()
    f.close()
    return equation

#Write the result to file
def writeFile(fileName, cryptaSolu, assignment):
    f = open(fileName, "w")
    if cryptaSolu == False:
        f.write("No Solution")
    elif cryptaSolu == True:
        for x in assignment:
            f.write(str(x[1]))
    f.close()

#Heuristic one operator "+" or "-"
def plusLevelOne(attributes, result, assignment):
    end_time = time.time()
    elapsed_time = end_time - start_time
    if(elapsed_time > 300): #5 mins
        print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
        print('No solution')
        exit()

    length = 0
    len_1 = len(attributes[0])
    len_2 = len(attributes[1])
    len_3 = len(result)

    if len_2 > len_3 or len_1 > len_3 or max(len_2, len_1) - len_3 >  max(len_2, len_1)- len_3 > 0 or len_3 - max(len_2, len_1) > 1:
        return False

    if assignment.get(result[-1], None) == 0:
        return False

    for attribute in attributes:
        if assignment.get(attribute[len(attribute) - 1], None) == 0:
            return False
    
    length = max(len_1, len_2)

    #Kiểm tra nếu độ dài kết quả lớn hơn độ dài lớn nhất của các phần tử thì chữ số ngoài cùng của kết quả phải bằng 1
    if len_3 > length:
        if assignment.get(result[-1]) is not None:
            if assignment.get(result[-1]) != 1:
                return False

    #kiểm tra nếu độ dài kết quả bằng bất kì phần tử nào thì tổng của các số ngoài cùng < 9
    sum = 0
    if len_3 == length:
        for i in range(len(attributes)):
            if len(attributes[i]) == len_3:
                if assignment.get(attributes[i][-1]) is not None:
                    sum += assignment.get(attributes[i][-1])
        if sum > 9:
            return False

    #Kiểm tra tổng các phần từ trong cùng với kết quả
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

#Heuristic many operators "+" or "-"
def plusLevelTwo(attributes, result, assignment, letters):
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
            if assignment.get(result[-1]) > carry:
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

#Heuristic many operators "+", "-", and "()"
def plusSubRoundBracket(attributes, result, assignment, letters, operator):
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
        if maxLength < length[i]:
            maxLength = length[i]
    

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
                    if operator[i] == '+':
                        sum += assignment.get(attributes[i][-1])
                    else:
                        sum -= assignment.get(attributes[i][-1])
        
        if sum > 9 or sum < 0:
            return False

    #Nếu độ dài của kết quả lớn hơn tất cả phần tử thì số ngoài cùng của kết quả phài <= biến nhớ
    if length[-1] > maxLength:
        carry = 0

        for i in range(len(length)-1):
            if length[i] == length[-1]-1 and operator[i] == '+':
                carry += 1

        if assignment.get(result[-1]) is not None:
            if assignment.get(result[-1]) > carry:
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
        for index in range(maxLength):
            sum = 0
            for i in range(len(attributes)):
                if length[i] > index:
                    if operator[i] == '+':
                        sum += assignment.get(attributes[i][index])
                    else:
                        sum -= assignment.get(attributes[i][index])
            if sum < 0:
                sum += carry
                if sum %10 != 0:
                    carry = sum//-10 + 1
                else:
                    carry = sum//-10

                if index <= length[-1] - 1:
                    if(sum + carry*10)%10!= assignment.get(result[index]):
                        return False
                carry *= -1
            else:
                if index <= length[-1] - 1:
                    if (sum + carry) % 10 != assignment.get(result[index]):
                        return False
                carry = (sum + carry)//10
            
        if carry == 0 and length[-1] > maxLength:
            return False  
    return True

#Heuristic one operator "*"
def multiOperation(attributes, result, assignment, letters):
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
    
    if assignment.get(result[- 1], None) == 0:
        return False

    for attribute in attributes:
        if assignment.get(attribute[- 1], None) == 0:
            return False

    #xét phần tử cuối
    if assignment.get(attributes[1][0]) is not None and assignment.get(attributes[0][0]) is not None and assignment.get(result[0]) is not None:
        if (assignment.get(attributes[1][0]) * assignment.get(attributes[0][0])) % 10 != assignment.get(result[0]) :
            return False
    
    if len(letters) == len(assignment):
        arrIndex = [0 for x in range(length[1])]
        sum = 0
        carry = 0
        for index in range(0, length[-1]):
            sum = 0
            for i in range(index + 1):
                if i < len(arrIndex):
                    if arrIndex[i] < length[0]:
                        sum += assignment.get(attributes[1][i]) * assignment.get(attributes[0][arrIndex[i]])
                        arrIndex[i] += 1
            if (sum + carry) % 10 != assignment.get(result[index]):
                return False
            if index == length[-1] -1 and sum + carry > 9:
                return False
            carry = (sum+carry)//10
        
    return True

#Solve one operator "*"
def solveCryptaLevelFour(letters, assignment, possibleDigits, attributes, result, operator):    

    if countAssignRight(possibleDigits) == len(letters):
        if (checkEquation(attributes, result, assignment, operator)) == True:
            value = sorted(assignment.items())
            print(assignment)
            writeFile("output.txt", True, value)
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
            if multiOperation(attributes, result, assignment, letters) == True:
                possibleDigits[value] = True
                check = solveCryptaLevelFour(letters, assignment, possibleDigits, attributes, result, operator)
                if check == True:
                    return True
            possibleDigits[value] = False
    return False

#Solve many operators "+", "-", and "()"
def solveCryptaLevelThree(letters, assignment, possibleDigits, attributes, result, operator):

    if countAssignRight(possibleDigits) == len(letters):
        if (checkEquation(attributes, result, assignment, operator)) == True:
            value = sorted(assignment.items())
            print(assignment)
            writeFile("output.txt", True, value)
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
            if plusSubRoundBracket(attributes, result, assignment, letters, operator) == True:
                possibleDigits[value] = True
                check = solveCryptaLevelThree(letters, assignment, possibleDigits, attributes, result, operator)
                if check == True:
                    return True
            possibleDigits[value] = False
    return False

#Solve many operators "+" or "-"
def solveCryptaLevelOne(letters, assignment, possibleDigits, attributes, result, operator):
    if countAssignRight(possibleDigits) == len(letters):
        if (checkEquation(attributes, result, assignment, operator)) == True:
            value = sorted(assignment.items())
            print(assignment)
            writeFile("output.txt", True, value)
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
            if plusLevelOne(attributes, result, assignment) == True:
                possibleDigits[value] = True
                check = solveCryptaLevelOne(letters, assignment, possibleDigits, attributes, result, operator)
                if check == True:
                    return True
            possibleDigits[value] = False
    return False

#Solve many operators "+" or "-"
def solveCryptaLevelTwo(letters, assignment, possibleDigits, attributes, result, operator):
    if countAssignRight(possibleDigits) == len(letters):
        if (checkEquation(attributes, result, assignment, operator)) == True:
            value = sorted(assignment.items())
            print(assignment)
            writeFile("output.txt", True, value)
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
            if plusLevelTwo(attributes, result, assignment, letters) == True:
                possibleDigits[value] = True
                check = solveCryptaLevelTwo(letters, assignment, possibleDigits, attributes, result, operator)
                if check == True:
                    return True
            possibleDigits[value] = False
    return False

#Convert from string to decimal
def stringToDec(string, assignment):
    length = len(string)
    dec = 0
    for index in range(length):
        dec += assignment[string[index]] * (10**(index))
    return dec

#Check attributes and operators with result in decimal form
def checkEquation(attributes, result, assignment, operator):
    Attri = 0
    for i in range(len(attributes)):
        if operator[i] == '+':
            Attri += stringToDec(attributes[i], assignment)
        elif operator[i] == '-':
            Attri -= stringToDec(attributes[i], assignment)
        elif operator[i] == '*':
            Attri *= stringToDec(attributes[i], assignment)
    
    total = stringToDec(result, assignment)

    return Attri == total

#Count letters whose values is correctly assigned
def countAssignRight(digits):
    count = 0
    for index in digits:
        if index == True:
            count += 1
    return count

#Convert subtract to plus. Then solve the problem with plus operator.
#Example: A-B=C -> C+B=A   
def convertSubtract(attributes, result):
    temp = attributes[0]
    attributes[0] = result  
    result = temp
    return result

#Remove round bracket and change operators inside if neccessary.
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

#Initial an operator array
def arrayOperator(equation):
    operator = []
    operator.append('+')
    for index in range(len(equation)):
        if not equation[index].isalpha():
            operator.append(equation[index])
    return operator

#Find max length between attributes and result which is used to take unique letters from input
def findMaxLength(attributes, result):
    maxLength = len(result)

    for attribute in attributes:
        if len(attribute) > maxLength:
            maxLength = len(attribute)
    return maxLength

def handleInput(attributes, result):
    #Except round brackets
    equation = convertEquation(attributes)

    #An operation array
    operator = arrayOperator(equation)

    if attributes.find("(") != -1 or (attributes.find("+") != -1 and attributes.find("-") != -1):
        attributes = []
        word = ""
        for letter in equation:
            if letter.isalpha():
                word += str(letter)
            elif not letter.isalpha():
                attributes.append(word)
                word = ""
        attributes.append(word)
        level = "three"

    elif attributes.find("+") != -1 and attributes.find("-") == -1:
        attributes = attributes.upper().split('+')
        if len(operator) == 2:
            level = "one"
        elif len(operator) > 2:
            level = "two"
            
    elif attributes.find("+") == -1 and attributes.find("-") != -1:
        attributes = attributes.upper().split('-')
        result = convertSubtract(attributes, result)
        #convert all '-' to '+'.
        operator = ['+' for x in operator]
        if len(operator) == 2:
            level = "one"
        elif len(operator) > 2:
            level = "two"

    elif attributes.find("*") != -1:
        attributes = attributes.upper().split('*')
        level = "four"
    
    return [attributes, result, operator, level]


if __name__ == "__main__":
    equation = readFile("input.txt")
    attributes, result = equation.split('=')

    attributes, result, operator, level = handleInput(attributes, result)

    letters = []
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
    
    #Mark possible digits to assign letters
    possibleDigits = [False] * 10
    
    #Solve Cryptarithmetic Problem
    """
    Level 1: 
        Operator + or -, it includes only one operator.
        Example: A+C=D. 
        Enter: one
    Level 2: 
        Operator + or -, it includes many opterators. 
        Example: A+B+C=D. 
        Enter: two
    Level 3: 
        Operator +, -, (). 
        Example: A-(A+B)+D=C. 
        Enter: three
    Level 4: 
        Operator *, it just includes 2 attributes to mutiply. 
        Example: A*A=B. 
        Enter: four
    """
    cryptaSolution = False
    start_time = time.time()
    if level == "one":
        cryptaSolution = solveCryptaLevelOne(letters, {}, possibleDigits, attributes, result, operator)
        if(not cryptaSolution):
            print("No Solution")
            writeFile("output.txt", cryptaSolution, {})
        end_time = time.time()
        elapsed_time = end_time - start_time
        print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")

    elif level == "two":
        cryptaSolution = solveCryptaLevelTwo(letters, {}, possibleDigits, attributes, result, operator)
        if(not cryptaSolution):
            print("No Solution")
            writeFile("output.txt", cryptaSolution, {})
        end_time = time.time()
        elapsed_time = end_time - start_time
        print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")

    elif level == "three":
        cryptaSolution = solveCryptaLevelThree(letters, {}, possibleDigits, attributes, result, operator)
        if(not cryptaSolution):
            print("No Solution")
            writeFile("output.txt", cryptaSolution, {})
        end_time = time.time()
        elapsed_time = end_time - start_time
        print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")

    elif level == "four":
        cryptaSolution = solveCryptaLevelFour(letters, {}, possibleDigits, attributes, result, operator)
        if(not cryptaSolution):
            print("No Solution")
            writeFile("output.txt", cryptaSolution, {})
        end_time = time.time()
        elapsed_time = end_time - start_time
        print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
    

    
    
    