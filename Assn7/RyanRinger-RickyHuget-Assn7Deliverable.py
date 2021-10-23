from tkinter import *
from tkinter import ttk
import re
'''
BNF2
    exp -> id = math;
    math -> int+math | float
BNF3
    Dec->type Exp
    Exp -> id = Math
    Math -> Multi + Multi
    Multi -> int * Multi | int
BNF4
    if_exp->(comparison_exp)
    comparison_exp -> id con_op comparison_exp
    con_op -> > | <
BNF5
    prn_exp-> print(value)
    value-> id | litrl | str_litrl 
'''
LIGHTGRAY = '#C4C5BF'
WHITE = '#FFFFFF'
DARKGRAY = '#65696B'

inToken = ("empty","empty")
outputList = []
BNFTAG = ""

def tinyPieLexerFirstToken(code):
    global outputList
    outputList = []
    while len(code) > 0:
        search = re.search(r'\s', code)
        # print(search)
        if search != None:
            code = re.sub(search.group(), '', code)
        else:

            if re.search(r'if|else|int|float|print', code) != None:
                search = re.search(r'if|else|int|float|print', code)
                if search.group() == "int" or search.group() == "float":                #keywords int and float
                    outputList.append(opFormat("kywrd", search.group()))
                    code = re.sub(search.group(), '', code, 1)

                elif search.group() == "if" or search.group() == "print":               #keywords if or print
                    outputList.append(opFormat("kywrd", search.group()))
                    code = re.sub(search.group(), '', code, 1)
                    if re.search(r'[\(]', code) != None:
                        code = parenthesis(code)

                else:                                                                   #keyword else
                    outputList.append(opFormat("kywrd", search.group()))
                    code = re.sub(search.group(), '', code, 1)


            elif re.search(r'\;|\:', code) != None:
                search = re.search(r'\;|\:', code)
                outputList.append(opFormat("sprtr", search.group()))
                code = re.sub(search.group(), '', code, 1)
            else:
                code = tinyPieLexerRemaining(code)


def parenthesis(code):
    global outputList

    search = re.search(r'[\(]', code)
    outputList.append(opFormat("sprtr", search.group()))
    code = tinyPieLexerRemaining(code)

    if re.search(r'[\)]', code) != None:
        search = re.search(r'[\)]', code)
        outputList.append(opFormat("sprtr", search.group()))
        code = re.sub(r'[\(][\)]', '', code, 1)
    return code

def quotations(code):
    global outputList

    search = re.search(r'\".*\"', code)
    outputList.append(opFormat("str_litrl", search.group()))
    code = re.sub(r'\".*\"', '', code, 1)
    return code

def tinyPieLexerRemaining(code):
    global outputList
    if re.search(r'[\"]', code) != None:
        code = quotations(code)
        code = tinyPieLexerRemaining(code)

    elif re.search(r'^\d+\.*\d*', code) != None:
        search = re.search('^\d+\.*\d*', code)
        outputList.append(opFormat("litrl", search.group()))
        code = re.sub(search.group(), '', code, 1)
        if re.search(r'[\=|\+|\<|\>|\*]', code) != None:
            search = re.search('[\=|\+|\<|\>|\*]', code)
            if search.group() == "<" or search.group() == ">" or search.group() == "+" or search.group() == "*":
                outputList.append(opFormat("oprtr", search.group()))
                code = re.sub(re.escape(search.group()), '', code, 1)
        code = tinyPieLexerRemaining(code)

    elif re.search(r'[A-Za-z_][A-Za-z0-9_]*', code) != None:
        search = re.search(r'[A-Za-z_][A-Za-z0-9_]*', code)
        outputList.append(opFormat("idntfr", search.group()))
        code = re.sub(search.group(), '', code, 1)


        if re.search(r'[\=|\+|\<|\>|\*]', code) != None:
            search = re.search('[\=|\+|\<|\>|\*]', code)

            outputList.append(opFormat("oprtr", search.group()))
            code = re.sub(re.escape(search.group()), '', code, 1)

            # if search.group() == "<" or search.group() == ">" or search.group() == "+" or search.group() == "*":
            #     outputList.append(opFormat("oprtr", search.group()))
            #     code = re.sub(re.escape(search.group()), '', code, 1)
            #
            # else:
            #     outputList.append(opFormat("oprtr", search.group()))
            #     code = re.sub(search.group(), '', code, 1)

        code = tinyPieLexerRemaining(code)

    return code


