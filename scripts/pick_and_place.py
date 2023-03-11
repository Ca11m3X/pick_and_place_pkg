#!/usr/bin/env python3

import rospy
from six.moves import input
from interbotix_xs_modules.arm import InterbotixManipulatorXS

def go_to_sleep_pose():
    bot.arm.set_joint_positions([0, -1.80, 1.65, 0.8, 0])

def get_object_info():
    print("___Grasp Position___")
    x = float(input("object_distance_x:= "))
    y = float(input("object_distance_y:= "))
    z = float(input("object_distance_z:= "))
    point = (x,y,z)

    print("\n___Release Position___")
    x_f = float(input("distance_x:= "))
    y_f = float(input("distance_y:= "))
    z_f = float(input("distance_z:= "))
    point_f = (x_f, y_f, z_f)
    return point, point_f

if __name__ == "__main__":
    bot = InterbotixManipulatorXS("rx150", "arm", "gripper")
    finish = True
    while finish:
        # A, B = get_object_info()
        safety_height = 4*0.01
        object_height = 2.5*0.01 
        # A = (0.2, 0, -5*0.01)
        # A = (0.15, 0.05, -5*0.01)
        # A = (0.1, -0.2, -5*0.01)
        A= [(0.2, 0, -5*0.01), (0.15, 0.05, -5*0.01), (0.13, -0.08, -5*0.01)]
        # print(type(A))
        B = (0, 0.2, 0.02)
        for i in range(3):
            bot.arm.go_to_home_pose()
            bot.arm.set_ee_pose_components(x= A[i][0], y= A[i][1], z= A[i][2]+object_height+safety_height,pitch= 1.57)
            angle = bot.arm.get_single_joint_command('waist')
            bot.arm.set_single_joint_position('wrist_rotate', angle)
            bot.gripper.open()
            bot.arm.set_ee_cartesian_trajectory(z=-safety_height+0.01)
            bot.gripper.close()
            bot.arm.set_ee_cartesian_trajectory(z=+safety_height-0.01+(B[2]-A[i][2]))
            bot.arm.set_ee_pose_components(x= B[0], y= B[1], z= B[2]+object_height+safety_height, pitch= 1.57)
            bot.gripper.open()
            
        bot.arm.go_to_home_pose()
        go_to_sleep_pose()

        check = ''
        while check != 'Y' and check != 'N':
            check = input("Continue with custom object position?(Y/N)\n").upper()
            if check.upper() == 'N':
                finish = False

        if finish:
            finish2 = True
            while finish2:
                A, B = get_object_info()
                bot.arm.go_to_home_pose()
                bot.arm.set_ee_pose_components(x= A[0], y= A[1], z= A[2]+object_height+safety_height,pitch= 1.57)
                angle = bot.arm.get_single_joint_command('waist')
                bot.arm.set_single_joint_position('wrist_rotate', angle)
                bot.gripper.open()
                bot.arm.set_ee_cartesian_trajectory(z=-safety_height+0.02)
                bot.gripper.close()
                bot.arm.set_ee_cartesian_trajectory(z=+safety_height-0.02+(B[2]-A[2]))
                bot.arm.set_ee_pose_components(x= B[0], y= B[1], z= B[2]+object_height+safety_height, pitch= 1.57)
                bot.gripper.open()
                bot.arm.go_to_home_pose()
                go_to_sleep_pose()
                check = ''
                while check != 'Y' and check != 'N':
                    check = input("Keep on custom object position mode?(Y/N)\n").upper()
                    if check.upper() == 'N':
                        finish2 = False

        check = ''
        while check != 'Y' and check != 'N':
            check = input("Exit?(Y/N)\n").upper()
            if check.upper() == 'Y':
                finish = False
