import sys
import csv
import numpy as np
import scipy.io.wavfile as scw
import pdb
import matplotlib.pyplot as plt

if __name__ == '__main__':
    pdb.set_trace()
    SRC_NAME = sys.argv[1]
    FPS = int(sys.argv[2])
    RATE, Data = scw.read(SRC_NAME)
    Data = np.mean(Data, axis=1)
    FRAME_SIZE = int(RATE / FPS)
    REST = Data.shape[0] % FRAME_SIZE
    Data = Data[:-REST]
    Data = np.absolute(Data)
    FRAME_NUM = Data.shape[0] / FRAME_SIZE
    Data = np.split(Data, FRAME_NUM)
    Data = np.array([(np.mean(x), 0) for x in Data])
    #Data_diff = Data[1:] - Data[:-1]
    with open(input(), 'w') as f:
        writer = csv.writer(f)
        writer.writerows(list(Data))
    