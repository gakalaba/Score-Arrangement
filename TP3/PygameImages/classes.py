
import pygame
class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, image, radius):
        super(GameObject, self).__init__()
        # x, y define the center of the object
        self.x, self.y, self.image, self.radius = x, y, image, radius
        self.baseImage = image.copy()  # non-rotated version of image
        w, h = image.get_size()



    def writeText(self, screen, text, Rect, color=(0,0,0), shift = 0):
        #Rect - not center
        x, y, width0, height0 = Rect
        centerX = x + width0/2
        centerY = y + height0/2
        #find new line breaks:
        textLines = text.splitlines()
        fontSize = 35
        proportion = 0.5
        """Tried to get font to adapt to text box, ran too slowly in creating screen"""
        # while True:
        #     fontSize += 1
        #     fonte = pygame.font.Font(None, fontSize)
        #     wholeSize = fonte.size(text)
        #     wid, hei= wholeSize[0], wholeSize[1]*len(textLines)
        #     if wid >= proportion*width or hei >= proportion*height:
        #         #found font size
        #         break
        # if not "\n" in text:
        #     width, height = wholeSize[0], wholeSize[1]
        #     ren = fonte.render(text,0,color)
        #     newX = centerX - width/2
        #     newY = centerY - height/2 - shift
        #     screen.blit(ren, (newX, newY))

        fonte = pygame.font.Font(None, fontSize)
        size = fonte.size(text)
        width, height = size[0], size[1]
        if "\n" in text:
            margin = 10
            for i in range(len(textLines)):
                text = textLines[i]
                fonte = pygame.font.Font(None, 20)
                wholeSize = fonte.size(text)
                width, height = wholeSize[0], wholeSize[1]
                ren = fonte.render(text,0,color)
                x1 = centerX - width/2
                y1 = y + height*i + margin/2
                screen.blit(ren, (x1, y1))
        elif width > width0:
            fonte = pygame.font.Font(None, 20)
            size = fonte.size(text)
            width, height = size[0], size[1]
            ren = fonte.render(text,0,color)
            newX = centerX - width/2
            newY = centerY - height/2 - shift
            screen.blit(ren, (newX, newY))

        else:
            ren = fonte.render(text,0,color)
            newX = centerX - width/2
            newY = centerY - height/2 - shift
            screen.blit(ren, (newX, newY))
        
class Note(pygame.sprite.Sprite):
    # we only need to load the image once, not for every ship we make!
    #   granted, there's probably only one ship...

    def __init__(self, fileName, x, y, upsideDown=False, cross= False):
        
        self.fileName= fileName
        #need special ratios of size of image for each
        imageScales = {'Treble Cleff.png':(20, 60), 'BaseClef.png':(24,48), 
        'QuarterNote.png':(15,45), 'flat.png':(6,18),'sharp.png':(7,21), 
        'accidental.png':(7,21), 'SixteenthNote.png':(27,45),
        'WholeNote.png':(18,12),'HalfNote.png':(15,45), 
        'EighthNote.png':(27,45), 'QuarterRest.png':(12,36), 
        'SixteenthRest.png':(13,32), 'EighthRest.png':(12,23), 
        'WholeRest.png':(19,7),'HalfRest.png':(18,6),'Dot.png':(4,4), 
        'crescendo.png':(120,15), 'decrescendo.png':(120,12), 
        'piano.png':(15,16), 'mpiano.png':(24,15), 'ppiano.png':(23,16),
        'forte.png':(19,19), 'mforte.png':(26,21), 'fforte.png':(25,20)}

        self.scale = imageScales[fileName]
        Note.noteImage = pygame.transform.scale(pygame.transform.scale(
                pygame.image.load(fileName).convert_alpha(),
                (60, 100)), self.scale)
        if upsideDown:
            Note.noteImage = pygame.transform.rotate(Note.noteImage, -180)
        self.image = Note.noteImage
        #to make bounding box
        w, h = self.scale
        dx, dy = w/2, h/2
        space = 5
        self.y = y
        self.x = x
        self.rect = (self.x-dx-space,self.y-dy-space, w + 2*space, h + 2*space)
        super(Note, self).__init__()
        self.y0 = self.y
        self.x0 = self.x
        self.drawBound = False
        self.cross = cross
        self.upsideDown = upsideDown
        self.isTextBox = False

    def updateMe(self):
        x = self.x
        y = self.y
        w, h = self.scale
        dx, dy = w/2, h/2
        space = 5
        self.rect = (x-dx-space,y-dy-space, w + 2*space, h + 2*space)

    def __repr__(self):
        return self.fileName

    def drawBoundingBox(self, screen):
        x, y, w, h = self.rect
        if not self.fileName == "crescendo.png" and not self.fileName == "decrescendo.png":
            x -= w/5
        y -= h/6
        h += 6
        rect = (x,y,w,h)
        pygame.draw.rect(screen, (0,0,0), rect, 1)
        
    def drawCross(self, screen):
        width = 20
        x = self.x-width/2
        
        if (self.fileName == "QuarterNote.png" or 
                                    self.fileName == "HalfNote.png"):
            y = self.y+11 if not self.upsideDown else self.y - 11
        elif self.fileName == "WholeNote.png":
            y = self.y
        elif self.fileName == "SixteenthNote.png":
            y = self.y + 13
            x -= 2
            width = 18
        elif self.fileName == "EighthNote.png":
            y = self.y + 12 
            x -= 3
        x1 = x + width
        pygame.draw.line(screen, (0,0,0), (x,y), (x1,y))

    def containsPoint(self, x, y):
        x0, y0, w, h = self.rect
        if x >= x0 and x <= x0 + w:
            if y >= y0 and y <= h + y0:
                return True
        return False


