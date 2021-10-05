#!/usr/bin/env python
"""
Publishes velocity messages to move the turtle in the direction of the waypoints.

Publisher:
topic - turtle_cmd  message type - turtle_control/TurtleVelocity

Subscriber:
topic - /turtle1/pose message type - turtlesim/Pose

Server:
topic - /restart message type - turtle_control/Start




"""

import rospy
from turtlesim.msg import Pose
from turtlesim.srv import TeleportRelative, TeleportAbsolute, SetPen
from std_msgs.msg import String
from turtle_control.msg import TurtleVelocity
from geometry_msgs.msg import Twist
from turtle_control.srv import Start
from std_srvs.srv import Empty, EmptyResponse
import math
from math import atan2,sqrt



PI = 3.14
i = 0
t0 = 0
t1 = 0
t2 = 0
t3 = 0
init_x = 0
init_y = 0

def callback(data):   
    """
    Collects the waypoints, calculates the orientation of the turtle with respect to the waypoints and publishes velocity messages on turtle_cmd

    Args:
        data

    Returns:
        None

    """



  
    turtle_pos = data
    
    
    
    waypoints = rospy.get_param("/waypoint")
    
    


    vel_pub = rospy.Publisher('turtle_cmd', TurtleVelocity, queue_size = 10)

    turtle_velocities= TurtleVelocity()
    turtle_velocities.linear = 0.5
    turtle_velocities.angular = 0.5
    rospy.loginfo(turtle_velocities)

    linear_speed = 0.5
    angular_speed = 0.5

    diff_1_x = waypoints[0][0] - turtle_pos.x
    diff_1_y = waypoints[0][1] - turtle_pos.y
        
    diff_2_x = waypoints[1][0] - waypoints[0][0]
    diff_2_y = waypoints[1][1] - waypoints[0][1]

    diff_3_x = waypoints[2][0] - waypoints[1][0]
    diff_3_y = waypoints[2][1] - waypoints[1][1]

    diff_4_x = waypoints[3][0] - waypoints[2][0]
    diff_4_y = waypoints[3][1] - waypoints[2][1]

    initial_angle = turtle_pos.theta #converting the initial angle of turtle from degrees to radians

    #first angle represents the angle made by the initial position of the turtle with respect to the first waypoint 

    first_angle = atan2(diff_1_y, diff_1_x)    
    second_angle = atan2(diff_2_y, diff_2_x)
    third_angle = atan2(diff_3_y, diff_3_x)
    fourth_angle = atan2(diff_4_y, diff_4_x)

    

    rospy.loginfo(first_angle)
    rospy.loginfo(initial_angle)
    if (first_angle - initial_angle > 0.5): #a < x < b
        turtle_velocities.linear = 0
        vel_pub.publish(turtle_velocities)
             
    else:
        turtle_velocities.angular = 0
        vel_pub.publish(turtle_velocities)
        if (diff_1_x == 0 and diff_1_y == 0):
            turtle_velocities.angular = 0
            turtle_velocities.linear = 0
            vel_pub.publish(turtle_velocities)
            


    '''if (second_angle - first_angle > 0.5): #a < x < b
        turtle_velocities.linear = 0
        vel_pub.publish(turtle_velocities)
        #t1 = rospy.Time.now().to_sec()
        #current_distance = linear_speed * (t1 - t0)
        #if (current_distance == dish_tresh):
        #    i+=1       
    else:
        turtle_velocities.angular = 0
        vel_pub.publish(turtle_velocities)'''
    
    '''if (first_angle == second_angle): #change to some range
        turtle_velocities.angular = 0
        vel_pub.publish(turtle_velocities)
        t2 = rospy.Time.now().to_sec()
        current_distance = linear_speed * (t2 - t1)
        rospy.loginfo(current_distance)
        if (dish_tresh == waypoint_1):
            i+=1       
    else:
        turtle_velocities.linear = 0
        vel_pub.publish(turtle_velocities)  
    

    
    if (second_angle == third_angle):
        turtle_velocities.angular = 0
        vel_pub.publish(turtle_velocities)
        t3 = rospy.Time.now().to_sec()
        current_distance = linear_speed * (t3 - t2)
        rospy.loginfo(current_distance)
        if (current_distance == dish_tresh):
            i+=1       
    else:
        turtle_velocities.linear = 0
        vel_pub.publish(turtle_velocities)


    
    if (third_angle == fourth_angle):
        turtle_velocities.angular = 0
        vel_pub.publish(turtle_velocities)
        t4 = rospy.Time.now().to_sec()
        current_distance = linear_speed * (t4 - t3)
        rospy.loginfo(current_distance)
        if (current_distance == dish_tresh):
            i+=1       
    else:
        turtle_velocities.linear = 0
        vel_pub.publish(turtle_velocities)'''


    
def restart_fn(req):

    """
    collects the waypoints, resets the turtle, draws the waypoints

    Args:
    req

    Returns:
    
    distance - the distance covered by the turtle by moving from the starting position to the final waypoint

    """
    init_x = req.x
    init_y = req.y
    
    init = [init_x, init_y]
    waypoints = rospy.get_param("/waypoint")
    #rospy.Subscriber('/turtle1/pose', Pose, callback)
    #turtle_pos = rospy.ServiceProxy('turtle1/teleport_absolute', TeleportAbsolute)
    
   
    reset_service = rospy.ServiceProxy('reset', Empty)
    reset_service()
        
    draw_service = rospy.ServiceProxy('draw', Empty)
    draw_service()


    turtle_set_pen_1 = rospy.ServiceProxy('turtle1/set_pen', SetPen)
    turtle_set_pen_1(255, 255, 0, 5, True)
    
    teleport_turtle_abs_1= rospy.ServiceProxy('turtle1/teleport_absolute',TeleportAbsolute)
    teleport_turtle_abs_1(1, 1, 30)

    
        
    rospy.Subscriber('/turtle1/pose', Pose, callback)
    
    distance1 = math.dist(waypoints[0], init)
    distance2 = math.dist(waypoints[1], waypoints[0])
    distance3 = math.dist(waypoints[2], waypoints[1])
    distance4 = math.dist(waypoints[3], waypoints[2])


    distance = distance1+distance2+distance3+distance4

        
    return distance









def follower():
    """
    This function initalizes the follower node. 
    
    The node will provide restart service to reset and draw the waypoints by calling the draw service


    """
    rospy.init_node('follower', anonymous = True)
    
    
    rospy.Service('restart', Start, restart_fn)





if __name__ == "__main__":
    follower()
    rospy.spin()