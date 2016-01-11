import pygame
from classes import Button, Note, Page, PopUpBox

def init(self):
        #set the modes
        self.welcome = True
        self.creating = False
        self.editing = False

        # take care of popup stuff
        self.popUpup = None
        self.invalidReply = "Please enter a valid %s"

        # used if traveling to "Create New" screen
        self.properties = []

        #buttons on the screen
        left = (self.width/7, self.height*2/3, self.width*2/7, self.height/6)
        right = (self.width*4/7, self.height*2/3, self.width*2/7, self.height/6)
        center = (0, 0, self.width, self.height)
        
        welcome = Button(center, "Welcome", (198,226,255), meaning = False)
        oldProjects = Button(left, "Edit Old Project", (159,182,205))
        createNew = Button(right, "Create New", (159,182,205))
        self.buttons = [welcome, oldProjects, createNew]

def isKeyPressed(key):
    ''' return whether a specific key is being held '''
    return self._keys.get(key, False)

def keyPressed(self, char):
    if self.popUpup != None and self.popUpup.type == "input":
        if char == '\r':
            if self.popUpup.button == "title":
                self.properties.append(self.popUpup.input)
                question = "Please enter a time signature (ex. 4/4)"
                self.popUpup = PopUpBox((self.width/2, self.height/2), 
                    question, 'input', 'time')
            elif self.popUpup.button == "time":
                if correctFormTimeSig(self.popUpup.input):
                    self.properties.append(readTime(self.popUpup.input))
                    question = "Please enter a key (ex. Bb)"
                    self.popUpup = PopUpBox((self.width/2, self.height/2), 
                    question, 'input', 'key')
                else:
                    question = self.invalidReply % ("time signature")
                    self.popUpup = PopUpBox((self.width/2, self.height/2), 
                    question, 'ok', 'time')
            elif self.popUpup.button == "key":
                if correctFormKey(self.popUpup.input):
                    self.properties.append(self.popUpup.input)
                    question = "Please enter the number of staffs per system (<7)"
                    self.popUpup = PopUpBox((self.width/2, self.height/2), 
                        question, 'input', 'number')
                else:
                    question = self.invalidReply % ("key")
                    self.popUpup = PopUpBox((self.width/2, self.height/2), 
                    question, 'ok', 'key')
            elif self.popUpup.button == "number":
                if correctStaffForm(self.popUpup.input):
                    self.properties.append(int(self.popUpup.input))
                    self.popUpup = None
                    self.properties += [self.width, self.height]
                    self.cInit(self.properties)
                else:
                    question = self.invalidReply % ("number of staffs")
                    self.popUpup = PopUpBox((self.width/2, self.height/2), 
                    question, 'ok', 'number')
        elif char == -1:
            self.popUpup.input = self.popUpup.input[:-1]
        elif char == None:
            self.popUpup.input += ""
        else:
            self.popUpup.input += char

def readTime(timeSig):
    result = ""
    for i in range(len(timeSig)):
        if i != len(timeSig)-1 and timeSig[i+1] == "/":
            result += str(timeSig[i])
            result += "\n"
        elif i != 0 and timeSig[i-1] == "/":
            result += "\n"
            result += str(timeSig[i])
        else:
            result += str(timeSig[i])
    return result



def correctStaffForm(prompt):
    staffs = ["1","2","3","4","5","6"]
    return prompt in staffs
def correctFormKey(prompt):
    keys = ["C", "G", "D", "A", "E", "B", "F#", "C#", "F", "Bb", "Eb",
                                                         "Ab", "Db", "Gb"]
    return prompt in keys
def correctFormTimeSig(prompt):
    after = False
    count = 0
    error = False
    if prompt == "": error = True
    if "/" not in prompt: return False
    numbers = prompt.split("/")
    if len(numbers) != 2: error = True
    if int(numbers[-1])%2 != 0: error = True
    for c in prompt:
        if after:
            if not c.isdigit() or int(c) > 12:
                error = True
                break
        else:
            if c == "/":
                after = True
            else:
                if not c.isdigit() or int(c) > 12:
                    error = True
                    break
    return error == False

def directWelMouse(self, x, y):
        if self.popUpup == None:
            for button in self.buttons:
                if button.pressed(x,y):
                    if button.text == 'Edit Old Project':
                        self.eInit()
                    elif button.text == 'Create New':
                        question = "Please enter a title for your score"
                        self.popUpup = PopUpBox((self.width/2, self.height/2), 
                            question, "input", 'title')
        else: #pressPopups for Welcome
            if self.popUpup.button == "title":
                if self.popUpup.whatPressed(x,y) == "enter":
                    self.properties.append(self.popUpup.input)
                    question = "Please enter a time signature (ex. 4/4)"
                    self.popUpup = PopUpBox((self.width/2, self.height/2), 
                        question, 'input', 'time')
            elif self.popUpup.button == "time":
                if self.popUpup.whatPressed(x,y) == "enter":
                    if correctFormTimeSig(self.popUpup.input):
                        self.properties.append(self.popUpup.input)
                        question = "Please enter a key (ex. Bb)"
                        self.popUpup = PopUpBox((self.width/2, self.height/2), 
                        question, 'input', 'key')
                    else:
                        question = self.invalidReply % ("time signature")
                        self.popUpup = PopUpBox((self.width/2, self.height/2), 
                        question, 'ok', 'time')
                elif self.popUpup.whatPressed(x,y) == "ok":
                        question = "Please enter a time signature (ex. 4/4)"
                        self.popUpup = PopUpBox((self.width/2, self.height/2), 
                        question, 'input', 'time')

            elif self.popUpup.button == 'key':
                if self.popUpup.whatPressed(x,y) == "enter":
                    if correctFormKey(self.popUpup.input):
                        self.properties.append(self.popUpup.input)
                        question = "Please enter the number of staffs per system (<7)"
                        self.popUpup = PopUpBox((self.width/2, self.height/2), 
                            question, 'input', 'number')
                    else:
                        question = self.invalidReply % ("key")
                        self.popUpup = PopUpBox((self.width/2, self.height/2), 
                        question, 'ok', 'key')
                elif self.popUpup.whatPressed(x,y) == "ok":
                    question = "Please enter a key (ex. Bb)"
                    self.popUpup = PopUpBox((self.width/2, self.height/2), 
                    question, 'input', 'key')

            elif self.popUpup.button == 'number':
                if self.popUpup.whatPressed(x,y) == "enter":
                    if correctStaffForm(self.popUpup.input):
                        self.properties.append(self.popUpup.input)
                        self.popUpup = None
                        self.properties += [self.width, self.height]
                        self.cInit(self.properties)
                    else:
                        question = self.invalidReply % ("number of staffs")
                        self.popUpup = PopUpBox((self.width/2, self.height/2), 
                        question, 'ok', 'number')
                elif self.popUpup.whatPressed(x,y) == "ok":
                        question = "Please enter the number of staffs per system (<7)"
                        self.popUpup = PopUpBox((self.width/2, self.height/2), 
                        question, 'input', 'number')



