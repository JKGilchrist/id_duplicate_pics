#pic.py
import matplotlib.pyplot as plt
import numpy as np
import os


#Creates mini-versions of a picture file in order to more quickly compare them (In exchange for a slight decrease in accuracy)
class Pic:
    def __init__(self, loc):
        self.loc = loc
        self.name = loc.split("\\")[-1]
        
        self.fingerprint = self.create_fingerprint()
        
    def create_fingerprint(self):
        print("\tmaking print of", self.loc)

        x = plt.imread(self.loc)
        full_fingerprint = np.array(plt.imread(self.loc), dtype = np.uint8)
        fingerprint = []
        for x in range(0, len(full_fingerprint), 10):
            for y in range(0, len(full_fingerprint[0]), 10):
                fingerprint.append(full_fingerprint[x][y])
        fingerprint = np.array(fingerprint)
        return fingerprint
        


