import pygame
from classes import Button, Note, Page, PopUpBox

def init(self):
    #reset the modes
    self.editing = True
    self.welcome = False
    self.creating = False

    self.popUpup = None

    self.invalidReply = "Please enter a valid %s"

    #buttons
    center = (0, 0, self.width, self.height)
    back = (0, 0, 100, 80)
    oldProjects = Button(center, "Old Projects", (198,226,255), meaning = False)
    backButton = Button(back, "<--", (108,123,139))
    self.buttons = [oldProjects, backButton]
    self.selectedProject = None

def directEditMouse(self, x, y):
    if self.popUpup == None:
        for button in self.buttons:
            if button.pressed(x,y):
                self.init()
        for button in self.projectButtons:
                if button.pressed(x,y):
                    self.selectedProject = findProject(self, button.text)
                    question = "Are you sure you want to edit this project?"
                    self.popUpup = PopUpBox((self.width/2, self.height/2), question, "Yes/No", 'oldProjects')
    else:
        #pop up for selecting the old projects
        if self.popUpup.whatPressed(x, y) == "No":
            self.popUpup = None
            self.selectedProject = None
        elif self.popUpup.whatPressed(x, y) == "Yes":
            self.popUpup = None
            self.cInit(None, project = self.selectedProject)


def findProject(self, title):
    for project in self.oldProjects:
        if project.scoreTitle == title:
            return project







