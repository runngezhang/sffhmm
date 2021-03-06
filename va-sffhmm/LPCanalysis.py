"""LPC analysis functions

2013 Jean-Louis Durrieu
durrieu.ch
"""

import numpy as np
import scikits.talkbox as tb
import scipy.signal # for lfilter

def stlpc(longSignal,
          order=10,
          windowLength=1024,
          hopsize=512,
          samplingrate=16000,
          axis=-1):
    """Compute 'Short Term LPC':
          Cut the input signal in frames
          Compute the LPC on each of the frames (through talkbox)
    
    """
    fs = samplingrate
    # adding zeros to have the first frame centered on 0:
    data = np.concatenate((np.zeros(windowLength/2),
                           longSignal))
    lengthSignal = data.size
    # number of windows, and resizing the data,
    # in accordance with stft from sffhmm.py:
    nbWindows = np.ceil((lengthSignal - windowLength) /
                        (np.double(hopsize)) + 1.0) + 1
    newLengthSignal = (nbWindows - 1) * hopsize + windowLength
    data = np.concatenate([data,
                           np.zeros([newLengthSignal - lengthSignal])])
    
    currentWindow = np.zeros([windowLength,])
    
    # number of coefficients for the LPC decomposition is `order+1`
    STLpc = np.ones([order + 1, nbWindows])
    # number of corresponding formants is
    #    `floor((order-1)/2)
    # indeed, if `order` is odd, then it's `(order-1)/2`, that is to say all
    # poles, except the isolated one (which is real)
    # if `order` is even, then it's equal to `(order-2)/2`,
    #
    # 20130514 wait, why is it not order/2 again?
    nbFormants = int(order / 2)
    rootLpc = np.zeros([order, nbWindows], dtype=np.complex)
    freqLpc = np.ones([nbFormants, nbWindows])
    # specFromLpc = np.zeros([windowLength / 2.0 + 1, nbWindows])
    sigmaS = np.zeros([nbWindows, ])
    
    # pre-processing the data, amplifying high frequencies:
    b_preamp=np.array([1.0,-0.99])
    a_preamp=np.array([1.0])
    longSignalPreamp = scipy.signal.lfilter(b_preamp,a_preamp,data)
    
    for n in np.arange(nbWindows):
        # getting the desired frame
        beginFrame = n * hopsize
        endFrame = np.minimum(n * hopsize + windowLength, lengthSignal)
        currentWindow[:endFrame-beginFrame] = longSignalPreamp[beginFrame:
                                                               endFrame]
        # windowing the frame
        currentWindow *= np.hamming(windowLength)
        # computing the LPC coefficients
        STLpc[:,n], sigmaS[n], _ = tb.lpc(currentWindow, order)
        # compute the corresponding spectrum - not necessary here
        # specFromLpc[:,n] = lpc2spec(STLpc[:,n], sigmaS[n], fs, windowLength)
        
        # compute the roots of the polynomial:
        rootLpc[:,n] = np.roots(STLpc[:,n])
        # convert to frequencies
        freqLpcTmp = np.angle(rootLpc[:,n]) / (2.0 * np.pi) * fs
        freqLpcTmp = freqLpcTmp[freqLpcTmp>0.0]
        freqLpcTmp.sort()
        nbMinPositiveRoots = freqLpcTmp[0:nbFormants].size
        freqLpc[0:nbMinPositiveRoots,n] = freqLpcTmp[0:nbFormants]
        
    return STLpc, rootLpc, freqLpc, sigmaS #, specFromLpc, 

def lpc2spec(lpc, sigma, fs, nfft):
    """Converts the LPC coefficients into a spectrogram like matrix.
    """
    orderPlus1 = lpc.size
    matExp = np.exp(- 1j * np.outer(2 * np.pi * \
                                    np.arange(nfft / 2.0 + 1) / \
                                    np.double(nfft),
                                    np.arange(orderPlus1, dtype=np.double)))
    return sigma / np.abs(np.dot(matExp, lpc)) 

