#This method goes through the string and returns the index of the nextOperand.
#If there isn't another operand None is returned
def findNextOperand(string):
    for i in range (0, len(string)):
        if isOperand(string[i]):
            return i
#This method finds the end of a segment. A segment is defined as one number, fraction, or mixed number
#so it just finds the index of the first segment breaker (anything in the string terminators). If one 
#is not found the length of the string is returned.
def findSegmentEnd(string):
     terminators = '+-/*^()'
     for i in range (0, len(string)):
         if string[i] in terminators:
            return i
     return len(string)
#This finds the end of segment in a similar manor to findSegmentEnd, but it is used before spaces are removed
#so spaces are considered a segment breaker. However, in a mixed number a space is mandatory so it determines
#if the space is just part of a mixed number to prevent false positives. If there is no segment end in the string
#the length of the string is returned.
def findSegmentEndWithSpaces(string):
    terminators = '+-/*^() '
    for i in range (0, len(string)):
        if string[i] in terminators:
            if(string[i] == " "):
                if followedByFraction(string[i+1:]):
                    return i
            else:
                return i

    return len(string)

#This method determines if before the next operator or parentheses there is a \ indicating a fraction. 
#This is used to ensure spaces are not removed that belong to a mixed number.
def followedByFraction(string):
    terminators = '+-/*^() '
    for i in range (0, len(string)):
        if string[i] in terminators:
            return False
        elif string[i] == "\\":
            return True
    return False

#This method goes through the string and converts all negatives into (0-negative) to make the string parsing
#of converting into custom classes simpler.
def fixNegatives(string):
    newString = ""
    forValue = 0
    if string[0] == "-":
        newString += "(0-"
        indexOfNumberEnd = findSegmentEndWithSpaces(string[1:]) + 1
        portion = string[1:indexOfNumberEnd]
        newString += portion
        newString += ")"
        forValue = indexOfNumberEnd
    while forValue < len(string) :
        if (string[forValue] == " " or string[forValue] == "(") and string[forValue+1] == "-" and (isNumber(string[forValue + 2]) or string[forValue+2] == "."):
            if(string[forValue] == "("):
                newString += "("
            indexOfTermEnd = findSegmentEndWithSpaces(string[forValue+2:]) + forValue + 2
            term = string[forValue+2:indexOfTermEnd]
            newString = newString +  "(0-" + term + ")"
            forValue = indexOfTermEnd
        else:
            newString += string[forValue]
            forValue += 1
    return newString


#This method goes through the string and removes any spaces unless it is followed by a fraction and that spaces is necessary.
#This is to make the string parsing of converting terms into a custom class simpler.
def removeSpaces(string):
    newString = ""
    for i in range (0, len(string)):
        if string[i] != " ":
            newString += string[i]
        else:
            if (isOperand(string[i-1]) == False and followedByFraction(string[i+1:])):
                newString += string[i]
    return newString

#This method goes through the entire expression and converts it into the form "fracList[0] operator fracList[1]...". This is so
#eval can be called on the expression even though it has fractions and mixed numbers. It does this by building a new String keeping
#operators, parentheses, and converting the terms into a custom class and appending it onto fracList.
def fractionalize(expression):
    lastIndex = 0
    alreadyConverted = ""
    segmentEnd = 0
    fracList = []
    #Append first
    indexOfFirstOperand = findNextOperand(expression)
    subExpression = expression[:indexOfFirstOperand]
    for i in range (0, len(subExpression)):
        if subExpression[i] == "(" or subExpression[i] == ")":
            alreadyConverted += subExpression[i]
        else:
            segmentEnd = findSegmentEnd(expression[i:]) + i
            firstTerm = subExpression[i:segmentEnd]
            fractionVersion = convertToFraction(firstTerm)
            fracList.append(fractionVersion)
            alreadyConverted += "fracList[" + str(len(fracList) - 1) + "]"
            break

    #Continue on with the rest of the expression
    for x in range (segmentEnd, len(expression)):
        if expression[x] == ")":
            alreadyConverted += expression[x]
        elif isOperand(expression[x]):
            if (expression[x] == "^"):
                alreadyConverted += "**"
            else:
                alreadyConverted += expression[x]
            while ( expression[x+1] == "(" or expression[x+1] == ")" ):
                alreadyConverted += expression[x+1]
                x+=1
            x+=1
            segmentEnd = findSegmentEnd(expression[x + 1:])
            term = expression[x:segmentEnd + x + 1]
            fractionVersion = convertToFraction(term)
            fracList.append(fractionVersion)
            alreadyConverted += "fracList[" + str(len(fracList) - 1) + "]"
    return alreadyConverted, fracList


