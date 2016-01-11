
import wave
import numpy
import math
import pyaudio
import analyse
import copy
import cleanup
import time

def onBeat(start):
    diff = time.time() - start
    tens = (diff*10)//1
    return tens%10 == 0

def inputSound():
    # Initialize PyAudio
    pyaud = pyaudio.PyAudio()
    
    # Open input stream, 16-bit mono at 44100 Hz
    # On my system, device 2 is a USB microphone, your number may differ.
    stream = pyaud.open(
        format = pyaudio.paInt16,
        channels = 1,
        rate = 44100,
        input_device_index = 1,
        input = True)
    times = []
    end = []
    notes = cleanup.notes
    notesSung = [] #so that there is an established pause in any beginning
    print "*listening*"
    start = time.time()
    fun = []
    while cleanup.silentEnd(notesSung):
        times.append(time.time()-start)
        fun.append("*")
        # Read raw microphone data
        rawsamps = stream.read(1024)
        # print(type(rawsamps), rawsamps)
        # Convert raw data to NumPy array
        samps = numpy.fromstring(rawsamps, dtype=numpy.int16)
        # print(type(samps), samps)
        # Show the volume and pitch
        # analyse.loudness(samps), analyse.musical_detect_pitch(samps)
        freq = analyse.musical_detect_pitch(samps)
        notesSung.append(cleanup.getNote(freq, notes))
        # print cleanup.getNote(freq, notes)
    print "*Done*"
    print times
    leng = len(notesSung)
    cleanup.cleanUp(notesSung)
    print notesSung
    print len(times), leng, len(notesSung), len(fun)
    print
    print
    cleanup.removeRepeats(notesSung)
    print notesSung




    # print "                                                     CHECK"
    # print
    # print "                                                     original" 
    # print notesSung
    # cleanup.removeWrongBreaks(notesSung)
    # print "                                                     getcounts"
    # print cleanup.getCounts(notesSung)
    # print
    # print "                                                 removed improper breaks" 
    # print notesSung
    # print
    # print "                                                 Removed improper slides"
    # cleanup.removeSlides(notesSung)
    # print
    # print notesSung
    # print "                                                     remove repeats/FINAL"
    # print cleanup.removeRepeats(notesSung)

print "                                          Please sing clearly and loudly into the microphone"
print "                                                   Sing only on the syllable 'Bah'"
print "                                                      Sing at a speed of 80 bpm"
print "                                              When you are ready, press the space bar to begin"
print "                                       **But record one full silent/empty measure before beginning**"
inputSound()

# print(analyse.musical_detect_pitch("E.wav"))

###############################################
#totipotent sygote (all capable of both paths below)
#1. inner cell mass - multiple/pluri potent
#2. trophoblast --> placenta