def opFormat(type, val):
    return type, val

def accept_token():
    global inToken
    if len(outputList) > 0:
        inToken = outputList.pop(0)
    # print("     accept token from the list:"+inToken[1])

# BNF5
#     prn_exp->print(value)
#     value-> id | litrl | str_litrl
#     litrl can be float or int
def bnf5prn_exp():
    global inToken
    global BNFTAG
    BNFTAG = BNFTAG + "prn_exp->print(value); "

    if (inToken[1] == "print"):
        BNFTAG = BNFTAG + "Print is = " + inToken[1]
        accept_token()
        if inToken[1] == "(":
            BNFTAG = BNFTAG + ", ( is = " + inToken[1]
            accept_token()
            bnf5value()
            BNFTAG = BNFTAG + "\n) is = " + inToken[1]
            accept_token()
def bnf5value():
    global inToken
    global BNFTAG
    BNFTAG = BNFTAG + "\nvalue-> id | litrl | str_litrl; "

    if(inToken[0] == "idntfr" or inToken[0] == "litrl" or inToken[0] == "str_litrl"):
        BNFTAG = BNFTAG + "value = " + inToken[1]
        accept_token()
    else:
        print("Error: you must have an identifier, a literal, or a string literal for value in prn_exp")

# BNF4
#     if_exp->(comparison_exp)
#     comparison_exp -> id com_op comparison_exp | id com_op id
#     com_op -> > | <
def bnf4if_exp():
    global inToken
    global BNFTAG
    BNFTAG = BNFTAG + "if_exp->(comparison_exp)"
    if (inToken[1] == "if"):

        BNFTAG = BNFTAG + "if is = " + inToken[1]
        accept_token()
        if inToken[1] == "(":
            BNFTAG = BNFTAG + ", ( is = " + inToken[1]
            accept_token()
            bnf4comparison_exp()
            BNFTAG = BNFTAG + "\n) is = " + inToken[1]
            accept_token()
    else:
        print("incorrect BNF Chosen, not_if")

def bnf4comparison_exp():
    global inToken
    global BNFTAG
    BNFTAG = BNFTAG + "\ncomparison_exp -> id com_op comparison_exp | id com_op id; "


    if(inToken[0] == "idntfr"):
        BNFTAG = BNFTAG + " ID = " + inToken[1]
        accept_token()
        if(inToken[1] == ">" or inToken[1] == "<"):
            BNFTAG = BNFTAG + ", com_op = " + inToken[1]
            accept_token()
            bnf4comparison_exp()

    else:
        print("Next token for comparison_exp must be a com_op")

# BNF3
#     Dec->type Exp
#     Exp -> id = Math
#     Math -> Multi + Multi
#     Multi -> int * Multi | int

def bnf3decl():
    global inToken
    global BNFTAG
    if (inToken[1] == "int" or inToken[1] == "float"):
        BNFTAG = BNFTAG + "Dec -> type Exp; "
        BNFTAG = BNFTAG + "type is = " + inToken[1]
        accept_token()
        bnf3exp()
    elif (inToken[0] == "idntfr"):
        print("Must use BNF2")
    else:
        print("wrong")



def bnf3exp():
    global BNFTAG

    global inToken;
    typeT,token=inToken;
    BNFTAG = BNFTAG + "\nExp -> Math; "
    if(typeT=="idntfr"):

        BNFTAG = BNFTAG + " ID is = " + token
        accept_token()

        if (inToken[1] == "="):
            BNFTAG = BNFTAG + " next token = " +inToken[1]
            accept_token()
            bnf3math()
        else:
            print("expect = as the second element of the expression!")
            return

    else:
        print("Should Have ID at start, Bad call")
        return




def bnf3math():
    global BNFTAG
    BNFTAG = BNFTAG + "\nMath -> Multi + Multi;"
    global inToken;
    typeT,token=inToken

    if(typeT == "idntfr" or typeT == "litrl"):
        BNFTAG = BNFTAG + " next token = " + inToken[1]
        accept_token()

        if(inToken[1] == "+"):
            BNFTAG = BNFTAG + " next token = " + inToken[1]
            accept_token()
            bnf3multi()
        else:
            print("error, Math must be Multi + Multi")

    else:
        print("bad token")

