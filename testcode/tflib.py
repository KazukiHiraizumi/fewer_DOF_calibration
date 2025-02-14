#!/usr/bin/python

import numpy as np
import math


def tf2dict(tf):
  d={'translation':{'x':0,'y':0,'z':0},'rotation':{'x':0,'y':0,'z':0,'w':0}}
  d['translation']['x']=float(tf.translation.x)
  d['translation']['y']=float(tf.translation.y)
  d['translation']['z']=float(tf.translation.z)
  d['rotation']['x']=float(tf.rotation.x)
  d['rotation']['y']=float(tf.rotation.y)
  d['rotation']['z']=float(tf.rotation.z)
  d['rotation']['w']=float(tf.rotation.w)
  return d

def toRT(tf):
  x=tf.rotation.x
  y=tf.rotation.y
  z=tf.rotation.z
  w=tf.rotation.w
  tx=tf.translation.x
  ty=tf.translation.y
  tz=tf.translation.z
  xx=x*x
  yy=y*y
  zz=z*z
  ww=w*w
  return np.matrix([[xx-yy-zz+ww,2.*(x*y-w*z),2.*(x*z+w*y),tx],[2.*(x*y+w*z),yy+ww-xx-zz,2.*(y*z-w*x),ty],[2.*(x*z-w*y),2.*(y*z+w*x),zz+ww-xx-yy,tz],[ 0, 0, 0, 1]])


def fromRTtoVec(rt):
  if (rt[0,0]+rt[1,1]+rt[2,2]>0):
    s=math.sqrt(1.0+rt[0,0]+rt[1,1]+rt[2,2])*2  #s=qw*4
    qw=s/4
    qx=(rt[2,1]-rt[1,2])/s
    qy=(rt[0,2]-rt[2,0])/s
    qz=(rt[1,0]-rt[0,1])/s
  elif ((rt[0,0]>rt[1,1]) and (rt[0,0]>rt[2,2])):
    s=math.sqrt(1.0+rt[0,0]-rt[1,1]-rt[2,2])*2  #s=qx*4
    qw=(rt[2,1]-rt[1,2])/s
    qx=s/4
    qy=(rt[0,1]+rt[1,0])/s
    qz=(rt[0,2]+rt[2,0])/s
  elif (rt[1,1]>rt[2,2]):
    s=math.sqrt(1.0-rt[0,0]+rt[1,1]-rt[2,2])*2  #s=qy*4
    qw=(rt[0,2]-rt[2,0])/s
    qx=(rt[0,1]+rt[1,0])/s
    qy=s/4
    qz=(rt[1,2]+rt[2,1])/s
  else:
    s=math.sqrt(1.0-rt[0,0]-rt[1,1]+rt[2,2])*2  #s=qz*4
    qw=(rt[1,0]-rt[0,1])/s
    qx=(rt[0,2]+rt[2,0])/s
    qy=(rt[1,2]+rt[2,1])/s
    qz=s/4
  vec=np.array([rt[0,3],rt[1,3],rt[2,3],qx,qy,qz,qw])
  return vec

def inv(tf):
  RT=toRT(tf)
  return fromRT(RT.I)

def toRTfromVec(vec):
  tx=vec[0]
  ty=vec[1]
  tz=vec[2]
  x=vec[3]
  y=vec[4]
  z=vec[5]
  w=vec[6]
  xx=x*x
  yy=y*y
  zz=z*z
  ww=w*w
  return np.matrix([[xx-yy-zz+ww,2.*(x*y-w*z),2.*(x*z+w*y),tx],[2.*(x*y+w*z),yy+ww-xx-zz,2.*(y*z-w*x),ty],[2.*(x*z-w*y),2.*(y*z+w*x),zz+ww-xx-yy,tz],[ 0, 0, 0, 1]])
