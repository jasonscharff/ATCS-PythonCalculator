from __future__ import division

def findNextOperand(string):
    for i in range (0, len(string)):
        if isOperand(string[i]):
            return i

def findSegmentEnd(string):
     terminators = '+-/*^()'
     for i in range (0, len(string)):
         if string[i] in terminators:
            return i
     return len(string)

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


def followedByFraction(string):
    terminators = '+-/*^() '
    for i in range (0, len(string)):
        if string[i] in terminators:
            return False
        elif string[i] == "\\":
            return True
    return False

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



def removeSpaces(string):
    newString = ""
    for i in range (0, len(string)):
        if string[i] != " ":
            newString += string[i]
        else:
            if (isOperand(string[i-1]) == False and followedByFraction(string[i+1:])):
                newString += string[i]
    return newString


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



def isNumber(string):
    try:
        float(string)
        return True
    except ValueError :
        return False

def isFloat(string):
    if "." in string:
        return True
    else:
        return False

def convertToFraction(string):
    if isNumber(string):
        if(isFloat):
            return decimal(float(string))
        else:
            return fraction(float(string), 1)
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


def isOperand(char):
    operands = '+-/*^'
    return char in operands


def gcd (a , b) :
    a = float(a)
    b = float(b)
    if a == 0:
        return b
    else:
        return gcd(b % a, a)
def lcm(a, b):
    return a * b / gcd(a,b)

class fraction :
    def __init__(self , Numerator=0, Denominator=1) :
        self.numerator = Numerator
        self.denominator = Denominator
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
    def __mul__(self , other) :
        product = fraction(self.numerator*other.numerator , self.denominator*other.denominator)
        return product
    def __float__(self) :
        return float(self.numerator)/self.denominator
    def reciprocal(self) :
        inverse = fraction(self.denominator , self.numerator)
        return inverse
    def __sub__(self, other):
        leastCommonMultiple = lcm(self.denominator, other.denominator)
        fracOne = fraction((self.numerator) * (leastCommonMultiple / (self.denominator)) , leastCommonMultiple)
        fracTwo = fraction((other.numerator) * (leastCommonMultiple / other.denominator), leastCommonMultiple)
        return fraction(fracOne.numerator - fracTwo.numerator, leastCommonMultiple)
    def __add__ (self, other):
        leastCommonMultiple = lcm(self.denominator, other.denominator)
        fracOne = fraction((self.numerator) * (leastCommonMultiple / (self.denominator)) , leastCommonMultiple)
        fracTwo = fraction((other.numerator) * (leastCommonMultiple / other.denominator), leastCommonMultiple)
        return fraction(fracOne.numerator + fracTwo.numerator , leastCommonMultiple)
    def __truediv__(self, other):
        recip = fraction(other.denominator, other.numerator)
        return self * recip
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

    def simplify(self):
        if(self.numerator == 0):
            return fraction(0, 1)
        else:
            greatestCommonDemoniator = gcd(self.numerator, self.denominator)
            return fraction(self.numerator / greatestCommonDemoniator, self.denominator / greatestCommonDemoniator)
    def simplifyToMixedNumber(self):
        if self.numerator >= self.denominator:
            numberPart = int(self.numerator / self.denominator)
            remainder = self - fraction(numberPart, 1)
            return numberPart , remainder.simplify()
        return 0, self.simplify()


def lenMantessa (number):
        stringVersion = str(number)
        indexOfDecimal = stringVersion.find(".")
        return len(stringVersion[indexOfDecimal + 1:])

class decimal (fraction):
    def __init__(self, numerator=0):
        length = lenMantessa(numerator)
        newNumerator = numerator * 10 ** length
        denominator = 10 ** length
        greatestCommonDemoniator = abs(gcd(newNumerator, denominator))
        fraction.__init__(self, newNumerator / greatestCommonDemoniator, denominator / greatestCommonDemoniator)
    def __str__(self):
        decimalValue = self.numerator / self.denominator
        return str(decimalValue)
    def __mul__(self, other):
         if type(other) == type(fraction()):
            return fraction.__mul__(self, other)
         else:
            fractionOne = float(self)
            fractionTwo = float(other)
            return decimal(fractionOne * fractionTwo)
    def __sub__(self, other):
        if type(other) == type(fraction()):
            return fraction.__sub__(self, other)
        else:
            fractionOne = float(self)
            fractionTwo = float(other)
            return decimal(fractionOne - fractionTwo)
    def __add__(self, other):
        if type(other) == type(fraction()):
            return fraction.__add__(self, other)
        else:
            fractionOne = float(self)
            fractionTwo = float(other)
            return decimal(fractionOne + fractionTwo)
    def __truediv__(self, other):
        if type(other) == type(fraction()):
            return fraction.__truediv__(self, other)
        else:
            fractionOne = float(self)
            fractionTwo = float(other)
            return decimal(fractionOne / fractionTwo)
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


class invalidRadical (Exception):
    pass


def main():
    print "At any point to end the session please enter \'done\'"
    while True:
        expression = raw_input("Please Enter An Expression: ")
        if expression != None and expression != "":
            if(expression.lower() == "done"):
                print "Session Concluded"
                break
            else:
                try:
                    expression = fixNegatives(expression)
                    expression = removeSpaces(expression)
                    fractionalized = fractionalize(expression)
                    expressionAsString = fractionalized[0]
                    fracList = fractionalized[1]
                except:
                    print "The syntax behind your expression is invalid. Please refer to the Readme file."
                    continue
                try:
                    evaluate = eval(expressionAsString)
                    print evaluate
                except ZeroDivisionError:
                    print "Please Don't Divide by Zero"
                except invalidRadical:
                    print "Invalid Radical"
                except:
                    print "Invalid Expression"
        else:
            print "You didn't enter anything"




main()