def bnf3multi():
    global BNFTAG
    BNFTAG = BNFTAG + "\nMulti -> int * multi | int; "
    global inToken;

    if(inToken[0] == "idntfr" or inToken[0] == "litrl"):
            BNFTAG = BNFTAG + "next token = " + inToken[1]
            accept_token()
            if(inToken[1]=="*"):
                BNFTAG = BNFTAG + ", next token = " + inToken[1]
                accept_token()
                bnf3multi()
    else:
        print("error")

def parsSelec():
    global outputList
    global inToken
    global BNFTAG
    accept_token()
    if(inToken[1] == "print"):
        bnf5prn_exp()
    elif(inToken[1] == "int" or inToken[1] == "float"):
        bnf3decl()
    elif(inToken[1] == "idntfr"):
        bnf3exp()
    elif(inToken[1] == "if"):
        bnf4if_exp()
    else:
        BNFTAG = BNFTAG + "Error: not suitable for available BNF grammars"

class LexerGui:
    def __init__(self, root):
        self.linecount = 0
        self.lastText = ""
        self.master = root
        self.lastindex = 0
        self.master.title("TinyPie GUI")

        self.frame = Frame(self.master, width=1000, height=800, bg=LIGHTGRAY)
        self.frame.grid(row=0, column=0)

        self.inputLabel = Label(self.frame, text="INPUT", bg=LIGHTGRAY)
        self.inputLabel.grid(row=0, column=0, padx = 10, pady = 10)

        self.outputLabel = Label(self.frame, text="OUTPUT", bg=LIGHTGRAY)
        self.outputLabel.grid(row=0, column=1, padx=10, pady=10)

        self.outputLabel = Label(self.frame, text="BNF", bg=LIGHTGRAY)
        self.outputLabel.grid(row=0, column=2, padx=10, pady=10)

        self.textField1 = Text(self.frame, width=30, height=20, bg=WHITE)
        self.textField1.grid(row=1, column=0, padx=10, pady=10)

        self.textField2 = Text(self.frame, width=30, height=20,  bg=WHITE)
        self.textField2.grid(row=1, column=1, padx=10, pady=10)

        self.textField3 = Text(self.frame, width=80, height=20, bg=WHITE)
        self.textField3.grid(row=1, column=2, padx=10, pady=10)

        self.lineValue = StringVar()
        self.lineValue.set("Current Line: N/A")
        self.lineNumber = Label(self.frame, textvariable=self.lineValue, bg=LIGHTGRAY)
        self.lineNumber.grid(row=2, column=0, padx=10, pady=10)

        # self.lineDisplay = Entry(self.frame)
        # self.lineDisplay.insert(0, self.linecount)
        # self.lineDisplay.grid(row=1, column=1)

        self.nextLineButton = Button(self.frame, text="Next Line", command=self.nextLine, width=10,  bg=DARKGRAY)
        self.nextLineButton.grid(row=3, column=0, padx=5, pady=5)

        self.quitButton = Button(self.frame, text="Quit", command=self.master.destroy, width=10, bg=DARKGRAY)
        self.quitButton.grid(row=3, column=2, padx=5, pady=5)


    def nextLine(self):
        global outputList
        global BNFTAG
        newIndex = 0
        tempString = self.textField1.get("1.0", END)
        # print(tempString)
        if self.lastindex < len(tempString):
            if tempString != self.lastText:
                self.linecount = 0
                self.lastindex = 0
                self.lastText = tempString
                self.textField2.delete("1.0", END)

            for i in range(self.lastindex, len(tempString)):
                if tempString[i] == '\n':
                    # print(i)
                    newIndex = i
                    break

            # print(type(newIndex))
            # print(type(self.lastindex))
            # print(type(tempString))
            thisLine = tempString[self.lastindex: newIndex: 1]
            tinyPieLexerFirstToken(thisLine)
            for item in outputList:
                self.textField2.insert(END, str(item) + '\n')
            print(outputList)
            parsSelec()
            BNFTAG = BNFTAG + '\n'
            self.textField3.insert(END, "^^^^ Parsing BNF tree for Line #" + str(self.linecount) + " ^^^^\n")
            self.textField3.insert(END, BNFTAG + '\n\n')
            BNFTAG = ""
            # self.textField2.insert(END, outputText)
            self.lastindex = newIndex + 1
            # print("Last Index = " + str(self.lastindex))


            self.lineValue.set("Current Line: " + str(self.linecount))
            self.linecount = self.linecount + 1



if __name__ == '__main__':
    root = Tk()
    myGui = LexerGui(root)
    root.mainloop()
    # tinyPieLexerFirstToken("print(\"I just built some parse trees \")")
    # print(outputList)
