'''
pygamegame.py
created by Lukas Peraza
 for 15-112 F15 Pygame Optional Lecture, 11/11/15
use this code in your term project if you want
- CITE IT
- you can modify it to your liking
  - BUT STILL CITE IT
- you should remove the print calls from any function you aren't using
- you might want to move the pygame.display.flip() to your redrawAll function,
    in case you don'd need to update the entire display every frame (then you
    should use pygame.display.update(Rect) instead)
'''
import pygame
from classes import Button, Note, Page, PopUpBox, menuButton, menuButtonButton, Project, Page, System, Measure, Note
import creating
import welcome
import edit
import pickletest



pygame.init()
screen = pygame.display.set_mode((0, 500))
clock = pygame.time.Clock()


############################################################################################################################

class PygameGame(object):
    def update(self, screenWidth, screenHeight):
        pass

    def init(self):
        welcome.init(self)

    def eInit(self):
        edit.init(self)
        projects = pickletest.loadAll()
        self.projectButtons = []
        for i in range(len(projects)):
            project = projects[i]
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
            text = str(projects[i])
            # text = project.scoreTitle
            button = Button(rect, text, (40,50,60))
            self.projectButtons.append(button)



    def directWelButtons(self, x, y):
        welcome.mousePressed(self, x, y)

    def directEditButtons(self, x,y):
        edit.mousePressed(self, x, y)
        for button in self.projectButtons:
            if button.pressed(x,y):
                self.init()
                # for project in self.projects:
                #     if button.text == project.scoreTitle:
                #         self.cInit(project.properties, project)

    def directWelcomKeys(self, keyCode, modifier):
        char = self.getKey(keyCode)
        welcome.keyPressed(self, char)

    def drawWelcomeScreen(self, screen):
        for button in self.buttons:
            button.draw(screen)
        self.drawPops(screen)

    def drawOldWorks(self,screen):
        for button in self.buttons:
            button.draw(screen)
        for button in self.projectButtons:
            button.draw(screen)
        self.drawPops(screen)

    def selectProject(self, x, y):
        edit.oldProj(self, x, y)

    def cInit(self, properties, project = None):
        creating.init(self, properties)

    def drawCreatingScreen(self, screen):
        #draw the seperating/formatting lines
        self.drawLines(screen)

        #draw the buttons
        for button in self.buttons:
            button.draw(screen)

        for button in self.menuButtons:
            button.draw(screen)

        #draw the pages of music
        self.project.draw(screen)

        #popUps - last becasue they should be ontop of the screen
        self.drawPops(screen)

    def drawPops(self, screen):
        if self.popUpup != None:
            self.popUpup.draw(screen)

    def directCreatingKeys(self, keyCode, modifier):
        if self.popUpup != None and self.popUpup.type == "input":
            char = self.getKey(keyCode)
            if char == '\r':
                if self.popUpup.button == 'title':
                    self.scoreTitle = self.popUpup.input
                    self.titleButton.text = self.scoreTitle
                    self.popUpup = None
                elif self.popUpup.button == "<--":
                    print(self.popUpup.input)
                    #SAVE NAME!
                    self.popUpup = None
                    self.init()
                elif self.popUpup.button == 'spec':
                    try:
                        welcome.correctFormTimeSig(self.popUpup.input)
                        self.timeSig = self.popUpup.input
                        self.popUpup = None
                    except:
                        question = "Please enter a valid time signature"
                        prev = "Please enter the time signature for your score (ex. 4/4)"
                        self.popUpup = PopUpBox((self.width/2, self.height/2), question, "ok", "spec", (prev, "input", "spec"))
            elif char == -1:
                self.popUpup.input = self.popUpup.input[:-1]
            elif char == None:
                self.popUpup.input += ""
            else:
                self.popUpup.input += char
        elif self.popUpup == None and self.canAdd:
            pass

    def pressingButtons(self, x, y):
        for button in self.buttons:
            if button.pressed(x,y):
                if button.text == "<--":
                    if not self.justSaved:
                        question = "Would you like to save?"
                        self.popUpup = PopUpBox((self.width/2, self.height/2), question, "Yes/No", '<--')
                    else:
                        self.init()
                elif button.text == "Sing":
                    #import testtiming
                    pass
                elif button.text == "Add Music":
                    self.canAdd = not self.canAdd
                elif button.text == "+":
                    pass
                elif button.text == "save":
                    self.justSaved = True
                    button.isPressed = False
                else:
                    #the title box
                    question = "Would you like to change the name of your score?"
                    self.popUpup = PopUpBox((self.width/2, self.height/2), question, "Yes/No", "title")

    def collapseAndOpen(self, drop=True):
        for button in self.menuButtons:
            button.y = button.y0 #close all
        if drop:
            for button in self.menuButtons:
                if button.y0 > self.openedMenu.y0:
                    height = 175
                    button.y += height


    def checkMenu(self,x,y,before=False):
        for button in self.menuButtons:
            if not self.oneOpened and button.pressed(x,y):
                button.openMenu()
                self.oneOpened = not self.oneOpened
                self.openedMenu = button
                self.collapseAndOpen()
            elif self.oneOpened and button is self.openedMenu and button.pressed(x,y):
                button.openMenu() #actually closes it
                self.oneOpened = not self.oneOpened #False
                self.openedMenu = None
                self.collapseAndOpen(False)
            elif self.oneOpened and button is not self.openedMenu and button.pressed(x,y):
                print("Y")
                self.openedMenu.isPressed = False
                self.openedMenu.openMenu() #close the open one
                self.openedMenu = button #open this one
                self.openedMenu.openMenu()
                self.collapseAndOpen()
        for button in self.menuButtons:
            for b in button.mbuttons:
                if b.pressed(x,y):
                    print("H")
                

    def directCreatingButtons(self, x, y):
        if self.popUpup == None:
            self.pressingButtons(x, y)
            self.checkMenu(x,y)
        else:
            self.pressPopups(x, y)


    def pressPopups(self, x, y):
        if self.popUpup.type == "Yes/No":
            if self.popUpup.button == '<--':
                if self.popUpup.whatPressed(x,y) == "Yes":
                    if self.scoreTitle == None:
                        question = "Enter a name for your score"
                        self.popUpup = PopUpBox((self.width/2, self.height/2), question, "input", "<--")
                    else:
                        #SAVE SOME SHIT
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
            if self.popUpup.button == "<--":
                if self.popUpup.whatPressed(x,y) == "enter":
                    print(self.popUpup.input)
                    #SAVE NAME!
                    self.popUpup = None
                    self.init()
            elif self.popUpup.button == "title":
                if self.popUpup.whatPressed(x,y) == "enter":
                    self.scoreTitle = self.popUpup.input
                    self.titleButton.text = self.scoreTitle
                    self.popUpup = None
            elif self.popUpup.button == "spec":
                if self.popUpup.whatPressed(x,y) == "enter":
                    print("hehe")
                    try:
                        welcome.correctFormTimeSig(self.popUpup.input)
                        self.timeSig = self.popUpup.input
                        self.popUpup = None
                    except:
                        question = "Please enter a valid time signature"
                        prev = "Please enter the time signature for your score (ex. 4/4)"
                        self.popUpup = PopUpBox((self.width/2, self.height/2), question, "ok", "spec", (prev, "input", "spec"))
        elif self.popUpup.type == "ok":
            if self.popUpup.whatPressed(x,y) == "ok":
                print("hehe")
                question, typ, button = self.popUpup.previous
                self.popUpup = PopUpBox((self.width/2, self.height/2), question, typ, button)
                #add more...

    
