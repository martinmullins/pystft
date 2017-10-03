import pygame
import numpy
import threading
import pyaudio
import scipy
import scipy.fftpack
import scipy.io.wavfile
import numpy as np
import wave
import sys

#TODO make these configurable from the command line
rate=12000 
soundcard=3
windowWidth=500
fftsize=512
scooter=[]
overlap=4 
window = scipy.hanning(fftsize+1)[1:]

#TODO stftbuf is thread safe?
def record(args):
    TODO = args 
    global stftbuf

    p = pyaudio.PyAudio()
    inStream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=rate,
                        input=True)

    buff = numpy.zeros(fftsize,dtype=numpy.int16)#TODO circular buffer, what is fast?
    while True:
        shift = fftsize/overlap
        buff = numpy.append(buff[shift:],
                numpy.fromstring(inStream.read(shift), dtype=numpy.int16))

        fft = scipy.fft(window*buff)
        # TODO fft normalization
        fft = np.abs(fft[:fftsize/2])/fftsize * 0.5

        stftbuf=numpy.roll(stftbuf,-1,0)
        stftbuf[-1]=fft[::-1]

def main():
    global stftbuf

    pygame.init()
    pygame.display.set_caption("PYSTFT")
    screen=pygame.display.set_mode((windowWidth,fftsize/2))

    world=pygame.Surface((windowWidth,fftsize/2),depth=8)
    # TODO make pallette configurable
    pal = [(max((x-128)*2,0),x,min(x*2,255)) for x in xrange(256)]
    world.set_palette(pal)

    stftbuf=numpy.array(numpy.zeros((windowWidth,fftsize/2)),dtype=int)

    t_rec=threading.Thread(target=record,args=(stftbuf,))
    t_rec.daemon=True 
    t_rec.start() 
    clk=pygame.time.Clock()

    # main "game" loop
    while True:
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.surfarray.blit_array(world,stftbuf) 
        screen.blit(world, (0,0))
        pygame.display.flip() 
        clk.tick(30) #limit to 30FPS

    return 0

if __name__=='__main__':
    sys.exit(main())

