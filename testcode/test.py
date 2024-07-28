#!/usr/bin/python

import numpy as np
import tflib
import rotz_solver as solver
from scipy.spatial.transform import Rotation as Rot

#Ground truth
gTc=np.eye(4)
gTc[:3,:3]=Rot.from_euler('X',135,degrees=True).as_matrix()
gTc[:3,3]=np.array([0,500,0],dtype=float)
cTg=np.linalg.inv(gTc)
print("Truth",tflib.fromRTtoVec(gTc))

#Target
bTt=np.eye(4)
bTt[:3,3]=np.array([50,0,0],dtype=float)

qlist=[-90,-45,0,45,90]

bTg_s=[]
cTt_s=[]
for q in qlist:
  bTg=np.eye(4)
  bTg[:3,:3]=Rot.from_euler('Z',q,degrees=True).as_matrix()
  gTb=np.linalg.inv(bTg)
  cTt=cTg.dot(gTb).dot(bTt)
  bTg_s.append(bTg)
  cTt_s.append(cTt)

bTg_s=np.array(bTg_s)
cTt_s=np.array(cTt_s)

RT1=solver.solve(bTg_s,cTt_s)
print("Result1",RT1)
print("Quot",tflib.fromRTtoVec(RT1))