#######################################################################################################################################################################################

    def mousePressed(self, x, y):
        if self.creating:
            self.directCreatingButtons(x,y)
            # Note.init(self)
            # self.noteGroup.append(pygame.sprite.Group(Note(x+27, y)))
        elif self.welcome:
            self.directWelButtons(x,y)
        elif self.editing:
            self.directEditButtons(x, y)

    def keyPressed(self, keyCode, modifier): 
        if self.creating:
            self.directCreatingKeys(keyCode, modifier)
        elif self.welcome:
            self.directWelcomKeys(keyCode, modifier)
        # if self.creating:
        #     if pygame.key.name(keyCode) == "q": self.object = 'QuarterRest.png'
        #     elif pygame.key.name(keyCode) == "w": self.object = 'WholeNote.png'
        #     elif pygame.key.name(keyCode) == "h": self.object = 'HalfNote.png'
        #     elif pygame.key.name(keyCode) == "s": self.object = 'SixteenthNote.png'
        #     elif pygame.key.name(keyCode) == "e": self.object = 'SixteenthRest.png'
        #     elif pygame.key.name(keyCode) == "d": self.object = 'Treble Cleff.png'
        #     elif pygame.key.name(keyCode) == "b": self.object = 'Flat.png'
        #     elif pygame.key.name(keyCode) == "n": self.object = 'QuarterNote.png'
        #     elif pygame.key.name(keyCode) == "y": self.object = 'BaseClef.png'


    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        if self.creating:
            for button in self.menuButtons:
                print button.mbuttons

    def drawLines(self, screen):
        #vert (first - left, 2nd - right)
        pygame.draw.line(screen, (0,0,0), (self.leftCol,0), (self.leftCol, self.height))
        pygame.draw.line(screen, (0,0,0), (self.rightCol, 0), (self.rightCol, self.height))
        #horiz
        pygame.draw.line(screen, (0,0,0), (self.width*4/5, self.height*6/7), (self.width, self.height*6/7))
        pygame.draw.line(screen, (0,0,0), (0, self.height/10), (self.width/4, self.height/10))

        pygame.draw.line(screen, (0,0,0), (0, self.height/5), (self.width/4, self.height/5))

    def redrawAll(self, screen):
        if self.welcome:
            self.drawWelcomeScreen(screen)
        elif self.creating:
            self.drawCreatingScreen(screen)
        elif self.editing:
            self.drawOldWorks(screen)
        
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
        self.bgColor = (255,255,255)
        pygame.init()

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
            screen.fill(self.bgColor)
            self.redrawAll(screen)
            pygame.display.flip()

        pygame.quit()

def main():
    game = PygameGame()
    game.run()

if __name__ == '__main__':
    main()