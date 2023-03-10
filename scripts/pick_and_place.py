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

    print("___Release Position___")
    x_f = float(input("distance_x:= "))
    y_f = float(input("distance_y:= "))
    z_f = float(input("distance_z:= "))
    point_f = (x_f, y_f, z_f)
    return point, point_f

if __name__ == "__main__":
    bot = InterbotixManipulatorXS("rx150", "arm", "gripper")
    finish = True
    while finish:
        A, B = get_object_info()
        bot.arm.go_to_home_pose()
        input()
        bot.arm.set_ee_pose_components(x= A[0], y= A[1], z= A[2]+0.08, pitch= 1.57)
        input()
        bot.gripper.open()
        bot.arm.set_ee_cartesian_trajectory(z=-0.08)
        bot.gripper.close()
        bot.arm.set_ee_cartesian_trajectory(z=0.08)

        bot.arm.set_ee_pose_components(x= B[0], y= B[1], z= B[2]+0.08, pitch= 1.57)
        bot.arm.set_ee_cartesian_trajectory(z=-0.08)
        bot.gripper.open()
        bot.arm.set_ee_cartesian_trajectory(z=0.08)

        bot.arm.go_to_home_pose()

        go_to_sleep_pose()

        check = 'a'
        check = input("Repeat?(Y/N)\n")
        if check.upper() == 'N':
            finish = False
    