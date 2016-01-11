import pygame
from classes import Button, Note, Page, PopUpBox, menuButton, menuButtonButton, Project, Page, System, Measure, Note


def init(self, properties, project = None, saved = False):
    #reset the modes
    self.creating = True
    self.welcome = False
    self.editing = False

    if project == None:
        #create a new project (coming from welcome screen)
        self.project = Project(properties)
    else:
        #load in an 'Old Work' (coming from edit screen)
        self.project = project
        #save the old version into the one that's about to be changed
        self.project.project0 = project #won't get modified

    self.properties = self.project.properties

    #a list with all the pages
    self.pages = self.project.pages
    self.project.currentPage = self.pages[0]

    #initialize all the buttons on the page
    cbuttonInit(self)

    self.startRecording = False

    self.popUpup = None
    self.justSaved = saved
    print saved

    #For the menu of features to add to score
    self.selectedMeasure = None
    self.canAdd = False
    self.grabbed = None
    self.oneOpened = False
    self.openedMenu = None
    self.imageRePosition = {'QuarterNote.png':(12),
    'SixteenthNote.png':(13),'WholeNote.png':(-5),
    'HalfNote.png':(11), 'EighthNote.png':(12)}


    # question = "Please enter the time signature for your score (ex. 4/4)"
    # specs = PopUpBox((self.width/2, self.height/2), question, "input", "spec")
    # self.popUpup = specs

def addPageButtons(self):
    r, g, b = (137,147,157) 
    for i in range(len(self.pages)):
        r += 9
        g += 10
        b += 12
        margin = 10
        width = self.width/5 - margin*2
        height = (self.height - 11*margin - self.height/10)/10
        x = self.width*4/5 + margin
        y = self.height/10 + margin + i*(height+margin)
        rect = (x, y, width, height)
        text = str(self.pages[i].pageNumber)
        button = Button(rect, text, (r, g, b))
        self.pageButtons.append(button)





def cbuttonInit(self):

    self.pageButtons = []
    #initiate the page buttons
    addPageButtons(self)


    self.leftCol = self.width/4
    self.rightCol = self.width*4/5

    self.buttons = []
    #initiate all regular buttons
    margin = 10
    back = (0, 0, 100, 80)
    singRect = (margin, self.height/margin+margin, self.width/8-2*margin, self.height/margin-2*margin)
    newRect = (self.leftCol/2+margin, self.height/margin+margin, self.width/8-2*margin, self.height/margin-2*margin)
    addRect = (self.rightCol + margin, self.height*6/7+margin, self.width/margin - 2*margin, self.height/7-2*margin)
    saveRect = (self.width*9/margin + margin, self.height*6/7+margin, self.width/margin - 2*margin, self.height/7-2*margin)
    pagesRect = (self.width*4/5 + margin, margin, self.width/5-2*margin, self.height/margin-2*margin)
    trashRect = (margin, self.height*6/7 + margin, self.width/4 - 2*margin, self.height/7 - 2*margin)
    directRect = (margin + 100, margin, 
                        self.width/4 - 2*margin - 100, self.height/10 - 2*margin)

    backButton = Button(back, "<--", (108,123,139))
    sing = Button(singRect,"Sing", (130,140,150))
    newNote = Button(newRect, "Add Music", (130,140,150))
    add = Button(addRect, "+", (198,226,255))
    save = Button(saveRect, "save", (198,226,255))
    pages = Button(pagesRect, "Pages", (108,123,139), meaning =False)
    trash = Button(trashRect, "Trash", (198,226,255), meaning = False)
    direct = Button(directRect, "Directions", (198,226,255))
    self.buttons += [pages, backButton, sing, newNote, add, save, trash, direct]


    self.features = ["Notes", "Rests", "Dynamics", "Time", "Clefs", "Lyrics", "Accidentals"]
    #initiate the other menu buttons
    self.menuButtons = []
    topOfMenu = self.height/5 + margin
    spread = margin
    height = ((self.height*4/5 - margin*(len(self.features)+1))/len(self.features))/2
    width = self.width/4 - 2*margin
    x = margin
    r, g, b = (137,147,157) #198;226;255
    for i in range(len(self.features)):
        feature = self.features[i]
        y = topOfMenu + i*(height+spread)
        rect = (x,y, width, height)
        button = menuButton(rect, feature, (r, g, b))
        self.menuButtons.append(button)
        r += 9
        g += 10
        b += 12















