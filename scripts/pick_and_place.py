#!/usr/bin/env python3

import math
import rospy
from six.moves import input
from interbotix_xs_modules.arm import InterbotixManipulatorXS
import interbotix_common_modules.angle_manipulation as ang

#Set up new sleep pose
def go_to_sleep_pose():
    bot.arm.set_joint_positions([0, -1.80, 1.65, 0.8, 0])

#Get the objects' information 
def get_object_info():
    print("___Grasp Position___")
    x = float(input("object_distance_x:= "))
    y = float(input("object_distance_y:= "))
    z = float(input("object_distance_z:= "))
    object_pitch = float(input("object_pitch:= "))
    object_roll = float(input("object_roll:= "))
    point = (x, y, z, object_roll, object_pitch)

    print("\n___Release Position___")
    x_f = float(input("distance_x:= "))
    y_f = float(input("distance_y:= "))
    z_f = float(input("distance_z:= "))
    release_pitch = float(input("object_pitch:= "))
    release_roll = float(input("object_roll:= "))
    point_f = (x_f, y_f, z_f, release_roll, release_pitch)
    return point, point_f


if __name__ == "__main__":
    bot = InterbotixManipulatorXS("rx150", "arm", "gripper")

    finish = True
    while finish:
        safety_height = 4*0.01 #Safety space
        object_height = 2.5*0.01 #Object's height

        # A = [(0.2, 0, -5*0.01), (0.15, 0.05, -5*0.01), (0.13, -0.08, -5*0.01)] #Postions of objects
        # B = (0, 0.2, 0.02)

        # for i in range(3):
        #     bot.arm.go_to_home_pose()
        #     bot.arm.set_ee_pose_components(
        #         x=A[i][0], y=A[i][1], z=A[i][2]+object_height+safety_height, pitch=1.57, roll=math.atan2(A[i][1], A[i][0]))
        #     bot.gripper.open()
        #     bot.arm.set_ee_cartesian_trajectory(z=-safety_height+0.01)
        #     bot.gripper.close()
        #     bot.arm.set_ee_cartesian_trajectory(
        #         z=+safety_height-0.01+(B[2]-A[i][2]))
        #     bot.arm.set_ee_pose_components(
        #         x=B[0], y=B[1], z=B[2]+object_height+safety_height, pitch=1.57)
        #     bot.gripper.open()
        # bot.arm.go_to_home_pose()
        # go_to_sleep_pose()

        # check = ''
        # while check != 'Y' and check != 'N':
        #     check = input(
        #         "Continue with custom object position?(Y/N)\n").upper()
        #     if check.upper() == 'N':
        #         finish = False

        if finish:
            finish2 = True
            while finish2:
                # A, B = get_object_info()
                ###VatNam###
                A = (0.15, 0.05, -5*0.01, 0.5, 1.57)
                B = (0, 0.2, 0.02, 0, 0)
                ###VatDung###
                # A = (0.28, 0, 0.15, 0, 0)
                # B = (0, 0.25, 0.08, 0, 1.57)

                if A[4] == 1.57: ###Vat nam tren xy
                    bot.arm.go_to_home_pose()
                    bot.arm.set_ee_pose_components(
                        x=A[0], y=A[1], z=A[2]+object_height+safety_height, roll=math.atan2(A[1], A[0])+A[3], pitch=A[4])
                    bot.gripper.open()
                    bot.arm.set_ee_cartesian_trajectory(z=-safety_height+0.02)
                    bot.gripper.close()
                    bot.arm.set_ee_cartesian_trajectory(
                        z=+safety_height-0.02+(B[2]-A[2]))
                    bot.arm.set_ee_pose_components(
                        x=B[0], y=B[1], z=B[2]+object_height+safety_height, pitch=1.57)
                    
                else: ###Vat thang dung
                    bot.arm.go_to_sleep_pose()
                    bot.arm.set_ee_pose_components(
                        x=A[0]-safety_height, y=A[1], z=A[2])
                    bot.gripper.open()
                    bot.arm.set_ee_cartesian_trajectory(x=+safety_height-0.02)
                    bot.gripper.close()
                    bot.arm.set_ee_cartesian_trajectory(
                        z=+safety_height)
                    bot.arm.set_ee_pose_components(
                        x=B[0], y=B[1], z=B[2], roll= math.atan2(B[1], B[0]) + B[3], pitch= B[4])
                bot.gripper.open()
                bot.arm.go_to_home_pose()
                go_to_sleep_pose()

                check = ''
                while check != 'Y' and check != 'N':
                    check = input(
                        "Keep on custom object position mode?(Y/N)\n").upper()
                    if check.upper() == 'N':
                        finish2 = False

        check = ''
        while check != 'Y' and check != 'N':
            check = input("Exit?(Y/N)\n").upper()
            if check.upper() == 'Y':
                finish = False
