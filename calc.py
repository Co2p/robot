from math import sin,cos,pi,atan2

def bearing(quaternion):
    return rotate(quaternion,{'X': 1.0,'Y':0.0,"Z":0.0})

def rotate(quaternion,vector):
    return vector(qmult(qmult(quaternion,quaternion(vector)),conjugate(quaternion)))

def quaternion(vector):
    quaternion=vector.copy()
    quaternion['W']=0.0;
    return quaternion

def vector(quaternion):
    vector={}
    vector["X"]=quaternion["X"]
    vector["Y"]=quaternion["Y"]
    vector["Z"]=quaternion["Z"]
    return vector

def conjugate(quaternion):
    qc=quaternion.copy()
    qc["X"]=-quaternion["X"]
    qc["Y"]=-quaternion["Y"]
    qc["Z"]=-quaternion["Z"]
    return qc

def qmult(quaternion1,quaternion2):
    quaternion={}
    quaternion["W"]=quaternion1["W"]*quaternion2["W"]-quaternion1["X"]*quaternion2["X"]-quaternion1["Y"]*quaternion2["Y"]-quaternion1["Z"]*quaternion2["Z"]
    quaternion["X"]=quaternion1["W"]*quaternion2["X"]+quaternion1["X"]*quaternion2["W"]+quaternion1["Y"]*quaternion2["Z"]-quaternion1["Z"]*quaternion2["Y"]
    quaternion["Y"]=quaternion1["W"]*quaternion2["Y"]-quaternion1["X"]*quaternion2["Z"]+quaternion1["Y"]*quaternion2["W"]+quaternion1["Z"]*quaternion2["X"]
    quaternion["Z"]=quaternion1["W"]*quaternion2["Z"]+quaternion1["X"]*quaternion2["Y"]-quaternion1["Y"]*quaternion2["X"]+quaternion1["Z"]*quaternion2["W"]
    return quaternion

def direction(vectorY, vectorX):
    """
    180*pi
    """
    return atan2(vectorY, vectorX)