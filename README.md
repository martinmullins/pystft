STFT
--------------

## mplstft.py: MatPlotLib STFT
* Use matplotlib to plot the stft for a wav file.

### Modifications
* TODO must use a short wav file < 3 seconds

## pygamestft.py PyGame Live STFT
Liked the idea using pygame with the scipy fft mentioned on [this blog](https://www.swharden.com/wp/2010-06-19-simple-python-spectrograph-with-pygame/)
Used that source at the starting point.

### Modifications
* ADDED windowing function
* TODO cleaned up some code
* TODO Best buffer
* TODO FFT normalization
* TODO command line arguments:
    * TODO sample frequency
    * TODO window size
    * TODO skip size
    * TODO windowing function

