#!/usr/bin/env python3

import rospy
import matplotlib.pyplot as plt
import os
import numpy as np
from sensor_msgs.msg import JointState

waist = []
shoulder = []
elbow = []
w_a = []
w_r = []
time = []

def update_data(jointState: JointState):
    waist.append(jointState.position[0])
    shoulder.append(jointState.position[1])
    elbow.append(jointState.position[2])
    w_a.append(jointState.position[3])
    w_r.append(jointState.position[4])
    time.append(float(rospy.Time.now().to_nsec()))


def plotting():
    waist_arr = np.array(waist)
    shoulder_arr = np.array(shoulder)
    elbow_arr = np.array(elbow)
    w_a_arr = np.array(w_a)
    w_r_arr = np.array(w_r)
    time_arr = np.array(time)

    y_values = waist_arr
    x_values = time_arr

    plt.title("Waist" + " by Time")
    plt.ylabel("Position (rad)")
    plt.xlabel("Time (sec)")
    plt.grid(True)
    plt.tight_layout()
    plt.plot(x_values, y_values, marker=".")
    figure_saved_path = os.path.join(os.path.dirname(__file__), 'figure/')
    fig_name = f'path.png'
    plt.savefig(figure_saved_path + fig_name, bbox_inches='tight')
    plt.close()

#     for i in range(len(joint_names)):
#         joint_name = joint_names[i]
#         positions = []
#         time = []

#         for j in range(len(points)):
#             positions.append(points[j].positions[i])
#             time.append(points[j].time_from_start.to_sec())

#         y_values = np.array(positions)
#         x_values = np.array(time)

#         plt.title(joint_name + " by Time")
#         plt.ylabel("Position (rad)")
#         plt.xlabel("Time (sec)")
#         plt.grid(True)
#         plt.tight_layout()
#         plt.plot(x_values, y_values, marker=".")
#         figure_saved_path = os.path.join(os.path.dirname(__file__), 'figure/')
#         fig_name = f'path_{count}_{joint_name}.png'
#         plt.savefig(figure_saved_path + fig_name, bbox_inches='tight')
#         plt.close()


if __name__ == "__main__":
    rospy.init_node("Plot_Node")

    sub = rospy.Subscriber( "/rx150/joint_states", JointState, update_data)
    rospy.spin()
    plotting()
