###
# Create the directories that will be required for storing the results of the trajectory experiments
# Code taken from http://stackoverflow.com/questions/23793987/python-write-file-to-directory-doesnt-exist
###

import pdb
import os, os.path

# Loop over utterances
for i in range(1,10): 
    # Loop over dimensions
    for j in range(1,61): 
        folderPath = './traj/utt'+str(i)+'/dim'+str(j)+'/'
        try:
            os.makedirs(folderPath)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else: 
                raise 
      
