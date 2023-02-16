
import robolink
import robodk
import time
import os
import xml.etree.ElementTree as XML
import ast
from win32com.shell import shell, shellcon
import configparser
config = configparser.ConfigParser()
coldrun=0
config.read("C:\\Users\\simat\\OneDrive\\Desktop\\ElementaryOperations\\Horn\\example.ini")

stop_index = ast.literal_eval(config['DEFAULT']['stop'])
name_index = ast.literal_eval(config['DEFAULT']['name'])
stop_index2 = ast.literal_eval(config['DEFAULT']['stop2'])
freq = ast.literal_eval(config['DEFAULT']['freq'])
index = ast.literal_eval(config['DEFAULT']['index'])
new_speed = ast.literal_eval(config['DEFAULT']['speed'])
RDK = robolink.Robolink()

robot = RDK.Item("Fanuc M-710iC/70")
RDK.setRunMode(robolink.RUNMODE_RUN_ROBOT)
# RDK.setRunMode(robolink.RUNMODE_SIMULATE)
XMLFile = XML.parse(os.path.join(shell.SHGetFolderPath(0, shellcon.CSIDL_PERSONAL, None, 0), "EWO.xml"))
XMLRoot = XMLFile.getroot()
ProductMeta = XMLRoot.attrib
weldments = []
for child in XMLRoot:
    weldments.append(child)

input('press any key to start weldment')
print('weldment_started')

weld_started = False
i = 0
for wldmnt in weldments:
    
    amal = ast.literal_eval(wldmnt.attrib['WeldBeadSize'])
    
    weld_name = ast.literal_eval(wldmnt.attrib['No'])
    
    if amal < 0.007:
        passes = 1
    elif amal < 0.012:
        passes = 2
    else:
        passes = 5
    print(passes)
    for weld_pass in range(passes):
        if weld_pass > 0:
            robot.setDO(11, 0)
            robot.setDO(13, 0)
            print('weldment finished')
            weld_started = False
        robot.setSpeed(30, 10)
        # try:
        #     approach_name = "Weldment" + str(weld_name) + "Approach"
        #     target = RDK.Item(approach_name)
        #     pose = target.Pose()
        #     # robot.setDO(11, 0)
        #     # robot.setDO(13, 0)
        #     weld_started = False
        #     print('weldment finished')
        #     robot.MoveL(target)
        #     robot.WaitFinished()
        # except Exception:
        #     print("approach not found")
        print(weld_pass)
        ewo_name = "Weldment" + str(weld_name) + "Pass"+ str(weld_pass) + "Target0"
        target = RDK.Item(ewo_name)
        robot.MoveL(target)
        robot.WaitFinished()
        robot.setSpeed(7.5, 10)
        if not weld_started:
            robot.setDO(13, 1)
            robot.setDO(11, 1)
            robot.waitDI(8, 1, 10000)
            weld_started = True
            print('weld started')
        point = 0
        for ewo in wldmnt:
            
            ewo_name = "Weldment" + str(weld_name) + "Pass" + str(weld_pass) + "Target" + str(ast.literal_eval(ewo.attrib['No']))
            target = RDK.Item(ewo_name)
            robot.MoveL(target)
            robot.WaitFinished()

            
                

            print('point reached ')
            print(point)
            point += 1

            if not weld_started and weld_pass > 0:
                robot.setDO(13, 1)
                robot.setDO(11, 1)
                robot.waitDI(8, 1, 10000)
                weld_started = True
                print('weld started')
        

        # weld_name = ast.literal_eval(wldmnt.attrib['No'])
        # robot.setSpeed(30)
    i += 1
    print("w", i)
    
        
robot.setDO(11, 0)
robot.setDO(13, 0)
print('weldment finished')
robot.setSpeed(50, 50)
# approach_name = "Weldment" + str(weld_name) + "Approach"
# target = RDK.Item(approach_name)
# robot.MoveL(target)
# robot.WaitFinished()

    


# name = None
# if freq == 0:
#     name = "TestTarget"
#     robot.setSpeed(30, 10)
#     target = RDK.Item(name + str(0))
#     target.setPose(target.Pose()*robodk.transl(0, 0, -100))
#     robot.MoveL(target)
#     robot.WaitFinished()
#     target.setPose(target.Pose()*robodk.transl(0, 0, 100))
#     target = RDK.Item(name + str(0))
#     robot.MoveL(target)
#     robot.WaitFinished()
#     #robot.setDO("0", 1)
#     weld = False
#     modified_pose = False
#     for i in range(0, index+1):
#         print('hey')
#         if not weld and i not in stop_index2:
#             print('Welding now')
#             robot.setSpeed(6.6667, 13.629392)
#             weld = True
        

#         print(i)
#         target = RDK.Item(name + str(i))
#         robot.MoveL(target)
#         robot.WaitFinished()

#         if i in stop_index2:
#             robot.setSpeed(100, 100)
#             print("Stopped welding")
#             target = RDK.Item(name + str(i))
#             target.setPose(target.Pose()*robodk.transl(0, 0, -100))
            
#             robot.MoveL(target)
#             robot.WaitFinished()
#             weld = False
#             modified_pose = True
        
#         if modified_pose:
#             target.setPose(target.Pose()*robodk.transl(0, 0, 100))
#             modified_pose=False
#         if not weld:
#             input()

# else:
#     name = "WeaveTarget"
#     robot.setSpeed(10, 10)
#     target = RDK.Item(name + str(1))
#     target.setPose(target.Pose()*robodk.transl(0, 0, -100))
#     robot.MoveL(target)
#     robot.WaitFinished()
#     target.setPose(target.Pose()*robodk.transl(0, 0, 100))
#     target = RDK.Item(name + str(2))
#     robot.MoveL(target)
#     robot.WaitFinished()
#     #robot.setDO("0", 1)
#     weld = False
#     modified_pose = False
#     for i in range(2, name_index):
#         if not weld and i not in stop_index:
#             print('Welding now')
#             robot.setSpeed(6.6667, 13.629392)
#             weld = True
#         if i in stop_index:
#             target = RDK.Item(name + str(i))
#             target.setPose(target.Pose()*robodk.transl(0, 0, -100))
#             print("Stopped welding")
#             robot.setSpeed(100, 100)
#             weld = False
#             modified_pose = True

#         print(i)
#         target = RDK.Item(name + str(i))
#         robot.MoveL(target)
#         robot.WaitFinished()
#         if modified_pose:
#             target.setPose(target.Pose()*robodk.transl(0, 0, 100))
#             modified_pose=False
#         if not weld:
#             input()
        


# # robot = RDK.Item("UR5")
# # RDK.setRunMode(robolink.RUNMODE_RUN_ROBOT)

# # for i in range(40):
# #     target = RDK.Item("WeaveTarget" + str(i+1))
# #     robot.MoveL(target)
# #     robot.WaitFinished()
