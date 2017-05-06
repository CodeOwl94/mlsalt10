#!/usr/bin/python

import numpy as np

import pdb

def loadData(initial, mean, sigma, weights, gvMean, gvSigma ):
    #initial = []
    #mean = []
    #sigma = []
    #weights = []

    #with open('dimension'+dimension+'.txt', 'r') as f:
    #    initial = np.loadtxt(f)
    #with open('meansBar'+dimension+'.txt', 'r') as f:
    #    mean = np.loadtxt(f)
    #with open('sigmasMatrixBar'+dimension+'.txt', 'r') as f:
    #    sigma = np.loadtxt(f)
    #with open('weightMatrix'+dimension+'.txt', 'r') as f:
    #    weights = np.loadtxt(f)
    #pdb.set_trace()
    
    sigmaInv = np.linalg.pinv(sigma)
 
    wSquareTerm = weights.transpose().dot(sigmaInv.dot(weights))
    meanTerm = weights.transpose().dot(sigmaInv.dot(mean))

    numberOfFrames = initial.shape[0]
    #TODO: Load in the next two values instead of hard coding it! 
    #gvMean = 0.169537
    #gvSigma = 0.00293601

    loadedData = {'initial':initial, 'wSquareTerm':wSquareTerm, 'meanTerm':meanTerm, 'omega':1.0/(3.0*numberOfFrames), 'gvMean':gvMean, 'gvSigmaInv':1.0/gvSigma, 'frames':numberOfFrames}
    return loadedData

def getGradient(loadedData, trajectory):
    trajectoryMean = trajectory.mean()
    
    #trajectoryScaled = np.zeros([loadedData['frames'],1])
    #pdb.set_trace()
    #for i in range(0, loadedData['frames']):
    trajectoryScaled = trajectory - trajectoryMean

    trajectoryVar = trajectory.var()

    vDash = (-2.0/loadedData['frames']) * (trajectoryScaled) * loadedData['gvSigmaInv'] * (trajectoryVar-loadedData['gvMean'])
    gradient = loadedData['omega'] * (-loadedData['wSquareTerm'].dot(trajectory) + loadedData['meanTerm']) + vDash 
    
    return gradient

def gradientAscent(loadedData, learningRate, stoppingCrit):
    trajectory = loadedData['initial']

    gradientNorm = 1
    while(gradientNorm>stoppingCrit):
        gradient = getGradient(loadedData,trajectory)
        trajectory = trajectory + learningRate*gradient
        
        gradientNorm = np.linalg.norm(gradient)

    return trajectory


if __name__ == "__main__":
    loadedData = loadData('4') 
    trajectory = gradientAscent(loadedData,0.01, 0.1)
    with open('gvRes.txt', 'w+') as f:
        np.savetxt(f, trajectory)

    #pdb.set_trace()