#This method determines if something is a number. If it is, True is returned. If not, False is returned. This is used in ConvertToFraction
def isNumber(string):
    try:
        float(string)
        return True
    except ValueError :
        return False


#This method takes a String and converts it into either a decimal or fraction. If the term is a mixed number
#this method will convert that into an impromper fraction.
def convertToFraction(string):
    if isNumber(string):
    	return decimal(float(string))
    elif " " in string:
        separator = string.find(" ")
        numberPart = float(string[:separator])
        fractionPart = string[separator + 1 :]
        separator = fractionPart.find("\\")
        numerator = float(fractionPart[:separator])
        denominator = float(fractionPart[separator + 1:])
        return fraction(numerator + numberPart * denominator, denominator)
    else:
        separator = string.find("\\")
        numerator = float(string[:separator])
        denominator = float(string[separator + 1:])
        return fraction(numerator, denominator)

#This method returns true if a character is an operator and false if it isn't
def isOperand(char):
    operands = '+-/*^'
    return char in operands

#This method uses Euclids algorithim to find the GCD of two numbers.
def gcd (a , b) :
    a = float(a)
    b = float(b)
    if a == 0:
        return b
    else:
        return gcd(b % a, a)

#This method finds the least common multiple by multipling the two numbers together (guaranteed to be a multiple)
#and dividing that product by the gcd.
def lcm(a, b):
    return a * b / gcd(a,b)

