import numpy as np
import matplotlib.pyplot as plt


class Plotter:
    
    def checkPlusOrMinusSign(self,sign):

        """
        Check if the given charachter is a plus or a minus sign charachter.

        Args:
            sign : Charachter to check if it's a plus or minus sign.
        Return:
            bool : True : if it's a plus or minus sign char.

        """

        if sign == "+" or sign == "-":
            return True
        else:
            return False


    def checkDivSign(self,sign):

        """
        Check if the given charachter is a divison sign charachter.

        Args:
            sign : Charachter to check if it's a mult or div sign.
        Return:
            bool : True : if it's a mult or div sign char.

        """

        if sign == "/":
            return True
        else:
            return False


    def checkMultSign(self,sign):

        """
        Check if the given charachter is a multiply sign charachter.

        Args:
            sign : Charachter to check if it's a mult or div sign.
        Return:
            bool : True : if it's a mult or div sign char.

        """

        if sign == "*":
            return True
        else:
            return False


    def checkPowerSign(self,sign):
        """
        Check if the given charachter is a power sign charachter.

        Args:
            sign : Charachter to check if it's a power sign.
        Return:
            bool : True : if it's a power sign char.

        """

        if sign == "^":
            return True
        else:
            return False


    def transformSignedStringToNumber(self,number):

        """
        Given a string number with its sign ex : "+1","-1" , convert it to an integer number ex "+1"->1, "-1"->-1

        Args:
            number : String number to be converted.
        Return:
            int(number) : The number in integer type.

        """

        if number[0] == "+":
            return int(number[1:])
        elif number[0] == "-":
            return int(number[1:]) * -1
        else:
            return int(number[0])


    def accumulateCoeffecients(self,terms, var, coeff):
        """
        Accumulate the coeffecients for the same variables in the terms by adding or subtracting them
        according to their signs, or adding the new variable with the coeffecient if it does not exist
        in the dict of terms.

        Args:
            terms : Dict of terms
            var   : The var to search for different coefficents
            coeff : The coeff to be added.
        Return:
            terms : Dict of terms in the function

        """

        if var in terms:
            terms[var] += coeff
        else:
            terms[var] = coeff

        return terms


    def calculateFunction(self,terms, x):
        """
        Calculate the output of the terms dict given the value of the variable .

        Args:
            terms : Dict of converted terms
            x : The value of the variable input
        Return:
            y : The output of the function given x as input.

        """

        y = 0

        for var, coeff in terms.items():
            powerSignIndex = var.index("^")
            powerString = var[powerSignIndex + 1:]
            powerNumber = int(powerString)
            y += coeff * (x ** powerNumber)

        return y

    def splitNumeratorDenominator(self, func):

        """

            Split the function into a numerator and a denominator if the input function in the form of ex :-> x/x+1
            to be : numFn="x" , denFn="x+1" and the output f(x)= numFn(x)/denFn(x)

            Args:
                func : the input function.

            Return:
                numFn: the numerator term.
                denFn: the denominator term if exists, None otherwise.

        """

        numFn = func
        denFn = None

        for i, char in enumerate(func):
            if self.checkDivSign(char):
                numFn = func[0:i]
                denFn = func[i + 1:]
                break
        # print(numFn)
        # print(denFn)
        return numFn, denFn

    def splitBySigns(self, func):

        """
        Split the input function into terms by using the plus or minus sign as a delimeter

        Args:
            func : Input function
        Return:
            terms : List of terms in the function

        """

        terms = []
        term = ""

        for i, char in enumerate(func):

            if self.checkPlusOrMinusSign(char):
                if not (i == 0):
                    if not (self.checkPowerSign(func[i - 1])):
                        terms.append(term)
                        term = ""
            term += char

        terms.append(term)

        return terms

    def adjustTerms(self, terms):

        """
        Adjust the terms to a correct format to be processed ex: "x+x^2" -> "+1*x^1+1*x^2"

        Args:
            terms : List of terms in the function
        Return:
            terms : List of adjusted terms in the function

        """

        for i, term in enumerate(terms):

            addCoeff = True
            addPower = True
            addSign = True
            done = False

            if self.checkPlusOrMinusSign(term[0]):
                addSign = False

            for element in term:

                if not addCoeff and not addPower and not addSign:
                    break

                if self.checkMultSign(element):
                    addCoeff = False
                elif self.checkPowerSign(element):
                    addPower = False

            if not addSign:
                if terms[i][1:].isnumeric():
                    terms[i] = terms[i] + "*x^0"
                    done = True

            if terms[i].isnumeric() and not done:
                terms[i] = terms[i] + "*x^0"
                if addSign:
                    terms[i] = "+" + terms[i]
                    done = True

            if not done:
                if addSign:
                    terms[i] = "+" + terms[i]
                if addCoeff:
                    terms[i] = terms[i][0] + "1*" + terms[i][1:]
                if addPower:
                    terms[i] = terms[i] + "^1"

        return terms

    def splitCoefficents(self, terms):

        """
        Split the list of terms into a dict of variables with their accumualted coefficents

        Args:
            terms : List of adjusted terms
        Return:
            convertedTerms : dict of converted terms with the variables as key and the coefficents as values.

        """

        convertedTerms = {}
        coeff = ""
        var = ""

        for term in terms:

            for i, element in enumerate(term):

                if self.checkMultSign(element):
                    var = term[i + 1:]
                    break

                coeff += element

            convertedTerms = self.accumulateCoeffecients(convertedTerms, var, self.transformSignedStringToNumber(coeff))
            var = ""
            coeff = ""

        return convertedTerms

    def calculate(self, func, x):

        """
        Calculate the output of a function given the value of the variable input.

        Args:
            func : input function f(x)
            x : The value of the variable input
        Return:
            y : The output of the function given x as input.

        """
        yDen = 1

        numFn, denFn = self.splitNumeratorDenominator(func)

        if not (denFn is None):
            terms = self.splitBySigns(denFn)
            terms = self.adjustTerms(terms)
            # print(terms)
            terms = self.splitCoefficents(terms)
            # print(terms)
            yDen = self.calculateFunction(terms, x)
            # print(yDen)

        terms = self.splitBySigns(numFn)
        terms = self.adjustTerms(terms)
        # print(terms)
        terms = self.splitCoefficents(terms)
        # print(terms)
        yNum = self.calculateFunction(terms, x)
        # print(yNum)

        return yNum / yDen

    def __call__(self, function, minX, maxX, canvas):

        X = np.arange(minX, maxX + 1, 1, dtype=np.float64)
        Y = [self.calculate(function, x) for x in X]
        if(canvas is not None):
            canvas.clear()
            canvas.plot(X, Y)
        return Y
