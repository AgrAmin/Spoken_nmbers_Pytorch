import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
import torch
#import math

fileNameandLoc= r'''C:\...\data\LDC93S1.wav''';
spf = wave.open(fileNameandLoc)#('wavfile.wav','r')

#Extract Raw Audio from Wav File
signal = spf.readframes(-1)
signal = np.fromstring(signal, 'Int16')
fs = spf.getframerate()

#If Stereo
if spf.getnchannels() == 2:
    print('Just mono files')
    sys.exit(0)


Time=np.linspace(0, len(signal)/fs, num=len(signal))


plt.figure(0)
plt.title('Signal Wave...')
plt.plot(Time,signal)
plt.show()


print(len(signal)/fs)
print(fs)
print(type(signal))

chunkL= 160*2 # 160 = 10 ms

Nchun10s=round(len(signal)/chunkL) #math.ceil
chun10s= np.zeros((Nchun10s+1, chunkL))
#print((chun10s.size()))
for cnt in range(Nchun10s):
    for cntr in range (chunkL):
        chun10s[cnt, cntr] = signal[(160*cnt)+cntr]
        print(cnt,cntr,chun10s[cnt, cntr])
print(Nchun10s, chunkL*Nchun10s)
print(signal[chunkL*Nchun10s-1])
print(chun10s[Nchun10s-1,chunkL-1])
for cnt in range(len(signal)-chunkL*Nchun10s):
    chun10s[Nchun10s,cnt]=signal[(chunkL*Nchun10s)+cnt]

uptoyou=3 #number of figures : 8 chnks/figure

for cntr in range(uptoyou):
    plt.figure(cntr+1)
    for cnt in range(8):
        sig = chun10s[cnt, :]
        plt.subplot(4, 2, cnt + 1)
        # plt.title('Signal Wave %d', cnt)
        Time = np.linspace(0, len(sig) / fs, num=len(sig))
        plt.plot(Time, sig)

plt.show()

plt.figure(uptoyou)
sig = chun10s[146, :]
powerSpectrum, freqenciesFound, timex, imageAxis = plt.specgram(signal, Fs=fs)
plt.show()
