import scipy
import sys
import numpy as np
import scipy.io.wavfile
import matplotlib.pyplot as plt

FREQ_LIMIT = 8000
FFT_SIZE = 2048
FFT_SHIFT = 256

def stft(x, fs, N, H):
	w = scipy.hanning(N+1)[1:]
	X = scipy.array([scipy.fft(w*x[i:i+N])
				for i in range(0, len(x)-N, H)])

	return X


def parseWav(fname):
    """ Returns ( sample freq, samples array ) """
    return scipy.io.wavfile.read(sys.argv[1])

def findLimit(fs,N):
    """ Determine the top bin for STFT """
    return int(FREQ_LIMIT/(fs/float(N))) #python 2.7 div

def usage():
    print >> sys.stderr, "Usage:",sys.argv[0],"<wav file>"

def main():
    try:
        fn = sys.argv[1]
    except IndexError, e:
        usage()
        return 2


    fs, samps = parseWav(fn)
    stftData = stft(samps,fs,FFT_SIZE,FFT_SHIFT)
    topBin = findLimit(fs,FFT_SIZE)
    print stftData.shape

    stftData = np.delete(stftData,np.s_[topBin:],1)
    stftData = np.absolute(stftData)

    plt.imshow(np.transpose(stftData),
            origin='lower'
            )
    plt.show()

    return 0

if __name__=='__main__':
    sys.exit(main())
