#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import subprocess
import navLog

def talker():
    pub.rospy.Publisher('topic', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate=rospy.Rate(10) # 10 hz
    while not rospy.is_shutdown():
        command=navLog.main
        rospy.loginfo(command)
        pub.publish(command)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