class Project(GameObject):
    def __init__(self, properties, yes=True):
        #score properties (inherited by pages and down)
        self.scoreTitle, self.timeSig, self.key, self.sysSize, self.width, self.height = properties
        self.properties = properties
        #extra properties of time to break down
        self.beats = (self.timeSig.split("\n"))[0] #the top number (number of beats per measure)
        self.unit = (self.timeSig.split("\n"))[-1] #the bottom number (which note gets one 1 beat)
        self.project0 = None #to recognize what the project used to be when resaving
        if yes:
            #initialize project pages
            self.pages = []
            page1 = Page(self.properties, 1)
            self.pages.append(page1)
            self.currentPage = self.pages[0]
        #get the title button
        self.margin = self.height/5 #used to put in title button
        margin = 10
        width = self.width - self.width/4 - self.width/5
        textRect = (self.width/4+margin,margin,width - 2*margin,
                                                        self.margin-2*margin)
        self.titleButton = Button(textRect, self.scoreTitle, (198,226,255))
        self.textBoxes = [] #these get added while the user changes the project

    def draw(self, screen):
        self.titleButton.draw(screen)
        self.currentPage.draw(screen)

    def __repr__(self):
        title, time, key, size, wid, hei = self.properties
        props = title, time, key, size, wid, hei
        props = str(props)
        return "Proj(%s)" % (props)

    def __eq__(self, other):
        return ((isinstance(other, Project) and 
                    (self.properties == other.properties)))

class Page(Project):
    def __init__(self, properties, number = 1,yes=True):
        super(Page, self).__init__(properties, False)
        self.pageNumber = number
        self.sysSize = int(self.sysSize)
        #get dimensions for page
        self.x = self.width/4
        self.y = 0
        width = self.width #the whole canvases width
        #page width
        self.width = width - self.width/4 - self.width/5 #lines set up in draw creating function
        self.Rect = (self.x, self.y, self.width, self.height)

        #set out page set up dimensions for other classes too (inherited)
        margin = 10
        self.lines = 5 #there are 5 lines per staff
        self.lineSpace = 15  #there will be 15 pixels of space between them
        self.measureHeight = self.lineSpace*(self.lines-1)
        self.systemSpread = 3*self.lineSpace #space between staffs
        self.systemHeight = (self.measureHeight*self.sysSize + 
                                            self.systemSpread*(self.sysSize-1))
        self.leftMargin = self.width/12
        self.systemWidth = self.width - self.leftMargin - margin
        if yes:
            #intitialize page systems
            maxNumberOfStaffs = 6 #regardless of systems, only 6 staffs per page
            if self.sysSize > 3: #if there are 4, 5, 6 staffs per system...
                self.numSystems = 1 #each page will have only 1 system
            else:
                self.numSystems = maxNumberOfStaffs/self.sysSize
            self.systems = []
            for sys in range(self.numSystems):
                sysSeparation = 45
                x = self.x + self.leftMargin
                y = (self.y + self.margin + margin + 
                                            sys*(self.systemHeight+sysSeparation))
                system = System(x, y, self.properties)
                self.systems.append(system)


    def draw(self, screen):
        pygame.draw.rect(screen, (0,0,0), self.Rect, 2)
        for i in range(self.pageNumber):
            x = 400 + 70*i
        for system in self.systems:
            system.draw(screen)

    def __repr__(self):
        return "Page(%s)" % (self.pageNumber)

    def overPage(self, x, y):
        topMargin = self.height/5 #used to put in title button
        margin = 10
        if x >= self.x and x <= self.x + self.width:
            if y >= self.y + topMargin + margin and y <= self.height:
                return True
        return False



