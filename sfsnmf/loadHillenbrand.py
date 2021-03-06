"""loadHillenbrand.py

Loads some pieces of information about the files from the
Hillenbrand dataset, available online at the address:
    http://homepages.wmich.edu/~hillenbr/voweldata.html

2013 Jean-Louis Durrieu, LTS5, EPFL

"""

import numpy as np
import scipy as sp
import scipy.io.wavfile as wav
import os.path

#########
# PATHS #
#########
"""
Modify these paths and filenames in order to fit those of your system.

In particular, one have to set the `timedataf` and `bigdataf` variables,
which contain the filename and complete path to, resp., the `timedata.dat`
and `bigdata.dat` files.

The path the the root of the database has to be given in `prefixBDD`.
"""
if os.path.isdir('/Users/jeanlouis/work/BDD/'):
    timedataf = '/Users/jeanlouis/work/BDD/hillenbrand/vowels/timedata.dat'
    bigdataf = '/Users/jeanlouis/work/BDD/hillenbrand/vowels/bigdata.dat'
    prefixBDD = '/Users/jeanlouis/work/BDD/hillenbrand/vowels/'
elif os.path.isdir('/home/durrieu/work/BDD/'):
    timedataf = '/home/durrieu/work/BDD/hillenbrand/vowels/timedata.dat'
    bigdataf = '/home/durrieu/work/BDD/hillenbrand/vowels/bigdata.dat'
    prefixBDD = '/home/durrieu/work/BDD/hillenbrand/vowels/'
else:
    raise ImportError('Jean-Louis, you are working somewhere unusual...')

###########
# PARSING #
###########

# parsing the metadata files:
timedat = np.loadtxt(timedataf, skiprows=6, usecols=(1,2,3,4))
timedatnames = np.loadtxt(timedataf, skiprows=6, usecols=(0,),
                          dtype=np.str)

timedatlabels = {'start':0, 'end':1,
                 'center1':2, 'center2':3}

bigdat = np.loadtxt(bigdataf, skiprows=43, usecols=range(1,30))
bigdatnames = np.loadtxt(bigdataf, skiprows=43, usecols=range(0,1),
                         dtype=np.str)

bigdatlabels = {'duration':0, 'F0':1, 'F1':2, 'F2':3, 'F3':4,
                'F1_10':5, 'F2_10':6, 'F3_10':7,
                'F1_20':8, 'F2_20':9, 'F3_20':10,
                'F1_30':11, 'F2_30':12, 'F3_30':13,
                'F1_40':14, 'F2_40':15, 'F3_40':16,
                'F1_50':17, 'F2_50':18, 'F3_50':19,
                'F1_60':20, 'F2_60':21, 'F3_60':22,
                'F1_70':23, 'F2_70':24, 'F3_70':25,
                'F1_80':26, 'F2_80':27, 'F3_80':28,
                }

# some statistics on the data:
meansFormants = {}
mediansFormants = {}
stdFormants = {}
for n in range(3):
    rangeInBigDat = 5 + n + 3*np.arange(8)
    mediansFormants[n] = np.median(bigdat[:,rangeInBigDat])
    meansFormants[n] = bigdat[:,rangeInBigDat].mean()
    stdFormants[n] = bigdat[:,rangeInBigDat].std()

#############
# Functions #
#############

def loadHill(filename, folder=prefixBDD):
    """Loads an audio wavfile, guessing the correct complete path
    from the filename and the provided root folder. 
    """
    if filename[0] == 'm':
        subpath = '/men/'
    elif filename[0] == 'w':
        subpath = '/women/'
    elif filename[0] == 'b' or filename[0] == 'g':
        subpath = '/kids/'
    filenameFull = str('').join([folder, subpath, filename, '.wav'])
    
    return wav.read(filenameFull)

def displayHistograms(bins=100):
    """draws a histogram, giving the distribution of formant values within
    the Hillenbrand dataset.
    """
    import matplotlib.pyplot as plt
    plt.figure()
    for n in range(3):
        plt.hist(bigdat[:, 5+n+np.arange(8)*3].flatten(),
                 histtype='step', bins=bins)

