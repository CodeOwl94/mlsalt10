###
# Extract the expert parameters for all dimensions of all utterances for all streams (mcep is stream 1, this is what we will focus on for now)
###

import pdb
import numpy as np
import os

# Loop over utterances
for i in range(1,10):
    # Loop over dimensions
    for j in range(1,61):
        os.system('./scripts/getexpert.sh -hmmdir models/htk -labdir original/lab -stream 1 -dimension ' + str(j) + ' -outdir experts/utt' + str(i) + '/dim' + str(j) + ' -filename utt' + str(i))

