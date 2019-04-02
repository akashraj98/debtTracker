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
    '''Class which stores data for a single transaction.
       Specifically, stores
       direction: who is paying whom
       name: who is involved in transaction with the user
       amount: amount moved in the transaction'''

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
    '''Stores same data as transaction, with extra comment'''
    def __init__(self, direction, name, amount, comment):
        transaction.__init__(self, direction, name, amount)
        self.comment = comment

    def setComment(self, comment):
        self.comment = comment

    def getComment(self):
        return self.comment

    @classmethod
    def getTransaction(cls, transactionString):
        '''converts a transaction in string format 
           into a transaction object'''
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
    '''Stores list of detailedTransaction object'''
    def __init__(self, transactionList = []):
        self.data = transactionList[:]
   
    def addTransaction(self, transaction):
        '''adds transaction object to the list of transactions'''
        self.data += [transaction]
 
    def getTotalAmount(self, keyFunction = lambda x: True):
        '''get sum of amounts for each 'transaction for which keyFunction
           returns true' from the list of the transactions
           inputs:
           keyFunction: function taking one argument and returns true/false
           Returns float representing total amount'''
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
        '''adds detailedTransaction object to the record for a given date
           input:
           dtransaction: detailedTransaction object
           date: date object from datetime module, defaults to today's date object
        '''
        if date not in self.data.keys():
            self.data[date] = transactionList()
        self.data[date].addTransaction(dtransaction)

    def getTotalAmountforDate(self, keyFunction = lambda x: True,
                                    listKeyFunction = lambda x: True):
        '''Give total sum of amounts from 'transactions for which listKeyFunction returns True' 
           for 'dates for which keyFunction returns true

           input:
           keyFunction: function which takes date object and returns true/false
           listKeyFunction: function which takes detailedTransaction object and returns true/false
        '''
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
        '''loads record from the file fileName to the current 
           record object
           input:
           fileName: string'''
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

