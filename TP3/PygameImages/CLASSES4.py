import pygame
import welcome
import edit
import creating
from classes import Project, Page, System, Measure, Note, Button, menuButton, menuButtonButton, PopUpBox, TextBox
import pickletest
from SoundAnalyse import Recordyourvoice as TT

################################################################################################################################################
################################################################################################################################################
class PygameGame(object):

    def init(self):
        welcome.init(self)

    def eInit(self):
        edit.init(self)
        self.oldProjects = pickletest.loadAll()
        self.projectButtons = []
        for i in range(len(self.oldProjects)):
            project = self.oldProjects[i]
            y0 = self.height/2 + 20
            x0 = self.width/5
            space = 20
            maxProjectsX = 5
            maxProjectsY = 2
            width = ((self.width*3/5) - (space*(maxProjectsX-1)))/maxProjectsX
            height = ((self.height/2) - (space*maxProjectsY))/maxProjectsY
            x = x0 + i%maxProjectsX*(space + width)
            y = y0 if i < maxProjectsX else y0 + height + space
            rect = (x, y, width, height)
            text = project.scoreTitle
            button = Button(rect, text, (159,182,205))
            self.projectButtons.append(button)
        if len(self.oldProjects) == 0:
            text = "No Old Projects"
            button = Button((self.width/4, 2*self.height/3,self.width/2, self.height/4), text, (198,226,255), 0, False)
            self.buttons.append(button)
    def selectProject(self, x, y):
        edit.oldProj(self, x, y)

    def cInit(self, properties, project = None, saved = False):
        creating.init(self, properties, project, saved)

    def resetPage(self):
        for system in self.project.currentPage.systems:
            for measure in system.measures:
                measure.color = (0,0,0)
        self.canAdd = False
        self.selectedMeasure = None
        for button in self.buttons:
            if button.text == "Add Music":
                button.isPressed = False

    def pressPopups(self, x, y):
        if self.popUpup.type == "Yes/No":
            if self.popUpup.button == '<--':
                if self.popUpup.whatPressed(x,y) == "Yes":
                    pickletest.saveProject(self.project)
                    self.init()
                elif self.popUpup.whatPressed(x,y) == "No":
                    self.init()
            elif self.popUpup.button == "title":
                if self.popUpup.whatPressed(x,y) == "No":
                    self.popUpup = None
                elif self.popUpup.whatPressed(x,y) == "Yes":
                    question = "Would you like to change the name of your score?"
                    self.popUpup = PopUpBox((self.width/2, self.height/2), question, "input", "title")

        elif self.popUpup.type == "input":
            if self.popUpup.button == "title":
                if self.popUpup.whatPressed(x,y) == "enter":
                    self.project.scoreTitle = self.popUpup.input
                    self.project.titleButton.text = self.project.scoreTitle
                    self.popUpup = None
            elif self.popUpup.button == "Timebox":
                if self.popUpup.whatPressed(x,y) == "enter":
                    time = self.popUpup.input
                    self.popUpup = None
                    newBox = TextBox(time, (self.width/2-40, self.height/2-40, 80, 80))
                    self.project.textBoxes.append(newBox)
            elif self.popUpup.button == "Lyrics":
                if self.popUpup.whatPressed(x,y) == "enter":
                    words = self.popUpup.input
                    self.popUpup = None
                    newBox = TextBox(words, (self.width/2-40, self.height/2-40, 80, 80))
                    self.project.textBoxes.append(newBox)

        elif self.popUpup.type == "ok":
            if self.popUpup.whatPressed(x,y) == "ok":
                if self.popUpup.button == 'sing':
                    question = "*Recording*"
                    self.popUpup = (PopUpBox((self.width/2, self.height/2), 
                                            question, "display", "recording"))
                elif self.popUpup.button == "notesSung":
                    self.popUpup = None
                elif self.popUpup.button == "direc":
                    self.popUpup = None

    def mousePressed(self, x, y):
        if self.creating:
            if self.popUpup == None:
                if self.project.titleButton.pressed(x,y):
                    question = "Would you like to change the name of your score?"
                    self.popUpup = PopUpBox((self.width/2, self.height/2), question, "Yes/No", "title")
                self.pressedButtons(x,y)
                self.switchedPages(x,y)
                self.pickFromMenu(x,y)
                selectMeasure = self.rearrangeMusic(x,y)
                if selectMeasure:
                    self.selectMeasures(x,y)
                self.checkMenu(x,y)
            else:
                self.pressPopups(x,y)
        elif self.welcome:
            welcome.directWelMouse(self, x,y)
        elif self.editing:
            edit.directEditMouse(self, x, y)

    def pickFromMenu(self, x, y):
        if self.canAdd:
            if self.selectedMeasure != None:
                for button in self.menuButtons:
                    for feature in button.mbuttons:
                        if feature.pressed(x,y):
                            name = feature.fileName
                            newMusic = Note(name, x, y)
                            self.grabbed = newMusic

    def rearrangeMusic(self, x, y):
        if self.canAdd:
            if self.selectedMeasure != None:
                for feature in self.selectedMeasure.music:
                    if feature.containsPoint(x,y):
                        props = (feature.fileName, feature.x, feature.y, feature.upsideDown, feature.cross)
                        if props in self.selectedMeasure.musicDoc:
                            self.selectedMeasure.musicDoc.remove(props)
                        self.grabbed = feature
                        return False
                for textBox in self.project.textBoxes:
                    if textBox.pressed(x,y):
                        self.grabbed = textBox
                        return False
        return True

    def pressedButtons(self,x,y):
        self.justSaved = False
        for button in self.buttons:
            if button.pressed(x,y):
                if button.text == "+":
                    maxPages = 8
                    newPage = len(self.pages) + 1
                    if newPage <= maxPages:
                        page = Page(self.properties, newPage)
                        self.pages.append(page)
                        creating.addPageButtons(self)
                    else:
                        pass
                        #popUp
                elif button.text == "Add Music":
                    button.isPressed = not button.isPressed
                    self.canAdd = not self.canAdd

                elif button.text == "<--":
                    if not self.justSaved:
                        question = "Would you like to save?"
                        self.popUpup = PopUpBox((self.width/2, self.height/2), question, "Yes/No", '<--')
                    else:
                        self.init()
                elif button.text == "save":
                    self.justSaved = True
                    pickletest.saveProject(self.project)
                    self.cInit(None, project = self.project, saved = True)
                elif button.text == "Sing":
                    question = "Press OK to record"
                    self.popUpup = PopUpBox((self.width/2, self.height/2), question, "ok", 'sing')    
                elif button.text == "Directions":
                        question = "Press 'Add Music' to change the score \n\
Select a measure to change \n drag and drop into the measure\n \n Press\
'Sing' to obtain the notes you sing \n You must sing on the syllable 'Bah'\
 loudly and clearly into the microphone \n For best results, sing slowly"
                        self.popUpup = PopUpBox((self.width/2, self.height/2), 
                            question, "ok", 'direc')

    def switchedPages(self,x,y):
        for button in self.pageButtons:
            if button.pressed(x,y):
                pageNumber = int(button.text)
                if not self.project.currentPage.pageNumber == pageNumber:
                    #switching pages!
                    for page in self.pages:
                        if page.pageNumber == pageNumber:
                            self.resetPage()
                            self.project.currentPage = page

    def selectMeasures(self, x,y):
        if self.canAdd:
            for system in self.project.currentPage.systems:
                for measure in system.measures:
                    if measure.overMeasure(x,y):
                        if self.selectedMeasure != None and self.selectedMeasure != measure:
                            self.selectedMeasure.color = (0,0,0) #deselect the measure
                            self.selectedMeasure = measure
                            measure.color = (30,144,255) #select a new measure
                        elif self.selectedMeasure != None and self.selectedMeasure == measure:
                            self.selectedMeasure = None #deselect same measure
                            measure.color = (0,0,0)
                        elif self.selectedMeasure == None:
                            self.selectedMeasure = measure #select a measure
                            measure.color = (30,144,255)
        else:
            if self.selectedMeasure != None:
                self.selectedMeasure.color = (0,0,0)
                self.selectedMeasure = None

    def collapseAndOpen(self, drop=True):
        for button in self.menuButtons:
            button.y = button.y0 #close all
        if drop:
            for button in self.menuButtons:
                if button.y0 > self.openedMenu.y0:
                    height = 175
                    button.y += height


    def checkMenu(self,x,y):
        for button in self.menuButtons:
            if not button.text == "Time" and not button.text == "Lyrics":
                if not self.oneOpened and button.pressed(x,y):
                    button.isPressed = not button.isPressed
                    button.openMenu()
                    self.oneOpened = not self.oneOpened
                    self.openedMenu = button
                    self.collapseAndOpen()
                elif self.oneOpened and button is self.openedMenu and button.pressed(x,y):
                    button.isPressed = not button.isPressed
                    button.openMenu() #actually closes it
                    self.oneOpened = not self.oneOpened #False
                    self.openedMenu = None
                    self.collapseAndOpen(False)
                elif self.oneOpened and button is not self.openedMenu and button.pressed(x,y):
                    button.isPressed = not button.isPressed
                    self.openedMenu.isPressed = not self.openedMenu.isPressed
                    self.openedMenu.openMenu() #close the open one
                    self.openedMenu = button #open this one
                    self.openedMenu.openMenu()
                    self.collapseAndOpen()
            elif button.text == "Time":
                if button.pressed(x,y):
                    name = self.project.timeSig
                    answer = ""
                    for c in name:
                        if c != "\n":
                            answer+=c
                    question = "Your current time signature is %s, enter a time signature" % (answer)
                    self.popUpup = PopUpBox((self.width/2, self.height/2), question, "input","Timebox")

            elif button.text == "Lyrics":
                if button.pressed(x,y):
                    question = "Enter lyrics or instrument names to add to the score"
                    self.popUpup = PopUpBox((self.width/2, self.height/2), question, "input","Lyrics")


    def mouseReleased(self, x, y):
        if self.creating:
            self.insertMusic(x,y)

    def insertMusic(self, x, y):
        insert = False
        if self.canAdd:
            if self.selectedMeasure != None:
                if self.grabbed != None:
                    if self.selectedMeasure.overMeasure(x,y):
                        insert = True
                    else:
                        dynamicKeywords = ["cres", "piano", "forte"]
                        for word in dynamicKeywords:
                            if (self.grabbed.isTextBox) or (word in self.grabbed.fileName):
                                if self.project.currentPage.overPage(x,y):
                                    insert = True
        if insert:
            if not self.grabbed.isTextBox and self.grabbed.fileName[-5:-9:-1] == "etoN":
                y = self.imageRePosition[self.grabbed.fileName] + self.grabbed.y
                newY = self.selectedMeasure.findNearestLineOrSpace(y)
                y = newY - self.imageRePosition[self.grabbed.fileName]
            self.grabbed.x = x
            self.grabbed.y = y 
            self.grabbed.x0 = x
            self.grabbed.y0 = y
            self.grabbed.updateMe()
            # properties = self.grabbed.fileName, x, y, self.grabbed.upsideDown, self.grabbed.cross
            # self.selectedMeasure.musicDoc.append(properties)
            if not self.grabbed.isTextBox and not self.grabbed in self.selectedMeasure.music:
                self.selectedMeasure.music.add(self.grabbed)
                properties = (self.grabbed.fileName, self.grabbed.x, 
                                self.grabbed.y, self.grabbed.upsideDown, self.grabbed.cross)
                self.selectedMeasure.musicDoc.append(properties)
        elif self.grabbed != None and not insert:
            for button in self.buttons:
                if button.text == "Trash":
                    if button.pressed(x,y):
                        if self.grabbed.isTextBox:
                            self.project.textBoxes.remove(self.grabbed)
                        else:
                            self.selectedMeasure.music.remove(self.grabbed)
                            properties = (self.grabbed.fileName, self.grabbed.x0, 
                                self.grabbed.y0, self.grabbed.upsideDown, self.grabbed.cross)
                            # self.selectedMeasure.musicDoc.remove(properties)
            if self.grabbed in self.selectedMeasure.music:
                x, y = self.grabbed.x0, self.grabbed.y0
                self.grabbed.x = x
                self.grabbed.y = y
                self.grabbed.updateMe()
                props = (self.grabbed.fileName, x, y, self.grabbed.upsideDown, self.grabbed.cross)
                self.selectedMeasure.musicDoc.append(props)
        self.grabbed = None

    def mouseMotion(self, x, y):
        if self.creating:
            for system in self.project.currentPage.systems:
                for measure in system.measures:
                    if self.selectedMeasure == None:
                        if measure.overMeasure(x,y):
                            measure.color = (30,144,255)
                        else:
                            measure.color = (0,0,0)
            if self.selectedMeasure != None:
                for note in self.selectedMeasure.music:
                    if note.containsPoint(x,y):
                        note.drawBound = True
                    else:
                        note.drawBound = False


    def mouseDrag(self, x, y):
        if self.creating:
            if self.grabbed != None:
                self.grabbed.x = x
                self.grabbed.y = y
                self.grabbed.updateMe()

    def directCreatingKeys(self, keyCode, modifier):
        if self.popUpup != None and self.popUpup.type == "input":
            char = self.getKey(keyCode)
            if char == '\r':
                if self.popUpup.button == 'title':
                    self.project.scoreTitle = self.popUpup.input
                    self.project.titleButton.text = self.project.scoreTitle
                    self.popUpup = None
                elif self.popUpup.button == "Lyrics":
                    words = self.popUpup.input
                    self.popUpup = None
                    newBox = TextBox(words, (self.width/2-40, self.height/2-40, 80, 80))
                    self.project.textBoxes.append(newBox)
                elif self.popUpup.button == "Timebox":
                    time = self.popUpup.input
                    self.popUpup = None
                    newBox = TextBox(time, (self.width/2-40, self.height/2-40, 80, 80))
                    self.project.textBoxes.append(newBox)

            elif char == -1:
                self.popUpup.input = self.popUpup.input[:-1]
            elif char == None:
                self.popUpup.input += ""
            else:
                self.popUpup.input += char
            

    def keyPressed(self, keyCode, modifier):
        if self.creating:
            self.directCreatingKeys(keyCode, modifier)
        elif self.welcome:
            char = self.getKey(keyCode)
            welcome.keyPressed(self, char)

    def timerFired(self, dt): 
        if self.creating:
            if self.startRecording:
                i = 0
                while i < 200: #to get a delay so the popUp is drawn
                    i += 1
                notesSung = TT.inputSound()
                notesSung = str(notesSung)
                self.popUpup = None
                self.startRecording = False
                question = "You sang %s" % notesSung
                self.popUpup = PopUpBox((self.width/2, self.height/2), question, "ok", "notesSung")

        

    def drawCreatingScreen(self, screen):
        #draw the seperating/formatting lines
        self.drawLines(screen)
        #draw the buttons
        for button in self.buttons:
            button.draw(screen)
        for button in self.menuButtons:
            button.draw(screen)
        for button in self.pageButtons:
            if button.text == str(self.project.currentPage.pageNumber):
                button.isPressed = True
            else:
                button.isPressed = False
            button.draw(screen)
        for button in self.project.textBoxes:
            button.draw(screen)
        #draw the pages of music
        self.project.draw(screen)
        if self.grabbed != None and not self.grabbed.isTextBox:
            current = pygame.sprite.Group()
            current.add(self.grabbed)
            current.draw(screen)
            pygame.draw.rect(screen, (255,0,0), (self.grabbed.x, self.grabbed.y, 5,5))
        #popUps - last becasue they should be ontop of the screen
        self.drawPops(screen)

    def drawPops(self, screen):
        if self.popUpup != None:
            self.popUpup.draw(screen)
            if self.popUpup.button == "recording":
                self.startRecording = True

    def drawLines(self, screen):
        #vert (first - left, 2nd - right)
        pygame.draw.line(screen, (0,0,0), (self.leftCol,0), (self.leftCol, self.height))
        pygame.draw.line(screen, (0,0,0), (self.rightCol, 0), (self.rightCol, self.height))
        #horiz
        pygame.draw.line(screen, (0,0,0), (self.width*4/5, self.height*6/7), (self.width, self.height*6/7))
        pygame.draw.line(screen, (0,0,0), (0, self.height/10), (self.width/4, self.height/10))

        pygame.draw.line(screen, (0,0,0), (0, self.height/5), (self.width/4, self.height/5))

    def redrawAll(self,screen):
        if self.welcome:
            for button in self.buttons:
                button.draw(screen)
            self.drawPops(screen)
        elif self.creating:
            self.drawCreatingScreen(screen)
        elif self.editing:
            for button in self.buttons:
                button.draw(screen)
            for button in self.projectButtons:
                button.draw(screen)
            self.drawPops(screen)

    def getKey(self, keyCode):
        lShift = 304
        rShift = 303
        capslock = 301
        backspace = 8
        three = 51
        try:
            if self.isKeyPressed(lShift) or self.isKeyPressed(rShift) or self.isKeyPressed(capslock):
                if keyCode == three:
                    char = "#"
                else:
                    char = chr(keyCode)
                    char = char.upper()
            elif keyCode != backspace:
                char = chr(keyCode)
            return char
        except:
            if keyCode == backspace:
                return -1


    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def __init__(self, width=1200, height=800, fps=50, title="112 Pygame Game"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (255, 255, 255)
        pygame.init()

    def keyReleased(self, keyCode, modifier):
            pass

    def run(self):

        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.init()
        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False

            screen.fill((255, 255, 255))

            self.redrawAll(screen)
            pygame.display.flip()
        pygame.quit()


def main():
    game = PygameGame()
    game.run()

if __name__ == '__main__':
    main()

