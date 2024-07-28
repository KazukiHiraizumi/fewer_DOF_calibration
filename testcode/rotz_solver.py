#!/usr/bin/python

import numpy as np
import tflib
import copy
from scipy import optimize
from scipy.spatial.transform import Rotation as Rot
import itertools

loop=0

def dot_each(As,Bs):
  return np.array(list(map(lambda x: x[0].dot(x[1]),zip(As,Bs))))

def fit_func(prm,bTg_i,cTt_i,bTg_j,cTt_j):
  gTc=np.eye(4)
  gTc[:3,:3]=Rot.from_rotvec(prm[1:4]).as_matrix()
  gTc[1,3]=prm[0]
  bTt_i=dot_each(bTg_i.dot(gTc),cTt_i)
  bTt_j=dot_each(bTg_j.dot(gTc),cTt_j)
  tdiff=bTt_i[:,:3,3]-bTt_j[:,:3,3]
  rdiff=Rot.from_matrix(bTt_i[:,:3,:3]).as_rotvec()-Rot.from_matrix(bTt_j[:,:3,:3]).as_rotvec()
  terr=np.linalg.norm(tdiff,axis=1)  #translation error
  rerr=np.linalg.norm(rdiff,axis=1)  #rotation(rotvec) error
  return terr*rerr

def error(gTc,bTg_s,cTt_s):
  bTt=dot_each(bTg_s.dot(gTc),cTt_s)
  bT=bTt[:,:3,3]
  bR=[Rot.from_matrix(x).as_rotvec() for x in bTt[:,:3,:3]]
  tcen=np.mean(bT,axis=0).reshape((1,3))
  terr=np.linalg.norm(bT-tcen,axis=1)
  rcen=np.mean(bR,axis=0).reshape((1,3))
  rerr=np.linalg.norm(bR-rcen,axis=1)
  return np.max(terr),np.max(rerr)

def solve(bTg_s,cTt_s,ttol=10,rtol=0.1,retry=30):
  global loop
  combi=np.array(list(itertools.combinations(np.arange(len(bTg_s)),2))).T
  dat=(bTg_s[combi[0]],cTt_s[combi[0]],bTg_s[combi[1]],cTt_s[combi[1]])
  sol=np.random.uniform(-1.5,1.5,4)
  sol[0]=np.random.rand()*1000
  sol,cov=optimize.leastsq(
    fit_func,
    sol,
    args=dat)
#    maxfev=10000,ftol=0.0001)
  if cov is None:
    print("rcalib_solver::scipy::optimize failed")
    return None
  RT=np.eye(4)
  RT[:3,:3]=Rot.from_rotvec(sol[1:4]).as_matrix()
  RT[1,3]=sol[0]
  terr,rerr=error(RT,bTg_s,cTt_s)
  print("error",terr,rerr)
  if sol[0]>0 and terr<ttol and rerr<rtol:
    loop=0
    return RT
  else:
    loop=loop+1
    if loop<retry: return solve(bTg_s,cTt_s,ttol,rtol,retry)
    else: return None