'''
The fraction class is used to hold both mixed numbers and fractions. Mixed numbers are stored as impromper fractions.
This class overides the standard operators, the toString method, the float method, and has a the helper methods simplifyToMixedNumber, 
simplify, and reciprocal. 
'''
class fraction :
	#The constructor just takes the given parameters (numerator and denominator) and
	#sets the proper values within the class
    def __init__(self , Numerator=0, Denominator=1) :
        self.numerator = Numerator
        self.denominator = Denominator
    #This method returns a string representation of the fraction. It first simpifies the fraction (part of simplifytoMixedNumber)
    #and if possible converts it into a mixed number. It then returns the fraction in the form A B\C, but if A is 0 it just returns B\C
    #and if B is 0 it just returns A.
    def __str__(self) :
        if(self.denominator == 0):
            return "Please Do Not Divide By Zero"
        simplified = self.simplifyToMixedNumber()
        frac = simplified[1]
        if simplified[0] == 0:
            return str(simplified[1].numerator) + "\\" + str(simplified[1].denominator)
        elif simplified[1].numerator == 0 :
            return str(simplified[0])
        else:
            return str(simplified[0]) + " " +  str(simplified[1].numerator) + "\\" + str(simplified[1].denominator)
    #This method returns a fraction of the product of the two given fractions.
    def __mul__(self , other) :
        product = fraction(self.numerator*other.numerator , self.denominator*other.denominator)
        return product
    #This method gets a float aproximation of the fraction by dividing the numerator by the denominator.
    def __float__(self) :
        return float(self.numerator)/self.denominator
    #This method gets the reciporcal by simplify flipping the numerator and denominator
    def reciprocal(self) :
        inverse = fraction(self.denominator , self.numerator)
        return inverse
   	#This method subtracts two fractions by first putting them over a common denominator then subtracting. It returns
   	#a fraction.
    def __sub__(self, other):
        leastCommonMultiple = lcm(self.denominator, other.denominator)
        fracOne = fraction((self.numerator) * (leastCommonMultiple / (self.denominator)) , leastCommonMultiple)
        fracTwo = fraction((other.numerator) * (leastCommonMultiple / other.denominator), leastCommonMultiple)
        return fraction(fracOne.numerator - fracTwo.numerator, leastCommonMultiple)
    #This method adds two fractions by first putting them over a common denominator then adding. It returns
   	#a fraction.
    def __add__ (self, other):
        leastCommonMultiple = lcm(self.denominator, other.denominator)
        fracOne = fraction((self.numerator) * (leastCommonMultiple / (self.denominator)) , leastCommonMultiple)
        fracTwo = fraction((other.numerator) * (leastCommonMultiple / other.denominator), leastCommonMultiple)
        return fraction(fracOne.numerator + fracTwo.numerator , leastCommonMultiple)
    #This method divides two fractions by returning the product of the first fraction and the reciprocal of the second
    def __truediv__(self, other):
        recip = fraction(other.denominator, other.numerator)
        return self * recip
    #This method handles fractional exponents. It first determines if the given radical is invalid throwing an invalidRadical exception.
    #If not then it solves the fractional exponent. If the output is a decimal value it returns a decimal to make things clear for the user.
    def __pow__ (self, power):
        if float(self) < 0 and float(power) % 2 == 0:
            raise invalidRadical
        if float(power) >= 0:
            partOne = fraction(self.numerator ** (1/power.denominator), self.denominator ** (1/power.denominator))
            partTwo = fraction(partOne.numerator ** power.numerator, partOne.denominator ** power.numerator)
            if(float.is_integer(partTwo.numerator) and float.is_integer(partTwo.numerator)):
                return partTwo
            else:
                return decimal(float(partTwo))
        else:
            power = abs(power)
            partOne = fraction(self.numerator ** power.demoninator, self.denominator ** power.demoninator)
            partTwo = fraction(partOne.numerator ** (1/power.numerator), partOne.demoniator ** (1/power.numerator))
            return fraction.reciprocal(partTwo)
    #This method simplifies a fraction to the lowest possible numerator and denominator.
    def simplify(self):
        if(self.numerator == 0):
            return fraction(0, 1)
        else:
            greatestCommonDemoniator = gcd(self.numerator, self.denominator)
            return fraction(self.numerator / greatestCommonDemoniator, self.denominator / greatestCommonDemoniator)
    #This method converts a fraction into a mixed number with the fraction portion in simplest terms. It returns
    #a tuple of the preceeding number and the fraction.
    def simplifyToMixedNumber(self):
        if self.numerator >= self.denominator:
            numberPart = int(self.numerator / self.denominator)
            remainder = self - fraction(numberPart, 1)
            return numberPart , remainder.simplify()
        return 0, self.simplify()

#This method takes in a number and finds the length of its mantessa by determining the length
#of its string version after the period.
def lenMantessa (number):
        stringVersion = str(number)
        indexOfDecimal = stringVersion.find(".")
        return len(stringVersion[indexOfDecimal + 1:])
