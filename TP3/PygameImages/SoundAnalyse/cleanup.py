


#create dictionary mapping frequencies to note names
letters = ['C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 
                                                    'G#/Ab', 'A', 'A#/Bb', 'B']
notes = {}
for i in range(40, 84):
    index = i%12
    note = letters[index]
    notes[i] = note
# print(notes)


def getNote(frequency, notes):
    if frequency == None: return 0
    freq = round(frequency)
    note = notes[freq]
    return note

def onlyZeros(L):
    for e in L:
        if e != 0:
            return False
    return True

def ended(L):
    zeros = []
    if not onlyZeros(L):
        for e in reversed(L):
            if e != 0: break
            else: zeros.append(e)
        return len(zeros) > 30
    return False

def removeRepeats(L):
    result = [L[0]]
    for i in range(1, len(L)):
        if L[i] == L[i-1]:
            continue
        else: 
            result.append(L[i])
    realResult = []
    for e in result:
        if e != 0:
            realResult.append(e)
    n = len(realResult)
    for i in range(n):
        L[i] = realResult[i]
    for step in range(len(L) - n):
        L.pop()



# print(removeRepeats([1,1,1,1,1,1,2,2,2,3,3,4,3,4,5,5,5,5,6]))


def removeWrongBreaks(L):
    count = 0
    temp = []
    for i in range(len(L)):
        if (L[i] == 0 and (not (i == len(L)-1))):
            count += 1
        elif L[i] != 0 or (i == len(L)-1):
            if count < 6:
                temp.append(L[i])
            elif count > 0: #valid break, include it
                temp += L[i-count:i+1]
            count = 0
    # print "temp" 
    # print temp
    # print
    n = len(temp)
    for i in range(n):
        L[i] = temp[i]
    for step in range(len(L) - n):
        L.pop()
    # print "modified" 
    # print L
    # print




# pi = [0,0,0,0,0,0,0,0,'B','G','A', 0, 0, 'C', 0,0,'D',0,0,0,0,0,0,0]
# print "pi before", pi
# removeWrongBreaks(pi)
# print "pi after", pi


def testRemoveWrongBreaks():
    print "Testing removeWrongBreaks...",
    tests = []
    A = [0,0,0,0,0,0,0,0,'B','G','A', 0, 0, 'C', 0,0,'D',0,0,0,0,0,0,0]
    removeWrongBreaks(A)
    B = [0,0,0,0,0,0,0,0,0,'B',0,'B',0,'B',0,'B',0,0,0,0,0,0,0,0]
    removeWrongBreaks(B)
    C = [0,0,0,0,0,0,0,0,'B','B',0,0,0,'B','B',0,0,0,0,0,0,0,'C','C',0,'C',
                                            0,0,0,0,0,0,0]
    removeWrongBreaks(C)
    assert(A == [0,0,0,0,0,0,0,0,'B','G','A','C','D',0,0,0,0,0,0,0])
    assert(B == [0,0,0,0,0,0,0,0,0,'B','B','B','B',0,0,0,0,0,0,0,0])
    assert(C == [0,0,0,0,0,0,0,0,'B','B','B','B',0,0,0,0,0,0,0,'C','C','C',
                                                            0,0,0,0,0,0,0])
    print "Passed!"
# testRemoveWrongBreaks()
# print
# print
# print

# H = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'B', 'B', 'B', 'B', 
# 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'C', 'C', 'C', 'C', 
# 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 
# 'C', 'C', 'C', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'C#/Db', 'C#/Db', 'C#/Db', 
# 'C#/Db', 'C#/Db', 'C#/Db', 'C#/Db', 'C#/Db', 'D', 'D', 'D', 'D', 'D', 'D', 
# 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 0, 0, 0, 0, 0, 0, 
# 0, 0, 'B', 'B', 'B', 'B', 'C', 'C', 'C', 'C', 0, 0, 0, 0, 0, 0, 0, 0, 0, 'E', 
# 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E',
#  'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 
#  'E', 'E', 'E', 'E', 'E', 'E', 'E']

def getCounts(L):
    counts = {}
    for e in L:
        if not e in counts:
            counts[e] = 1
        else:
            counts[e] += 1
    return counts

# print(getCounts(H))



