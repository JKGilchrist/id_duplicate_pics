#album.py
import os
import numpy as np
import pickle
import sys

from pic import Pic

class Album:

    def __init__(self, dir):
        self.names = [] #Filepaths of photo files that haven't been fingerprinted
        self.pics = [] #processed photo files (list of Pic objects)
        self.dir = dir
        print("\nBeginning to process pics in order to find duplicates.")
        self.process_pics()
        print("Processing complete. Beginning to search for duplicates.")
        dup_count = self.find_dups()
        if dup_count == 0 :
            print("Search complete. No duplicates were found.")
            if os.path.exists(self.dir + "\duplicate_pics.txt"):
                os.remove(self.dir + "\duplicate_pics.txt")
        else:
            print("Search complete.", dup_count, "duplicate file(s) found. See 'duplicate_pics.txt' for a list of them all, and a Windows file explorer query to open each pair.")


    def process_pics(self):
        #Checks if mini-versions have already been created. 
        if "identify_duplicate_pics.save_data" in os.listdir(self.dir):
            self.names, self.pics = pickle.load(open(self.dir + "\identify_duplicate_pics.save_data", "rb"))
            print("\tUsing saved data ")
        else:
            print("\tNo saved data found")
            self.names = self.get_names(self.dir)[0]
        
        for i in range(len(self.names)): #If there are (any remaining) files that need a mini-version created, go through and do so 
            try:
                y = Pic(self.names[i])
                
                self.pics.append(y)
                if i > 2 and i % 100 == 0: #Saves every-so-often, so if one interrupts programs execution, it can still resume close to where it was and that                
                    print("\tsaving..")
                    pickle.dump( [self.names[i:], self.pics  ] , open(self.dir + "\identify_duplicate_pics.save_data", "wb" ) )
            except:
                print("\tFingerprinting fails for:", self.names[i])
                x = input("Skip " + self.names[i]+ " and continue on [y] or save progress up to this point and quit [n] ? [y/n]")
                if x.lower().strip() == "y":
                    print("\tSkipping", self.names[i], "and continuing on without it")   
                else:
                    print("Saving..")
                    pickle.dump( [self.names[i:], self.pics ] , open(self.dir + "\identify_duplicate_pics.save_data", "wb" ) )
                    sys.exit(1)


        self.names = [] #Once out of for-loop, names is emptied because all have been processed
        
        pickle.dump( [self.names, self.pics  ] , open(self.dir + "\identify_duplicate_pics.save_data", "wb" ) ) #Save all processed pics 

        
    def find_dups(self):
        if os.path.exists(self.dir + "\duplicate_pics.txt"): #Otherwise it will repeat stating what duplicates exist
            os.remove(self.dir + "\duplicate_pics.txt")
        dup_count = 0
        i =  0
        while i < len(self.pics) - 1:
            j = i + 1
            while j < len(self.pics):
                if np.array_equal(self.pics[i].fingerprint, self.pics[j].fingerprint): #duplicates will have the exact same fingerprint
                    if store((self.pics[i].loc, self.pics[j].loc), dup_count, self.dir):
                        dup_count += 1
                j += 1
            i += 1
        os.remove(self.dir + "\identify_duplicate_pics.save_data")
        return dup_count
    
#Retrieve file paths of all pics in current dir and any sub-dirs
    def get_names(self, root_dir):
        dirs, pics, other = split_up(root_dir)

        for dir in dirs:
            add_pics, add_other = self.get_names(dir)
            pics += add_pics
            other += add_other
        
        return pics, other

        

#Splits up a dir into 3 lists, one of sub-dirs, one of jpgs, and one of other ()
def split_up(path):
    lst = os.listdir(path)
    dirs, pics, other = [], [], []
    
    for x in lst:
        try: 
            if len(x) > 4 and (x[-3:].lower() in ["jpg", "peg"]) and os.path.isfile(path + "\\" + x):
                pics.append(path + "\\" + x)
            elif len(x) > 4 and os.path.isfile(path + "\\" + x):
                other.append(path + "\\" + x)
            else:
                dirs.append(path + "\\" + x)
        except:
            other.append(path + "\\" + x) #When in doubt, it goes in other
    return dirs, pics, other


#Saves info on duplicate pics to txt file
def store(tup, dup_count, path):
    if tup[0] == tup[1]:
        return False
    with open(path + '\\duplicate_pics.txt', 'a') as f:
        print("\t", tup)
        if dup_count > 0:
            f.write("\n\n") 
        f.write("Duplicate #" + str(dup_count + 1) + ":\n")
        f.write(tup[0] + "  and  " + tup[1] + "\nFull Windows query:")
        f.write("\n" + "(\"" + tup[0].replace("/", "\\") + "\" AND \"*." + tup[0].split(".")[-1] +  "\")" + " OR " + "(\"" + tup[1].replace("/", "\\") + "\"  \"*." + tup[1].split(".")[-1] +  "\")"  )
        f.write("\nRelative Windows query (much faster to use), from " + path.replace("/", "\\") + " : ")
        f.write("\n" + "(\"" + tup[0].replace("/", "\\")[len(path):] + "\" AND \"*." + tup[0].split(".")[-1] +  "\")" + " OR " + "(\"" + tup[1].replace("/", "\\")[len(path):] + "\"  \"*." + tup[1].split(".")[-1] +  "\")"  )
        
    return True