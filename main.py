"""
Example demonstrating how to communicate with Microsoft Robotic Developer
Studio 4 via the Lokarria http interface. 

Author: Erik Billing (billing@cs.umu.se)

Updated by Ola Ringdahl 204-09-11
"""
import getRequests
from getRequests import MRDS_URL
import time
from math import sin,cos,pi,atan2

def bearing(q):
    return rotate(q,{'X':1.0,'Y':0.0,"Z":0.0})

def rotate(q,v):
    return vector(qmult(qmult(q,quaternion(v)),conjugate(q)))

def quaternion(v):
    q=v.copy()
    q['W']=0.0;
    return q

def vector(q):
    v={}
    v["X"]=q["X"]
    v["Y"]=q["Y"]
    v["Z"]=q["Z"]
    return v

def conjugate(q):
    qc=q.copy()
    qc["X"]=-q["X"]
    qc["Y"]=-q["Y"]
    qc["Z"]=-q["Z"]
    return qc

def qmult(q1,q2):
    q={}
    q["W"]=q1["W"]*q2["W"]-q1["X"]*q2["X"]-q1["Y"]*q2["Y"]-q1["Z"]*q2["Z"]
    q["X"]=q1["W"]*q2["X"]+q1["X"]*q2["W"]+q1["Y"]*q2["Z"]-q1["Z"]*q2["Y"]
    q["Y"]=q1["W"]*q2["Y"]-q1["X"]*q2["Z"]+q1["Y"]*q2["W"]+q1["Z"]*q2["X"]
    q["Z"]=q1["W"]*q2["Z"]+q1["X"]*q2["Y"]-q1["Y"]*q2["X"]+q1["Z"]*q2["W"]
    return q
    
def getBearing():
    """Returns the XY Orientation as a bearing unit vector"""
    return bearing(getRequests.getPose()['Pose']['Orientation'])

if __name__ == '__main__':
    print('Sending commands to MRDS server', MRDS_URL)

    while True:
        try:
            laser = getRequests.getLaser()
            laserAngles = getRequests.getLaserAngles()
        except getRequests.UnexpectedResponse as ex:
            print('Unexpected response from server when reading laser data:', ex)


        try:
            pose = getRequests.getPose()
            #print('Current position: ', pose['Pose']['Position'])
            #print('Current heading vector: X:{X:.3}, Y:{Y:.3}'.format(**getBearing()))

        except getRequests.UnexpectedResponse as ex:
            print('Unexpected response from server when reading position:', ex)

        try:
            rightLaser1 = laser['Echoes'][90]
            rightLaser2 = laser['Echoes'][110]
            midLaser = laser['Echoes'][135]
            leftLaser1 = laser['Echoes'][160]
            leftLaser2 = laser['Echoes'][180]

            half_laser = laser['Echoes'][50:220]

            longest_laser = half_laser.index(max(half_laser))

            too_close = False

            for n in half_laser:
                if n < 0.3:
                    too_close = True

            if too_close:
                print('tooclose')
                if midLaser < 0.3:
                    print('midlaser', laser['Echoes'][135])
                    response =  getRequests.postSpeed(1,0)
                    time.sleep(1)

                if rightLaser1 < 0.3 or rightLaser2 < 0.3:
                    response = getRequests.postSpeed(1.3,0.1)

                if leftLaser1 < 0.3 or leftLaser2 < 0.3:
                    response = getRequests.postSpeed(-1.3,0.1)

            elif longest_laser > len(half_laser)/2+7:
                response = getRequests.postSpeed(1, 0.5)

            elif longest_laser < len(half_laser)/2-7:
                response = getRequests.postSpeed(-1, 0.5)

            else:
                response = getRequests.postSpeed(0, 1)
        except getRequests.UnexpectedResponse as ex:
            print('Unexpected response from server when sending speed commands:', ex)

        time.sleep(0.1)
