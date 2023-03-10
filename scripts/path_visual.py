#!/usr/bin/env python3
from sensor_msgs.msg import JointState
import rospy
import modern_robotics as mr
import interbotix_xs_modules.mr_descriptions as mrd
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point


marker = Marker()
marker.header.frame_id = "world"
marker.type = marker.SPHERE_LIST
marker.action = marker.ADD
marker.id =0 

marker.scale.x = 0.005
marker.scale.y = 0.005
marker.scale.z = 0.005

marker.color.r = 0.0
marker.color.g = 1.0
marker.color.b = 0.0
marker.color.a = 1.0

# line = Marker()
# line.header.frame_id = "world"
# line.type = Marker.LINE_STRIP
# line.action = Marker.ADD
# line.id =1 

# line.scale.x = 0.02

# line.color.r = 0.0
# line.color.g = 1.0
# line.color.b = 0.0
# line.color.a = 1.0

# line.pose.orientation.x = 0.0
# line.pose.orientation.y = 0.0
# line.pose.orientation.z = 0.0
# line.pose.orientation.w = 1.0

def graph_funct(joint_state: JointState):
    robot_des = getattr(mrd, "rx150")
    T_sb = mr.FKinSpace(robot_des.M, robot_des.Slist, joint_state.position[:5])
    point = Point()
    point.x = T_sb[0,3]
    point.y = T_sb[1,3]
    point.z = T_sb[2,3]
    marker.points.append(point)

# def graph_funct_line(joint_state: JointState):
#     robot_des = getattr(mrd, "rx150")
#     T_sb = mr.FKinSpace(robot_des.M, robot_des.Slist, joint_state.position[:5])
#     point = Point()
#     point.x = T_sb[0,3]
#     point.y = T_sb[1,3]
#     point.z = T_sb[2,3]
#     line.points.append(point)

def get_postion(event):
    get_joint_state = rospy.Subscriber( "/rx150/joint_states", JointState, graph_funct)

# def get_postion_line(event):
#     get_joint_state_line = rospy.Subscriber( "/rx150/joint_states", JointState, graph_funct_line)

def update_markers(event):
    marker_pub.publish(marker)
    # line_pub.publish(line)

if __name__ == "__main__":
    rospy.init_node("Marker_Publisher")
    marker_pub = rospy.Publisher("/rx150/visualization_marker", Marker, queue_size = 100)
    # line_pub = rospy.Publisher("/rx150/visualization_marker", Marker, queue_size = 100)

    rospy.Timer(rospy.Duration(2), get_postion)
    rospy.Timer(rospy.Duration(1), update_markers)
    # rospy.Timer(rospy.Duration(5), get_postion_line)
    rospy.spin()