class System(Page):
    def __init__(self, x, y, properties, yes=True):
        super(System, self).__init__(properties, yes=False)
        self.x = x
        self.y = y


        #initialize measure contained inside system
        self.numberOfMeasures = 3 #3 measures per staff per system
        self.measureWidth = self.systemWidth/self.numberOfMeasures
        if yes:
            self.measures = []
            for staff in range(self.sysSize):
                #per staff  in a system, initiate the measures
                for measure in range(self.numberOfMeasures):
                    if staff == 0 and measure == 0: 
                        first = True
                    elif measure == 0:
                        first = None
                    else:
                        first = False
                    x = self.x + measure*self.measureWidth
                    y = self.y + staff*(self.measureHeight + self.systemSpread)
                    measure = Measure(x, y, first, self.properties)
                    self.measures.append(measure)

    def draw(self, screen):
        pygame.draw.line(screen, (0,0,0), (self.x, self.y), 
                                                    (self.x, self.y + self.systemHeight))
        for measure in self.measures:
            measure.draw(screen)

    def __repr__(self):
        return "System(%d, %d)" % (self.x, self.y)


class Measure(System):
    def __init__(self, x, y, first, properties):
        super(Measure,self).__init__(x, y, properties, False)
        self.first = first
        self.color = (0,0,0)
        #musical properties
        self.measure = {}
        self.music = pygame.sprite.Group()
        self.musicDoc = []
        #the lines of a measure 
        self.allLines = {}
        for line in range(self.lines): #5 lines
            notes = ["F", "D", "B", "G", "E"]
            lineY = self.y + self.lineSpace*line
            note = notes[line]
            self.allLines[note] = lineY

    def findNearestLineOrSpace(self, y):
        for note in self.allLines:
            lineY = self.allLines[note]
            dy = y - lineY
            if (dy >= -4 and dy <= 0) or (dy >= 0 and dy <= 4):
                return lineY
            elif dy >= 4 and dy <= 11:
                return lineY + 7

    def __repr__(self):
        return "Meas(%d, %d)" % (self.x, self.y)


    def overMeasure(self, x, y):
        if x >= self.x and x <= self.x + self.measureWidth:
            if y >= self.y and y <= self.y+self.measureHeight:
                return True
        return False

    def draw(self, screen):
        x1 = self.x + self.measureWidth
        for line in range(self.lines):
            x = self.x
            y = self.y + line*self.lineSpace
            pygame.draw.line(screen, self.color, (x,y), (x1, y))
        #draw verical end line
        pygame.draw.line(screen, (0,0,0), (x1, self.y), 
                                        (x1, self.y+self.measureHeight))

        try: 
            self.music.draw(screen)
        except:
            self.music = pygame.sprite.Group()
            for noteProps in self.musicDoc:
                properties = noteProps
                newNote = Note(*properties)
                self.music.add(newNote)
            self.music.draw(screen)
        for note in self.music:
            if note.drawBound:
                note.drawBoundingBox(screen)



    def overNote(self, note, x,y):
        lineY = self.allLines[note]
        error = self.lineSpace/4
        if x >= self.x and x <= self.x + self.measureWidth:
            if y >= lineY - error and y <= lineY + error:
                return True
        return False





################################################################################################################################################
################################################################################################################################################