'''
The custom class decimal inherits from fraction and is used for non-fraction/mixed number entries.
The purpose of this is such that all decimals are compatible with fractions (so an error isn't called
when doing an operation on a fraction and a decimal). As well because a custom class is used custome exceptions
can be thrown such as the invalidRadical. 
'''
class decimal (fraction):
	#The constructor in essence converts each decimal into a fraction that has a numerator and denominator. 
	#However, by using a custom class instead of just making every decimal fraction the toString can output
	#a more appropriate result. This method works by finding the length of the mantissa, multipling the decimal
	# times 10 ^ (length of mantessa) and making the denominator 10 ^ length of the mantissa. The fraction is then simplified.
    def __init__(self, numerator=0):
        length = lenMantessa(numerator)
        newNumerator = numerator * 10 ** length
        denominator = 10 ** length
        greatestCommonDemoniator = abs(gcd(newNumerator, denominator))
        fraction.__init__(self, newNumerator / greatestCommonDemoniator, denominator / greatestCommonDemoniator)
    #toString method which just returns a string of the float value of each decimal.
    def __str__(self):
        decimalValue = self.numerator / self.denominator
        return str(decimalValue)
    #If one of the items is a fraction it calls the fraction class's mulitplication method to correct typing errors and 
    #provide the proper output, if not the float values of each decimal are multiplied together
    def __mul__(self, other):
         if type(other) == type(fraction()):
            return fraction.__mul__(self, other)
         else:
            fractionOne = float(self)
            fractionTwo = float(other)
            return decimal(fractionOne * fractionTwo)
    #If one of the items is a fraction it calls the fraction class's subtractaction method to correct typing errors and 
    #provide the proper output, if not the float values of each decimal are subtracted together
    def __sub__(self, other):
        if type(other) == type(fraction()):
            return fraction.__sub__(self, other)
        else:
            fractionOne = float(self)
            fractionTwo = float(other)
            return decimal(fractionOne - fractionTwo)
    #If one of the items is a fraction it calls the fraction class's addition method to correct typing errors and 
    #provide the proper output, if not the float values of each decimal are added together
    def __add__(self, other):
        if type(other) == type(fraction()):
            return fraction.__add__(self, other)
        else:
            fractionOne = float(self)
            fractionTwo = float(other)
            return decimal(fractionOne + fractionTwo)
    #If one of the items is a fraction it calls the fraction class's division method to correct typing errors and 
    #provide the proper output, if not the float values of each decimal are divided.
    def __truediv__(self, other):
        if type(other) == type(fraction()):
            return fraction.__truediv__(self, other)
        else:
            fractionOne = float(self)
            fractionTwo = float(other)
            return decimal(fractionOne / fractionTwo)
    #If one of the items is a fraction it calls the fraction class's division method to correct typing errors and 
    #provide the proper output, if not the method checks to see if there is an invalid radical and if there isn't
    #takes float value of the number to power of the float value of the other. If there is an invalid radical
    #an exception is thrown.
    def __pow__(self, power):
         if type(power) == type(fraction()):
            return fraction.__pow__(self, power)
         else:
            fractionOne = float(self)
            powerDecimal = float(power)
            if decimal(power).denominator %2 == 0 and fractionOne < 0:
                raise invalidRadical
            else:
                return decimal(fractionOne ** powerDecimal)


#If a radical is invalid such as -2 ^ 1\2 then this exception is thrown.
#A custom exception is used to properly give an error message to the user.
class invalidRadical (Exception):
    pass

'''
This method handles the entire programs control flow. It runs a loop that takes in inputs, readies them
for evaluation, evaluates, then repeats. If an error arises then the method prints out an error messgae
informing the user as to avoid any crashes. The main loop only concludes when the user enters
the keyword 'done' (case insensitive)
'''
def main():
    print("At any point to end the session please enter \'done\'")
    while True:
        expression = input("Please Enter An Expression: ")
        if expression != None and expression != "":
            if(expression.lower() == "done"):
                print ("Session Concluded")
                break
            else:
                try:
                    expression = fixNegatives(expression)
                    expression = removeSpaces(expression)
                    fractionalized = fractionalize(expression)
                    expressionAsString = fractionalized[0]
                    fracList = fractionalized[1]
                except:
                    print ("The syntax behind your expression is invalid. Please refer to the Readme file.")
                    continue
                try:
                    evaluate = eval(expressionAsString)
                    print(evaluate)
                except ZeroDivisionError:
                    print ("Please Don't Divide by Zero")
                except invalidRadical:
                    print("Invalid Radical")
                except:
                     print("Invalid Expression")
        else:
            print ("You didn't enter anything")



main() #Start program

