#!/usr/bin/env python3

import rospy
from interbotix_xs_modules.arm import InterbotixManipulatorXS

if __name__ == "__main__":
    bot = InterbotixManipulatorXS('rx150', 'arm', 'gripper')
    bot.arm.set_ee_pose_components(x= 0.2, y= 0, z=0.1)
    rospy.spin()