#!/usr/bin/env python3

import datetime

def parseDate(strDate):
    strDateList = strDate.split('-')
    year = int(strDateList[0])
    month = int(strDateList[1])
    day = int(strDateList[2])
    return datetime.date(year, month, day)

def readFile(fileName):
    try:
        with open(fileName) as f:
            fileString = f.read()
        return fileString
    except:
        return ''

class transaction():
    ''''''
    def __init__(self, direction, name, amount):
        '''direction: string, either one of '<-' or '->'
           name: string, entity with which transaction was performed
           amount: number, amount that was transferred during transaction'''
        self.direction = direction
        self.name = name
        self.amount = amount

    def setDirection(self, direction):
        self.direction = direction

    def setName(self, name):
        self.name = name

    def setAmount(self, amount):
        self.amount = amount

    def getDirection(self):
        return self.direction

    def getName(self):
        return self.name

    def getAmount(self):
        return self.amount

    def __repr__(self):
        return str(self.direction) + ' ' + str(self.name) + ' ' + str(self.amount)

class detailedTransaction(transaction):
    def __init__(self, direction, name, amount, comment):
        transaction.__init__(self, direction, name, amount)
        self.comment = comment

    def setComment(self, comment):
        self.comment = comment

    def getComment(self):
        return self.comment

    @classmethod
    def getTransaction(cls, transactionString):
        Parts = transactionString.split(r'//')
        try:
            try:
                comment = Parts[1]
            except:
                comment = ''
        
            nonComment = Parts[0]
            wordList = nonComment.split()
            if wordList[0] != '<-' and wordList[0] != '->':
                raise ValueError
            direction = wordList[0]
            if len(wordList[1]) == 0:
                raise ValueError
            name = wordList[1]
            amount = float(wordList[2])
        except:
            print('invalid transaction string :' + transactionString)
            direction = name = comment = ''
            amount = 0
        return detailedTransaction(direction, name, amount, comment)

    def __repr__(self):
        return transaction.__repr__(self) + r' //' + self.comment

class transactionList():
    def __init__(self, transactionList = []):
        self.data = transactionList[:]
   
    def addTransaction(self, transaction):
        self.data += [transaction]
 
    def getTotalAmount(self, keyFunction = lambda x: True):
        sum = 0
        for x in self.data:
            if keyFunction(x):
                if x.getDirection()[0] == '<':
                    sum += x.getAmount()
                elif x.getDirection()[1] == '>':
                    sum -= x.getAmount()
        return sum

    def __repr__(self):
        returnString = ''''''
        for x in self.data:
            returnString += x.__repr__() + '\n'
        return returnString

class record():
    def __init__(self, dct = {}):
        self.data = dct.copy()
    
    def addTransaction(self, dtransaction, 
                       date = datetime.date.today()):
        if date not in self.data.keys():
            self.data[date] = transactionList()
        self.data[date].addTransaction(dtransaction)

    def getTotalAmountforDate(self, keyFunction = lambda x: True,
                                    listKeyFunction = lambda x: True):
        sum = 0
        for x in self.data:
            if keyFunction(x):
                bla = self.data[x].getTotalAmount(listKeyFunction)
                sum += self.data[x].getTotalAmount(listKeyFunction)
        return sum
    
    def write(self, fileName):
        with open(fileName, 'w') as f:
            f.write(self.__repr__())
       
    def load(self, fileName):
        fileString = readFile(fileName)
        level = 0
        for line in fileString.split('\n'):
            if level == 0 and line:
                date = parseDate(line[:-1])
                level = 1
            elif level == 1:
                if line:
                    trans = detailedTransaction.getTransaction(line)
                    self.addTransaction(trans, date)
                else:
                    level = 0

    def __repr__(self):
        returnString = '''''' 
        for x in self.data:
            returnString += str(x) + ':\n'
            returnString += self.data[x].__repr__()
            returnString += '\n'
        return returnString

