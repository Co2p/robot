"""
Example demonstrating how to communicate with Microsoft Robotic Developer
Studio 4 via the Lokarria http interface. 

Author: Erik Billing (billing@cs.umu.se)

Updated by Ola Ringdahl 204-09-11
"""
import getRequests as get
from getRequests import MRDS_URL
import time
from math import sin,cos,pi,atan2

if __name__ == '__main__':
    print('Sending commands to MRDS server', MRDS_URL)

    while True:
        try:
            laser = get.getLaser()
            laserAngles = get.getLaserAngles()
        except get.UnexpectedResponse as ex:
            print('Unexpected response from server when reading laser data:', ex)


        try:
            pose = get.getPose()
            #print('Current position: ', pose['Pose']['Position'])
            #print('Current heading vector: X:{X:.3}, Y:{Y:.3}'.format(**getBearing()))

        except get.UnexpectedResponse as ex:
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
                    response =  get.postSpeed(1,0)
                    time.sleep(1)

                if rightLaser1 < 0.3 or rightLaser2 < 0.3:
                    response = get.postSpeed(1.3,0.1)

                if leftLaser1 < 0.3 or leftLaser2 < 0.3:
                    response = get.postSpeed(-1.3,0.1)

            elif longest_laser > len(half_laser)/2+7:
                response = get.postSpeed(1, 0.5)

            elif longest_laser < len(half_laser)/2-7:
                response = get.postSpeed(-1, 0.5)

            else:
                response = get.postSpeed(0, 1)
        except get.UnexpectedResponse as ex:
            print('Unexpected response from server when sending speed commands:', ex)

        time.sleep(0.1)
