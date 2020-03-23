#!/usr/bin/env python

# Example of programming UR robot with gripper

import urx

# blending makes trajectory smoother
def movej_cmd(p, blending = 0, vel = 0.2, acc = 0.2):
    return "movej([{},{},{},{},{},{}], a={}, v={}, t=0, r={}) \n".format(p[0], p[1], p[2], p[3], p[4], p[5], acc, vel, blending)

def close_gripper_cmd():
    prog = ''
    prog += 'set_tool_digital_out(0, True)\n'
    prog += 'set_tool_digital_out(1, False)\n'
    prog += 'sleep(0.7)\n'
    return prog

def open_gripper_cmd():
    prog = ''
    prog += 'set_tool_digital_out(0, False)\n'
    prog += 'set_tool_digital_out(1, True)\n'
    prog += 'sleep(0.7)\n'
    return prog

rob = urx.Robot("172.31.1.3")
print("Connected to UR")

p1 = [1.8908352851867676, -1.662417551080221, 2.1432841459857386, -2.2762657604613246, -1.5395177046405237, 2.842644453048706]
p2 = [1.2429156303405762, -2.1738087139525355, 1.926166836415426, -1.4705680173686524, -1.4161360899554651, 2.0479683876037598]
p3 = [1.0125579833984375, -1.9873339138426722, 2.3369506041156214, -1.9662381611266078, -1.385411564503805, 2.0025296211242676]

# generate URScript in form of string and then send to robot

header = "def myProg():\n"
end = "end\n"
prog = header # first put header into program code 

prog += movej_cmd(p1)	
prog += close_gripper_cmd()
prog += movej_cmd(p2, 0.2)
prog += movej_cmd(p3)
prog += open_gripper_cmd()

prog += end

rob.send_program(prog)

rob.close()
