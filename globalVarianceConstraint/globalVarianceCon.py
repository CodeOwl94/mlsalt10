#!/usr/bin/python

import numpy as np
from scipy.optimize import fmin
import pdb
from numpy.linalg import pinv as inv 

def staticParameters(dimension):
    statics = {}
    with open('dimensionSigma'+dimension+'.txt', 'r') as f:
        sigma = np.loadtxt(f)
        statics['P'] =inv(sigma)
    with open('dimensionMean'+dimension+'.txt', 'r') as f:
        mean = np.loadtxt(f)

        statics['b'] = mean.T.dot(statics['P']).T

    statics['T'] = statics['b'].shape[0]
    #statics['J'] = np.identity(statics['T']) - (1.0/statics['T'])*np.ones(statics['T']).dot(np.ones(statics['T']))
    statics['J'] = np.eye(statics['T']) - (1.0/statics['T'])*np.ones((statics['T'],statics['T']))
    statics['omega'] = 1.0/(3*statics['T'])
    
    #TODO: Load this in from the file
    statics['gvMean'] = 0.169537
    statics['gvSigma'] = 0.00293601
     
    return statics     

def calcParameters(statics,lOpt):
    l = lOpt
    c = inv((statics['P'] - l*statics['J'])).dot(statics['b'])
    
    return c

def globalVarianceLik(l,P,b,omega,gvSigma,gvMean,J): 
    
    c = inv(P - l*J).dot(b)
    
    gvLik = -0.5*c.T.dot(P).dot(c) + b.T.dot(c) - ((1.0/omega)/(2.0*gvSigma))*np.power((c.var()-gvMean),2)     
     
    # The optimisation function minimizes so we make it negative. Minimizing negative log likelihood is the same as maximising log likelihood
    return -gvLik

def optimiseLambda(lInit,statics):
    l = np.array([lInit])

    lOpt = fmin(globalVarianceLik, l, args=(statics['P'],statics['b'],statics['omega'],statics['gvSigma'],statics['gvMean'], statics['J']))
    print(lOpt) 
    return lOpt

if __name__ == "__main__":
    
    # Load in static data
    statics = staticParameters('4')

    # Obtain optimal lambda
    lOpt = optimiseLambda(0.5,statics)

    # Obtain trajectory given optimal lambda
    trajectory = calcParameters(statics, lOpt)

    print(trajectory.var())
    # Final trajectory should be 0.16 
    with open('gvRes.txt', 'w+') as f:
        np.savetxt(f, trajectory)

   
