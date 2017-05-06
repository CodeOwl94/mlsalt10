#!/usr/bin/python

import numpy as np
from scipy.linalg import block_diag

import pdb

# Parse a *.dur.expt file to get the duration means in a matrix
def getDuration(durationFile):
    lines = []
    with open(durationFile, 'r') as f:
        lines = f.read().splitlines()

    # Extract the timing information, discarding the label names
    times = lines[1:len(lines):2]     
    uDur = []
    for time in times:
        timeNumbers = time.split() 
        for i in range(0,5):
            timeNumber = int(round(float(timeNumbers[i])))
            uDur.append(timeNumber)

    #pdb.set_trace()
    uDur = np.asarray(uDur)
    return uDur

# Parse a *.cmp.expt file to get the HMM means and sigmas in matrices
def getHatStats(statsFile):
    lines = []
    with open(statsFile, 'r') as f:
        lines = f.read().splitlines()
    
    # Extract the timing information, discarding the label names
    means  = []
    sigmas = []
    for time in lines: 
        timeNumbers = time.split()
        if(len(timeNumbers)==6):
            meanLabel = []
            sigmaLabel = []
            for i in range(0,3): 
                timeNumber = float(timeNumbers[i])
                meanLabel.append(timeNumber)
            for i in range(3,6): 
                timeNumber = float(timeNumbers[i])
                sigmaLabel.append(timeNumber)
            
            # Append to the overall
            means.append(meanLabel)
            sigmas.append(sigmaLabel)
     
    #pdb.set_trace()            
    return(means,sigmas)

# Convert hat stats to bar stats using uDur
def getBarStats(meansHat, sigmasHat, uDur):
    meansHat = np.asarray(meansHat)
    sigmasHat = np.asarray(sigmasHat)
    #uDur = np.asarray(uDur)
    numberOfFrames = uDur.sum()
    # Create mean bar
    meansBar = np.zeros(numberOfFrames * 3)
    sigmasBar = np.zeros(numberOfFrames * 3) 
    frameCounter = 0
    for i in range(0,len(uDur)):
        for j in range(0,uDur[i]):
            meansBar[frameCounter:frameCounter+3] = meansHat[i]
            sigmasBar[frameCounter:frameCounter+3] = sigmasHat[i]

            frameCounter += 3
   
    # Convert sigmasBar into the matrix form
    sigmasBarMatrix = []
    for i in range(0, len(sigmasBar),3):
        sigmaBarMatrix = np.array([[sigmasBar[i],0,0],[0,sigmasBar[i+1],0],[0,0,sigmasBar[i+2]]])
        sigmasBarMatrix = block_diag(sigmasBarMatrix, sigmaBarMatrix)

    # Remove the dummy row at the top
    sigmasBarMatrix = sigmasBarMatrix[1:,:]
    
    return (meansBar,sigmasBarMatrix)

# Create the W matrix using the window provided with uDur
def createWeightMatrix(uDur):
    wTilda = np.array([[0.0,0.0,1.0,0.0,0.0],[-0.2,-0.1,0.0,0.1,0.2],[0.285714,-0.142857,-0.285714,-0.142857,0.285714]])
    
    numberOfFrames = uDur.sum()

    #weightMatrix = np.zeros([(numberOfFrames*3),(5+numberOfFrames-1)]
    weightMatrix = np.zeros([1,(5+numberOfFrames-1)])   

    frameCounter = 0
    for i in range(0,numberOfFrames):
       preMat = np.zeros([3,i])
       postMat = np.zeros([3,(numberOfFrames-1-i)])
       entry = np.concatenate((preMat,wTilda,postMat),axis=1)         
       weightMatrix = np.concatenate((weightMatrix,entry),axis=0)
    #pdb.set_trace()


   
    # We need to remove two blocks on the end and two blocks on the front to account for not being able to look at frames before and after we those points. wTilda assumes you can look two into the past and two into the future
    weightMatrix = weightMatrix[1:,2:-2]
    
    return weightMatrix

# Create the mean and variance of the trajectory (handout 4, slide 5) using W, meansHat, sigmasHat
def createTrajectory(meansBar, sigmasBarMatrix, weightMatrix):
    sigmasBarInverse = np.linalg.pinv(sigmasBarMatrix)
    #pdb.set_trace()
    firstMultiple = np.dot(np.transpose(weightMatrix),sigmasBarInverse)
    secondMultiple = np.dot(firstMultiple, weightMatrix)
    #pdb.set_trace() 
    sigmasMatrix = np.linalg.pinv(secondMultiple)

    #sigmasCoeff = np.dot(np.dot(sigmasBarMatrix,np.transpose(weightMatrix)),sigmasBarInverse)
    means = sigmasMatrix.dot(weightMatrix.transpose().dot(sigmasBarInverse.dot(meansBar)))
    #means = np.dot(sigmasCoeff,meansBar)
    #pdb.set_trace() 
    return means

if __name__ == "__main__":
    uDur = getDuration('utt1.dur.expt')
    means, sigmas = getHatStats('utt1.cmp.expt')
    meansBar, sigmasMatrix = getBarStats(means,sigmas,uDur)
    weightMatrix = createWeightMatrix(uDur)
    means = createTrajectory(meansBar,sigmasMatrix,weightMatrix)
    #pdb.set_trace() 
    with open('dimension4.txt','w+') as f:
        np.savetxt(f,means)

    with open('meansBar4.txt', 'w+') as f:
        np.savetxt(f,meansBar)

    with open('sigmasMatrixBar4.txt', 'w+') as f:
        np.savetxt(f,sigmasMatrix)
    
    with open('weightMatrix4.txt', 'w+') as f:
        np.savetxt(f, weightMatrix)

    #pdb.set_trace()
