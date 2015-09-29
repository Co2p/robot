import sys
import calc
import getRequests as get
from getRequests import MRDS_URL
import time
import json
import math
from math import pi, sqrt


angular_direction = 1
old_diff = 0
MAX_SPEED = 4
MAX_SPIN = 4

starttime = 0

print('Sending commands to this MRDS server: ', MRDS_URL)

print(sys.argv[1])
jstr = open(sys.argv[1])
print(jstr)
jsonInstruction = json.load(jstr)


current_position = get.getPose()

print(current_position)
i=0

current_instruction = jsonInstruction[i]
goal_position = current_instruction['Pose']['Position']

def paralellMovement(diff, distance):
    global angular_direction

    spin = angular_direction * abs(diff)
    speed = distance

    if diff > pi - 0.5:
        speed = 0

    speed_c = speed / MAX_SPEED
    spin_c = spin / MAX_SPIN

    if abs(spin) > 0.5:
        speed = 0.1

        while spin > 1:
            spin = spin - 0.5

        #print('speed: ', speed, 'spin: ', spin)

    if speed_c > spin_c:
        speed = speed / speed_c
        spin = spin / speed_c
        get.postSpeed(spin , speed)

    else:
        speed = speed / spin_c
        spin = spin / spin_c
        get.postSpeed(spin , speed)

def singleMovement():
        global angular_direction

        #MOVE
        if abs(diff) < distance / 40:
            print('distance ', distance)
            get.postSpeed(0, distance)
            time.sleep(abs(distance)/10)
            get.postSpeed(0, 0)


        #ROTATE
        else:
            print('angular diff ',diff)
            get.postSpeed(angular_direction * 0.5, 0)
            time.sleep(abs(diff) / 2)
            get.postSpeed(0, 0)

def getDiff(diff):
    global angular_direction
    global old_diff

    #if diff > pi:
    while diff > pi:
        #print('more ', math.degrees(diff))
        diff = diff - pi * 2

    #elif diff < -pi:
    while diff < -pi:
        #print('less ', math.degrees(diff))
        diff = diff + pi * 2

    if diff < 0:
        angular_direction = -1
    else:
        angular_direction = 1

    #print('diff ', math.degrees(diff), '\n')

    return diff

while i < len(jsonInstruction) -1:

    if len(jsonInstruction) - 1 - i is 70:
        print('################## SLOW SPEED #################')
        MAX_SPEED = 0.5

    current_position = get.getPose()

    #calc rotation
    #robot_direction = calc.direction(current_position['Pose']['Orientation']['Y'], current_position['Pose']['Orientation']['X'])

    vector = calc.bearing(current_position['Pose']['Orientation'])
    robot_direction = calc.direction(vector['Y'], vector['X'])

    vectorX = current_instruction['Pose']['Position']['X'] - current_position['Pose']['Position']['X']
    vectorY =  current_instruction['Pose']['Position']['Y'] - current_position['Pose']['Position']['Y']

    goal_direction = math.atan2(vectorY, vectorX)

    #calc movement
    robot_position = current_position['Pose']['Position']

    deltaX = robot_position['X'] - goal_position['X']
    deltaY = robot_position['Y'] - goal_position['Y']

    distance = sqrt((deltaX)**2 + (deltaY)**2)

    #print('pimary angular diff ',diff * angular_direction)

    if distance < 0.8:
        i = i + 1
        current_instruction = jsonInstruction[i]
        goal_position = current_instruction['Pose']['Position']

    else:
        if starttime is not 0:
            print('Started the clock')
            starttime = time.time()

        diff = (goal_direction - robot_direction)
        diff = getDiff(diff)
        #print('direction ', math.degrees(robot_direction), ' should be ', math.degrees(goal_direction))

        print('%.1f%% of the track' %((i / (len(jsonInstruction) - 1)) * 100))
        paralellMovement(diff, distance)
        #singleMovement()

print('%.1f%% of the track' %((i / (len(jsonInstruction) - 1)) * 100))
get.postSpeed(0,0)

print('Done!, took %.2f ' %(time.time() - starttime))