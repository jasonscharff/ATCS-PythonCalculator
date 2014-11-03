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

def fractionalize(expression):
    lastIndex = 0
    alreadyConverted = ""
    fracList = []
    #Append first
    indexOfFirstOperand = findNextOperand(expression)
    subExpression = expression[:indexOfFirstOperand]
    for i in range (0, len(subExpression)):
        if subExpression[i] == "(" or subExpression[i] == ")":
            alreadyConverted += subExpression[i]
        else:
            segmentEnd = findSegmentEnd(expression)
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

def convertToFraction(string):
    if isNumber(string):
        return fraction(float(string), 1)
    elif " " in string:
        separator = string.find(" ")
        numberPart = string[:separator]
        fractionPart = string[separator + 1 :]
        separator = fractionPart.find("\\")
        numerator = fractionPart[:separator]
        denominator = fractionPart[separator + 1:]
        return fraction(numerator + numerator * denominator, denominator)
    else:
        separator = string.find("\\")
        numerator = string[:separator]
        denominator = string[separator + 1:]
        return fraction(numerator, denominator)


def isOperand(char):
    operands = '+-/*^'
    return char in operands


def gcd (a , b) :
    if a == 0:
        return b
    else:
        return gcd(b % a, a)
def lcm(a, b):
    return a * b / gcd(a,b)

class fraction :
    def __init__(self , numerator=0, denominator=1) :
        self.numerator = numerator
        self.denominator = denominator
    def __str__(self) :
        simplified = self.simplifyToMixedNumber()
        frac = simplified[1]
        if simplified[0] == 0:
            return str(simplified[1].numerator) + "\\" + str(simplified[1].denominator)
        elif simplified[1].numerator == 0 :
            return str(simplified[0])
        else:
            return str(simplified[0]) + str(simplified[1].numerator) + "\\" + str(simplified[1].denominator)
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
    def __div__(self, other):
        recip = fraction(other.denominator, other.numerator)
        return self * recip
    def __pow__ (self, power):
        return fraction(self.numerator ** power, self.denominator ** power)
    def simplify(self):
        if(self.numerator == 0):
            return fraction(0, 1)
        else:
            leastCommonMultiple = lcm(self.numerator, self.denominator)
            return fraction(self.numerator / leastCommonMultiple, self.denominator / leastCommonMultiple)
    def simplifyToMixedNumber(self):
        if self.numerator > self.denominator:
            numberPart = int(self.numerator / self.denominator)
            remainder = self - fraction(numberPart, 1)
            return numberPart , remainder.simplify()
        return 0, self.simplify()



def main():
    #expression = input("Please Enter An Expression: ")
    expression = "1+(2*5)"
    fractionalized = fractionalize(expression)
    expressionAsString = fractionalized[0]
    fracList = fractionalized[1]
    print(expressionAsString)
    return eval(expressionAsString)

print(main())