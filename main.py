import sys
import calc
import getRequests as get
from getRequests import MRDS_URL
import time
import json
from math import sin,cos,pi,atan2, sqrt

global robot_direction
global goal_direction


print('Sending commands to MRDS server', MRDS_URL)

print(sys.argv[1])
jstr = open(sys.argv[1])
print(jstr)
jsonInstruction = json.load(jstr)


current_position = get.getPose()

print(current_position)
i=0

while True:

    current_instruction = jsonInstruction[i]
    print(i)

    current_position = get.getPose()

    #calc rotation
    robot_direction = calc.direction(current_position['Pose']['Orientation'])
    print('robot is poining ', robot_direction)

    vector = calc.qmult(calc.quaternion(current_position['Pose']['Position']), calc.quaternion(current_instruction['Pose']['Position']))

    #vector = calc.bearing(calc.qmult(calc.quaternion(current_position['Pose']['Position']), calc.quaternion(current_instruction['Pose']['Position'])))

    goal_direction = calc.direction(vector)
    print('robot should be ', goal_direction)



    #calc movement
    robot_position = current_position['Pose']['Position']
    goal_position = current_instruction['Pose']['Position']

    deltaX = robot_position['X']-goal_position['X']
    deltaY = robot_position['Y'] - goal_position['Y']

    distance = sqrt((deltaX)**2 + (deltaY)**2)

    print('distance to goal: ', distance)

    if distance > 0.2:
        if (abs(goal_direction - robot_direction) > pi * 2):
            print('Shiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiit')

        get.postSpeed((goal_direction - robot_direction), 0)
        time.sleep(1)
        get.postSpeed(0, distance)
        time.sleep(1)

    else:
        i = i + 1