class Button(GameObject):
    def __init__(self, Rect, text, color, border=2, meaning = True):
        self.x, self.y, self.width, self.height = Rect
        self.Rect = Rect
        centerX = self.x + self.width/2
        centerY = self.y + self.height/2

        self.text = text
        self.border = border

        self.color = color
        r, g, b = color
        shade = 45
        r = max(r - shade, 0)
        g = max(g - shade, 0)
        b = max(b - shade, 0)
        self.pressedColor = (r, g, b)

        #To be able to draw boxes as buttons, but not select them
        self.meaning = meaning
        self.isPressed = False
        self.isTextBox = False
        
    def __repr__(self):
        return self.text

    def __eq__(self, other):
        return isinstance(other, self) and self.Rect == other.Rect

    def draw(self, screen):
        if self.isPressed:
            color = self.pressedColor
        else:
            color = self.color
        rect = self.x, self.y, self.width, self.height
        pygame.draw.rect(screen, color, rect)
        if not self.border == 0:
            pygame.draw.rect(screen, (0,0,0), rect, self.border)
        if self.text == "Welcome" or self.text == "Old Projects":
            shifted = self.height/6
        else:shifted = 0
        self.writeText(screen, self.text, 
                            (self.x, self.y, self.width, self.height), shift=shifted)

    def pressed(self, x, y):
        x0, y0, width, height = self.x, self.y, self.width, self.height
        if self.meaning or self.text=="Trash":
            if x >= x0 and x <= (x0 + width):
                if y >= y0 and y <= (y0 + height):
                    return True
        return False

imagePositions = {'Treble Cleff.png':(45, 490), 'BaseClef.png':(145, 500),
        'accidental.png':(45, 615), 'flat.png':(110, 615),'sharp.png':(175, 615),
        'QuarterNote.png':(40, 280),'EighthNote.png':(95, 280),
        'SixteenthNote.png':(155, 280),'HalfNote.png':(210, 280),
        'WholeNote.png':(262, 280),'QuarterRest.png':(45, 320),
        'EighthRest.png':(140, 320),'SixteenthRest.png':(220, 320),
        'HalfRest.png':(80, 390),'WholeRest.png':(180, 390),
        'mforte.png':(50, 345),'mpiano.png':(50, 405),'forte.png':(150, 345),
        'piano.png':(150, 405),'fforte.png':(250, 345),
        'ppiano.png':(250, 405),'crescendo.png':(85, 460),
        'decrescendo.png':(220, 460)}




class menuButton(Button):
    def __init__(self, Rect, feature, color):
        super(menuButton, self).__init__(Rect, feature, color)
        self.mbuttons = []
        self.y0 = self.y



    def openMenu(self):
        if self.isPressed:
            global imagePositions
            if self.text == "Notes":
                quarter = menuButtonButton(imagePositions, 'QuarterNote.png')
                eight = menuButtonButton(imagePositions, 'EighthNote.png')
                sixteenth = menuButtonButton(imagePositions, 'SixteenthNote.png')
                half = menuButtonButton(imagePositions, 'HalfNote.png')
                whole = menuButtonButton(imagePositions, 'WholeNote.png')
                self.mbuttons = [quarter, eight, sixteenth, half, whole]
            elif self.text == "Rests":
                quarter = menuButtonButton(imagePositions, 'QuarterRest.png')
                eight = menuButtonButton(imagePositions, 'EighthRest.png')
                sixteenth = menuButtonButton(imagePositions, 'SixteenthRest.png')
                half = menuButtonButton(imagePositions, 'HalfRest.png')
                whole = menuButtonButton(imagePositions, 'WholeRest.png')
                self.mbuttons = [quarter, eight, sixteenth, half, whole]
            elif self.text == "Dynamics":
                pp = menuButtonButton(imagePositions, 'ppiano.png')
                mp = menuButtonButton(imagePositions, 'mpiano.png')
                p = menuButtonButton(imagePositions, 'piano.png')
                f = menuButtonButton(imagePositions, 'forte.png')
                ff = menuButtonButton(imagePositions, 'fforte.png')
                mf = menuButtonButton(imagePositions, 'mforte.png')
                cres = menuButtonButton(imagePositions, 'crescendo.png')
                decres = menuButtonButton(imagePositions, 'decrescendo.png')
                self.mbuttons = [pp, mp, p, f, ff, mf, cres, decres]
            elif self.text == "Time":
                pass
            elif self.text == "Clefs":
                treble = menuButtonButton(imagePositions, 'Treble Cleff.png')
                bass = menuButtonButton(imagePositions, 'BaseClef.png')
                self.mbuttons = [treble, bass]
            elif self.text == "Lyrics":
                pass
            elif self.text == "Accidentals":
                flat = menuButtonButton(imagePositions, 'flat.png')
                sharp = menuButtonButton(imagePositions, 'sharp.png')
                natural = menuButtonButton(imagePositions, 'accidental.png')
                self.mbuttons = [flat, sharp, natural]
        else:
            self.mbuttons = []

    def draw(self, screen):
        super(menuButton, self).draw(screen)
        if self.isPressed:
            if not self.text == "Lyrics" and not self.text == "Time":
                w = self.width
                height = 175
                rect = (self.x, self.y+self.height, w, height)
                pygame.draw.rect(screen, (0,0,0), rect,2)
                for button in self.mbuttons:
                    button.draw(screen)


