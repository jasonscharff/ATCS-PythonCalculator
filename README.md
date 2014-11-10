#ATCS Command Line Based Calculator
###Section One User Experience:
The program starts by the computer prompting for an expression. An expression is entered the same way it would normally be written with a few exceptions discussed below. The supported operators are addition (+), subtraction (-), multiplication (\*), division (/), and exponentiation (^). To conclude the program enter the word done (case insensitive) instead of an expression when prompted. If the user enters all numbers (non fractions/mixed numbers) the answer will be in decimal form. However, if one mixed number or fraction is present the answer will be in mixed number form or fraction form (whichever is appropriate such that in A B\\C A will never be 0), unless the the fraction portion would equal 0 in which case just the leading number is displayed.
#####Spaces:
The number of spaces between numbers and operators is completely irrevelant with the exception of mixed numbers and negatives.
#####Entering Fractions:
To enter a fraction simply write the numerator backslash (\\) denominator. For example two thirds is written 2\\3. This is to distinguish a fraction from simple divison in that a fraction will always be prioritized in order of operations and to determine the form in which to give an answer. So while writing something like 1 + 1/3 is valid it will output 1.6667 instead of 1 1\\3.  This is even more important for order of operations issues because writing 8 ^ 2/3 will output 21.333 (64/3), but  8 ^ 2\\3 will output 4.
#####Entering Mixed Numbers:
Mixed numbers are written in the form A B\\C with exactly one space separating the number portion from the fraction. For example one and two thirds would be written 1 2\\3.

#####Negatives:
While the number of spaces is irrevelant such that 8+1 is the same as 8   + 1 there must be either at least one space before a negative or parentheses. For example 1 + -5 is valid as is 1+(-5), but 8+-5 is _not_ valid. 

#####Groupings:
The only acceptable grouping symbol is parentheses. Brackets are not valid. Howver, multiple, nested parentheses are acceptable.


###Section Two Development Tools:
This project was developed using Python Version 3.4.1 then converted to support Python version 2.7. The only conversion requirements necessary were removing the parantheses in print statements, changing input to raw_input (as to avoid calling eval on the input), and importing division from future to avoid integer division errors. Both the Python 2 and Python 3 Versions are available on this projects <a href="https://github.com/jasonscharff/ATCS-PythonCalculator">Github</a> 
###Section Three Strategy:
The general strategy was to parse the string entered by the user by converting each number (fraction, mixed number, or decimal) into a variable of a custom class then appending all of the variables into a list and using the operators given with the exception of the exponentiation operator (^) being converted into a \*\* to statisy the eval method. This can best be illustrated through an example. If the user enters something like 3 + 5 then a method will convert both the three and five into a custom class known as decimal and append all of these to a list. From there, the expression 3 + 5 is converted into something like "fracList[0]+fracList[1]". The Python standard eval method is then called on that string which will return the correct answer of 8. If instead of an integer or decimal the user enters a fraction or mixed number the variable inside of fracList will just be a fraction such that 1\\2 + 3 is also converted into "fracList[0]+fracList[1]". 
<br/>
This program employs two classes that each override the python standard mathematical operator in addition to the \_\_str\_\_ method
#####Classes:
######1. Fraction:
The fraction class is used to support both mixed numbers and fractions. If the user enters a mixed number it is just converted to an improper fraction before being created. The fraction class provides an implementation to all of the five supported operators as well as simplify method and convertToMixedNumber. Whenever the string method is called it simplifies the fraction then if possible returns a mixed number in the form A B\\C. If instead the simplified fraction is an integer, then the str method returns just the integer and if a mixed number is not possible it returns a string in the form B\\C. 
######2. Decimal:
The decimal class inheritts from the fraction class such that it also has a numerator and denominator. In the constructor the decimal class converts the decimal into a fraction by multipling both the inputted decimal by the mutliple of ten to remove the decimal then setting the denominator to be the multiple of ten the numerator was multiplied by. For the mathematical operators if both terms are a decimal then both terms are converted to floats and evaluated–if not the fraction version is called. This is so that if just one term is a fraction the final result will appear as a fraction, but if they are all decimals then a decimal approximation is returned in the final call of the method str. Logically, the str method in the decimal class just divides the numerator by the denominator and returns a string of the resulting float.


#####Process:
After the user enters in a String the program runs a few methods to make it evaluatable (in the form fracList[0] _operator_ fracList[1]...). The first thing it does is convert all negatives into (0-_positiveInt_). This simplifies the later portions of the program such that converting the entered numbers into either fractions or decimals is much easier from a string parsing perspective. After the negatives are converted, all the spaces from the string are removed unless it is the space required in a mixed number. This is to again simplify string parsing because everything can be done in terms of the location of each operator. Then a method is called that goes through the converted string and builds a new version using the custom classes. This is done by determining each term by the location of operators then determining if it is a number, fraction, or mixed number and converting them to their respective classes (a mixed number is not a custom class, but it needs extra code to convert it into a fraction). After this conversion eval is called and any potential exceptions are caught and if there cause is known (such as divison by zero) the proper error message is displayed. The other known cause besides divison by zero is an invalid radical such as -2 ^ 1/2. A custom exception class was built called invalid radical which is thrown if the power method determines the radical to not be possible. Because of the way string parsing is done something like an invalid operator could be many things and thus that is just declared to be "Invalid Syntax". 



