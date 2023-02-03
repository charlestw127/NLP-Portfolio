#Charles Wallis
#CTW170000
#2/2/2023

import sys   
import os    
import re    
import pickle

class Person:
    def __init__(self, last, first, mi, id, phone):
        self.last = last   
        self.first = first 
        self.mi = mi       
        self.id = id       
        self.phone = phone 

    def display(self):
        print('\nEmployee ID    :', self.id)
        print('Employee Name  : ' + self.first + ' ' + self.mi + ' ' + self.last)
        print('Employee Phone : ' + self.phone)  

#open file from a data folder within the same folder as the python file
def readFile(filepath):
    with open(os.path.join(os.getcwd(), filepath), 'r') as f:
        text_in = f.read()
    return text_in

#return user's console input
def getInput(errorMsg):
        print(errorMsg)
        consoleResponse = input("Enter your new input: ")
        return consoleResponse 

#return data content without the header line (5 strings are popped in this case)
def removeHeader(data):
    data.reverse()
    for i in range(0, 5):
        data.pop(len(data)-1)
    data.reverse()
    return data 

#only alphas, and capitalize first letter
def verifyName(name):
    if len(name)==0:
        return verifyName(getInput("You must enter a name."))
    else:
        name = re.sub(r'[^a-zA-Z]', '', name) #only read the a-z and A-Z characters as name
    return name.capitalize() 

#only alpha, capital, single letter
def verifyMidInitial(middleInitial):
    middleInitial = re.sub(r'[^a-zA-Z]', '', middleInitial) #only read the a-z and A-Z characters as MI
    middleInitial = middleInitial.upper() #capitalize MI
    if len(middleInitial) < 1: #if MI is empty, set as X
        middleInitial = 'X'
    return middleInitial[0] 

#return ID with 2 uppercase letters followed by 4 digits
def verifyID(id):
    if not len(id) == 6: #verify length
        return verifyID(getInput("\nEmployee ID: " + id + " is invalid. Please enter two(2) letters followed by four(4) digits"))
    else:
        if not id[0:2].isalpha(): #verify that first 2 are letters
            return verifyID(getInput("\nEmployee ID: " + id + " is invalid. Please enter two(2) letters followed by four(4) digits"))
        else:
            if not id[2:6].isdigit(): #verify that last 4 are digits
                return verifyID(getInput("\nEmployee ID: " + id + " is invalid. Please enter two(2) letters followed by four(4) digits"))
            else:
                return id.upper() 
       
#return Phone number with 10 digits and dashes between them
def verifyPhone(num):
    num = re.sub('\D', '', num) #only read the numbers out of the input
    if not len(num) == 10: #if the phone number is not exactly 10 digits, ask for new number
        return verifyPhone(getInput("\nPhone Number: " + num + " is invalid. Please enter ten(10) digits"))
    num = num[0:3] + '-' + num[3:6] + '-' + num[6:] #add dashes
    return num 

#process data using above methods and put it all in a dictionary, then return the dictionary
def processData(inFile) :
    inFile = inFile.replace("\n", ',') # Replace \n to ,
    data = inFile.split(',') #split by comma
    data = removeHeader(data) #remove first line

    i = 0 
    personDict = {}
    while i < len(data):
        #LAST: capital case
        data = data[:i] + [verifyName(data[i])] + data[i + 1:]
        i += 1

        #FIRST: capital case
        data = data[:i] + [verifyName(data[i])] + data[i + 1:]
        i += 1

        #MIDDLE: single upper case letter
        data = data[:i] + [verifyMidInitial(data[i])] + data[i + 1:]
        i += 1

        #ID: 2 letters followed by 4 digits
        data = data[:i] + [verifyID(data[i])] + data[i + 1:]
        i += 1

        #PHONE NUMBER: 999-999-9999
        data = data[:i] + [verifyPhone(data[i])] + data[i + 1:]
        i += 1
        
        #p=person data (name, id, phone)
        p = Person(data[i-5], data[i-4], data[i-3], data[i-2], data[i-1])

        #if duplicate ID, display error, else add to dictionary
        if personDict.__contains__(p.id):
            print("Error adding: ")
            p.display()
            print("Employee above has duplicate key!\n")
        else:
            personDict[data[i-2]] = p
    return personDict

#main
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Specify the parameter to be data/data.csv')
    else:
        filePath = sys.argv[1] #set path to data.csv
        fileData = readFile(filePath) #read data.csv
        employeeList = processData(fileData) #process data.csv into employee list

        if len(employeeList) < 1:
            print("Error: No employees in dictionary.")
        else:
            #save dict in pickle
            pickle.dump(employeeList, open('employeeList.p', 'wb'))
            #load pickle file
            employee = pickle.load(open('employeeList.p', 'rb'))
            #display pickle file
            print("\n=====================Employee list=====================")
            for e in employee:
                employee[e].display()