class menuButtonButton(Button):
    def __init__(self, imagePositions, fileName):
        cX, cY = imagePositions[fileName]
        self.fileName = fileName
        self.image = pygame.sprite.Group()
        image = Note(self.fileName, cX, cY)
        self.image.add(image)
        self.Rect = image.rect
        super(menuButtonButton, self).__init__(self.Rect, self.fileName, (255,255,255))
        # self.text = fileName
        # self.meaning = True
    def draw(self, screen):
        self.image.draw(screen)
        for image in self.image:
            image.drawBoundingBox(screen)
            # pygame.draw.rect(screen, (0,0,0),self.Rect, 2)



class PopUpBox(GameObject):
    def __init__(self, center, text, typ, button, border=2):
        self.width = 700
        self.height = 200
        self.color = (30,144,255)
        self.cX = center[0] #center x coordinate of the window
        self.cY = center[1] #center y coordinate of the window
        self.x = self.cX - self.width/2
        displacement = self.height/2
        self.y = self.cY - self.height/2 - displacement

        self.Rect = (self.x, self.y, self.width, self.height)
        self.text = text
        self.border = border
        self.type = typ
        self.button = button

        if self.type == 'Yes/No':
            x = self.x + self.width/8
            y = self.y + self.height*3/4
            width = self.width/4
            height = self.height/6
            #establish buttons on surface of popup
            self.yes = Button((x, y, width, height), "Yes", (255,255,255))
            x = self.x + self.width*5/8
            self.no = Button((x, y, width, height), "No", (255,255,255))
        elif self.type == 'input':
            x = self.x + self.width/3
            y = self.y + self.height*3/4
            width = self.width/3
            height = self.height/6
            rect = x, y, width, height
            self.enter = Button(rect, "Enter", (255,255,255))
            self.input = ''
        elif self.type == 'ok':
            x = self.x + self.width/4
            y = self.y + self.height*2/3
            width = self.width/2
            height = self.height/6
            rect = (x, y, width, height)
            self.ok = Button(rect, "Ok", (255,255,255))

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.Rect)
        pygame.draw.rect(screen, (0,0,0), self.Rect, 2)
        if self.type == 'Yes/No':
            self.writeText(screen, self.text, self.Rect)
            self.yes.draw(screen)
            self.no.draw(screen)
        elif self.type == 'input':
            shift = 20
            self.writeText(screen, self.text, self.Rect, shift = shift)
            #enter screen
            x = self.x + self.width/7
            y = self.y + self.height*2/3 - shift
            width = self.width*5/7
            height = self.height/6
            rect = x, y, width, height
            pygame.draw.rect(screen, (self.color), rect)
            pygame.draw.rect(screen, (0,0,0), rect, self.border)
            self.writeText(screen, self.input, rect)
            #The enter button
            self.enter.draw(screen)
        elif self.type == "ok":
            self.writeText(screen, self.text, self.Rect)
            self.ok.draw(screen)
        elif self.type == "display":
            self.writeText(screen, self.text, self.Rect)


    def whatPressed(self, x, y):
        if self.type == 'Yes/No':
            if self.yes.pressed(x, y):
                return "Yes"
            elif self.no.pressed(x,y):
                return "No"
            else:
                return None
        elif self.type == 'input':
            if self.enter.pressed(x,y):
                return "enter"
            else:
                return None
        elif self.type == 'ok':
            if self.ok.pressed(x,y):
                return "ok"
            else:
                return None

class TextBox(Button):
    def __init__(self, text, Rect):
        super(TextBox, self).__init__(Rect, text,(255,255,255), border=0)
        self.isTextBox = True
    def updateMe(self):
        x = self.x
        y = self.y
        w, h = self.width, self.height
        self.Rect = (x,y,w,h)

