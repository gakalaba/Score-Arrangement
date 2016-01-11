######
# how to save all the stuff


"""\
Learned how to pickle from, and used examples on, website:
https://docs.python.org/2/library/pickle.html
"""
def saveProject(project):
    import pickle
    allFiles = loadAll()
    if project.project0 in allFiles:
        allFiles.remove(project.project0)
    allFiles.append(project)
    pickled = open('oldProjects.pkl', 'wb')

    # Pickle the objct using the highest protocol.
    for fileName in allFiles:
        pickle.dump(fileName, pickled, -1)

    pickled.close()



def loadProject(project):
    import pickle
    import pprint
    pickled = open('oldProjects.pkl', 'rb')

    while True:
        check = pickle.load(pickled)
        if check == project:
            pickled.close()
            return(check)


def loadAll():
    import pickle
    result = []
    try:
        pickled = open('oldProjects.pkl', 'rb')
    except:
        return result #the file doesnt exist (never saved anything... so return empty list)
    """\
    This ingenius for loop comes from 
    http://stackoverflow.com/questions/15809369/how-to-get-all-pickled-data
    """
    while True:
        try:
            result.append(pickle.load(pickled))
        except:
            break
    return result

