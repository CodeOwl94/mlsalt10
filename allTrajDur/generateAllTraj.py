###
# Extract the expert parameters for all dimensions of all utterances for all streams (mcep is stream 1, this is what we will focus on for now)
###

import pdb
import numpy as np
import os
import subprocess
import sys

import generateTrajNoGV as noGV
import globalVarianceExpert as expertGV
import globalVarianceExpertAlt as expertAltGV
import globalVarianceConstraint as constraintGV

output = subprocess.check_output(['../bin/x2x', '+da', '../models/hts/gv-mcep.pdf'])
gvMeanArray = np.array(output.split()[:60]).astype(float)
gvSigmaArray = np.array(output.split()[60:]).astype(float)
#sigma_inv_v = np.array([1/val for val in sigma_v]) 
utterance = int(sys.argv[1])
# Loop over utterances
for i in range(utterance,utterance+1):
    # Loop over dimensions
    for j in range(50,61):
        #print('Looking at utterance ' + str(i) + ', dimension ' + str(j))
        pathLoc = 'utt'+str(i)+'/dim'+str(j)+'/'

        # Generate the trajectories from the model with GV and also obtain the statistics associated with it 
        uDur = noGV.getDuration('../experts/'+pathLoc+'utt'+str(i)+'.dur.expt')
        meansHat, sigmasHat = noGV.getHatStats('../experts/utt'+str(i)+'/dim'+str(j)+'/utt'+str(i)+'.cmp.expt')
        meansBar, sigmasBarMatrix = noGV.getBarStats(meansHat,sigmasHat,uDur)
        weightMatrix = noGV.createWeightMatrix(uDur)
        means, sigmasMatrix = noGV.createTrajectory(meansBar, sigmasBarMatrix, weightMatrix)
 
        # Save the trajectory generated
        with open('./traj/'+pathLoc+'trajNoGV.txt', 'w+') as f:
            np.savetxt(f,means)
        
        # Extract the GV expert parameters from the PDF
        gvMean = gvMeanArray[j-1]
        gvSigma = gvSigmaArray[j-1]
        
        # Generate the trajectories with GV, using the expert method
        loadedData = expertGV.loadData(means, meansBar,sigmasBarMatrix, weightMatrix, gvMean, gvSigma)
        trajectory = expertGV.gradientAscent(loadedData,0.01,0.1)
        with open('./traj/'+pathLoc+'trajExpertGV.txt','w+') as f:
            np.savetxt(f,trajectory)
       
        # Generate the trajectories with GV, using the expert method with alternative initialization
        loadedData = expertAltGV.loadData(means, meansBar,sigmasBarMatrix, weightMatrix, gvMean, gvSigma)
        trajectory = expertAltGV.gradientAscent(loadedData,0.01,0.1)
        with open('./traj/'+pathLoc+'trajExpertAltGV.txt','w+') as f:
            np.savetxt(f,trajectory)


        # Generate the trajectories with GV, using the constraint method
        loadedData = constraintGV.loadData(means, sigmasMatrix, gvMean, gvSigma) 
        lOpt = constraintGV.optimiseLambda(0.1, loadedData)
        trajectory = constraintGV.calcTrajectory(loadedData, lOpt)
        with open('./traj/'+pathLoc+'trajConstraintGV.txt','w+') as f:
            np.savetxt(f, trajectory)