def removeSlides(L):
    indices = [-1]
    for i in range(1, len(L)):
        if L[i] == 0 and L[i-1] != 0:
            indices.append(i-1) #end of target note
    temp = []
    for i in range(1, len(indices)):
        index = indices[i]
        targetNote = L[index]
        inMistake = False
        count = 0
        for j in range(index, -1, -1):
            if not inMistake:
                if L[j] != targetNote:
                    shift = j
                    inMistake = True
            elif inMistake:
                if L[j] == 0:
                    prevIndex = indices[i-1]
                    temp += L[prevIndex + 1: shift-count]
                    temp += L[shift+1:index+1]
                    break
                else: 
                    count += 1

    lastIndex = indices[-1]
    temp += L[lastIndex+1:] #add back in trailing zeros
    n = len(temp)
    for i in range(n):
        L[i] = temp[i]
    for step in range(len(L) - n):
        L.pop()






# print
# print
# print

# har = [0,0,0,'A','A','B','B','B','B',0,0,0,0,'C','C','C','C','C','C','D',0,0,0,0,0, 'G','G','F',0,0,0,0]
# print "beofre:  ", har
# removeSlides(har)
# print "after:   ", har

def testRemoveSlides():
    print "Testing removeSlides...", 
    tests = []
    A = [0,0,0,0,'A','A','A','B','B','B','B','B','B',0,0,0]
    B = [0,'A','B','C','B','A','A',0]
    C = [0,0,0,'B','B','B','C','C','C','C','C',0,0]
    D = [0,0,'B','C','C',0,0,'D','D','E','E','E',0,0,0,'F','G','G','B',0,0]
    tests.append(A)
    tests.append(B)
    tests.append(C)
    tests.append(D)
    for test in tests:
        removeSlides(test)
    assert(A == [0,0,0,0,'B','B','B','B','B','B',0,0,0])
    assert(B == [0,'A','A',0])
    assert(C == [0,0,0,'C','C','C','C','C',0,0])
    assert(D == [0,0,'C','C',0,0,'E','E','E',0,0,0,'B',0,0])
    print "Passed!"
# testRemoveSlides()


def removeSingles(L):
    temp = [L[0]]
    for i in range(1, len(L)-1):
        if L[i] != 0 and L[i-1] == 0 and L[i+1] == 0:
            continue
        else:
            temp.append(L[i])
    temp.append(L[-1])
    n = len(temp)
    for i in range(n):
        L[i] = temp[i]
    for step in range(len(L) - n):
        L.pop()

def testRemoveSingles():
    print "Testing removeSinlges...",
    A = [0,0,0,'A',0,0,0]
    removeSingles(A)
    B = [0,0,0,'C','C','C','C','C',0,0,0,0,0,0,'C',0,0,0]
    removeSingles(B)
    C = [0,0,'B','B','B',0,0,0,'B',0,0,'C','C','C',0,0,0,]
    removeSingles(C)
    assert(A == [0,0,0,0,0,0])
    assert(B == [0,0,0,'C','C','C','C','C',0,0,0,0,0,0,0,0,0])
    assert(C == [0,0,'B','B','B',0,0,0,0,0,'C','C','C',0,0,0,])
    print "Passed"
# testRemoveSingles()

def cleanUp(L):
    #first take raw data and remove improper streaming errors/breaks
    removeWrongBreaks(L)
    #next, remove any slides that were picked up from inaccurate singing
    removeSlides(L)
    #Get rid of weird ones that came up once - known for sure to be wrong
    removeSingles(L)
    #finally, string together the readings as occurances of notes
    # removeRepeats(L)



def testCleanUp():
    print "Testing cleanUp...",
    A = [0,0,0,0,0,0,0,'C#/Db','C#/Db','C#/Db','C#/Db','C','C','C','C',
                                                            0,0,0,0,0,0,0,0]
    cleanUp(A)
    B = [0,0,0,0,0,0,'A','A','A',0,0,'C#/Db','C#/Db','C#/Db','C#/Db','C#/Db',
    'C#/Db',0,0,0,0,'C#/Db','C#/Db','C#/Db',0,'C#/Db',0,0,0,0,0,0,0,'B','B',
                                        'B','B','B',0,'B',0,0,0,0,0,0,0,0,0]
    cleanUp(B)
    C = [0,0,0,0,0,0,0,0,'C#/Db','C#/Db','C#/Db','C#/Db','D','D','D',0,0,
    'D#/Eb','D#/Eb','D#/Eb','D#/Eb','D#/Eb',0,'D#/Eb',0,'D#/Eb',0,0,0,0,0,
                                                                    0,0,0,0]
    cleanUp(C)
    assert(A == ['C'])
    assert(B == ['C#/Db','B'])
    assert(C == ['D#/Eb'])
    print "Passed!"
# print
# print
# testCleanUp()








