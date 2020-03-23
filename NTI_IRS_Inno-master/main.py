#!/usr/bin/env python

# Example of programming UR robot with gripper

import urx
import math
import time
from UR10_Robot import UR10_Robot

VEL = 1
ACC = 0.2
RVEL = 0.5

MIN = 200

DELTA = 7

rob = UR10_Robot("172.31.1.3", ACC, ACC, VEL, RVEL)

#Положительный y — к основанию
#положительный x — к машинам (влево от основания)
#z ok
DT = 300

if __name__ == "__main__":
    time0 = time.time()
    while True:
        C = []
        rob.construct_map()
        for tar in rob.TO:
            C.append(tar.get_position())
        print(*C)
        print(rob.TO)
        print(len(C))
        '''for coord in C:
            rob.translate(coord[0], coord[1], 0)
            sleep(0.5)'''
        try:
            rob.take_all_cubes('GREEN')
        except:
            pass
        '''try:
            rob.take_all_cubes('RED')
        except Exception:
            pass'''
        if time.time() - time0 >= DT:
            print("Program ended")
            break



    
    '''rob.gr_open()
    rob.get_down_center('GREEN', 'Cube')
    rob.stab_xy('GREEN', 'Cube')
    print(rob.get_pose())
    rob.take_object()
    sleep(2)
    rob.rtranslate(0, 0.3, 0.2)
    rob.get_down_center('GREEN', 'Bucket')
    rob.stab_xy('GREEN', 'Bucket')
    rob.gr_open()'''

    #rob.release_object()
    #rob.release_object()
    '''rob.gr_close()
    sleep(2)
    rob.rtranslate(-0.2, -0.1, 0.1)
    rob.gr_open()
    print(rob.get_pose())
    sleep(2)
    rob.rrotate(3.14/2)
    sleep(0.5)
    rob.rrotate(-3.14/2)
    sleep(0.5)'''
    rob.shutdown()
