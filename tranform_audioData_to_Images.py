import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from os import listdir
from os.path import isfile, join

mypath=r"C:\...\data\spoken_numbers_pcm\spoken_numbers_pcm\16bit" #audio dataset path directory
cntr=0
flx = [f for f in listdir(mypath) if isfile(join(mypath, f))]
FileList = [] #list of files' names , it servs as an output laber later
for cnt in range (len(flx)): #reducing the amount data for faster processing during tests
    if (('100' in flx[cnt])or('180' in flx[cnt])or('260' in flx[cnt])or('340' in flx[cnt])):
        FileList.append(flx[cnt])


fileNameandLocx=r"C:\Users\...\data\spoken_numbers_pcm\spoken_numbers_pcm\16bit\\"
fileImgLoc=r"C:\...\data\spoken_numbers_pcm\16bimg\\"

for ccnt in range(len(FileList)):
    fileNameandLocxx=mypath + FileList[ccnt]
    spf = wave.open(fileNameandLocxx,'r')  # ('wavfile.wav','r')
    # Extract Raw Audio from Wav File
    signal = spf.readframes(-1)
    signal = np.fromstring(signal, 'Int16')
    fs = spf.getframerate()

    # If Stereo
    if spf.getnchannels() == 2:
        print('Just mono files')
        sys.exit(0)

    Time = np.linspace(0, len(signal) / fs, num=len(signal))

    chunkL = int((fs / 100) * 2)  # 160 = 10 ms
    Nchun10s = round(len(signal) / chunkL)  # math.ceil
    chun10s = np.zeros((Nchun10s + 1, chunkL))
    if (Nchun10s>(len(signal) / chunkL)):
        Nchun10s=Nchun10s-1
        print('Bing Bango')

    for cnt in range(Nchun10s):
        print(Nchun10s,(len(signal) / chunkL))
        for cntr in range(chunkL):
            chun10s[cnt, cntr] = signal[(chunkL * cnt) + cntr]
            #print(cnt, cntr, chun10s[cnt, cntr])
    for cnt in range(len(signal) - chunkL * Nchun10s):
        chun10s[Nchun10s, cnt] = signal[(chunkL * Nchun10s) + cnt]

    fig = plt.figure(12) #12 means nothing I just wanted to use the same fi to fix the memory loss, which probably fixed by the 3 lines after saving the .png
    powerSpectrum, freqenciesFound, timex, imageAxis = plt.specgram(signal, Fs=fs)

    ax = fig.gca()
    ax.axis('off')
    fileNameLocImg = fileImgLoc + FileList[ccnt]+'.png'
    fig.savefig(fileNameLocImg)
    plt.close(fig)
    plt.clf()
    plt.cla()
