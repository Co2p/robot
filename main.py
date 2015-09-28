import sys
import calc
import getRequests as get
from getRequests import MRDS_URL
import time
import json
from math import sin,cos,pi,atan2, sqrt

global robot_direction
global goal_direction
global MAX_SPEED
global MAX_SPIN

MAX_SPEED = 0.5
MAX_SPIN = 0.7

print('Sending commands to MRDS server', MRDS_URL)

print(sys.argv[1])
jstr = open(sys.argv[1])
print(jstr)
jsonInstruction = json.load(jstr)


current_position = get.getPose()

print(current_position)
i=0

current_instruction = jsonInstruction[i]
goal_position = current_instruction['Pose']['Position']

def paralellMovement(angular_direction, diff, distance):
    spin = angular_direction * abs(diff)
    speed = distance

    if diff > pi - 1:
        speed = 0

    speed_c = speed / MAX_SPEED
    spin_c = spin / MAX_SPIN

    if speed_c > spin_c:
        speed = speed / speed_c
        spin = spin / speed_c

    else:
        speed = speed / spin_c
        spin = spin / spin_c

    if speed > MAX_SPEED:
        speed = 0.5

    if abs(spin) > 0.5:
        speed = 0.1

        while spin > 1:
            spin = spin - 0.5

        #print('speed: ', speed, 'spin: ', spin)

    get.postSpeed(spin , speed)

def singleMovement():
        #MOVE
        if abs(diff) < 0.01:
            get.postSpeed(0, distance)
            time.sleep(abs(distance)/10)

        #ROTATE
        else:
            print('angular diff ',diff)
            get.postSpeed(angular_direction * 0.6, 0)

while True:


    current_position = get.getPose()

    #calc rotation
    robot_direction = calc.direction(current_position['Pose']['Orientation']['Y'], current_position['Pose']['Orientation']['X'])

    #vector = calc.bearing(calc.qmult(calc.quaternion(current_position['Pose']['Position']), calc.quaternion(current_instruction['Pose']['Position'])))

    vectorX = current_position['Pose']['Position']['X'] - current_instruction['Pose']['Position']['X']
    vectorY = current_position['Pose']['Position']['Y'] - current_instruction['Pose']['Position']['Y']

    goal_direction = calc.direction(vectorY, vectorX)

    #calc movement
    robot_position = current_position['Pose']['Position']

    deltaX = robot_position['X'] - goal_position['X']
    deltaY = robot_position['Y'] - goal_position['Y']

    distance = sqrt((deltaX)**2 + (deltaY)**2)

    diff = (goal_direction - robot_direction)

    angular_direction = 1

    #print('pimary angular diff ',diff * angular_direction)

    if diff > 0:
        while diff > pi:
            print('more ', diff)
            diff = diff - pi * 2

        angular_direction = 1

    elif diff < 0:
        while diff < -pi:
            print('less ', diff)
            diff = diff + pi * 2

    if diff < 0:
        angular_direction = -1

    if distance < 0.2:
        i = i + 1
        print('instruction: ', i)
        current_instruction = jsonInstruction[i]
        goal_position = current_instruction['Pose']['Position']

    else:
        #print('distance', distance)

        #print('distance to goal: ', distance)

        #if abs(diff) > 0.3:
        #    print(distance, '/', diff,'=',abs(distance/diff))
        #    distance = 0#abs(distance/diff)

        print('robot is poining ', robot_direction * 180/pi)
        print('robot should be ', goal_direction * 180/pi)
        #print('diff ', diff)

        #paralellMovement(angular_direction, diff, distance)
        singleMovement()

