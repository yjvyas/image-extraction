#!/usr/bin/env python3

import os
import rospy
from duckietown.dtros import DTROS, NodeType
from std_msgs.msg import String
from sensor_msgs.msg import CompressedImage
import cv2
from cv_bridge import CvBridge

class ImageExtraction(DTROS):

    def __init__(self, node_name):
        # initialize the DTROS parent class
        super(ImageExtraction, self).__init__(node_name=node_name, node_type=NodeType.GENERIC)
        # construct publisher
        self.cap = cv2.VideoCapture(2)
        self.pub = rospy.Publisher('~images/compressed', CompressedImage, queue_size=10)
        self.cvbr = CvBridge()

    def run(self):
        # publish message every 1 second
        rate = rospy.Rate(30) # 30Hz
        while not rospy.is_shutdown():
            ret, frame = self.cap.read()
            if ret:
                cmprsmsg = self.cvbr.cv2_to_compressed_imgmsg(frame)  # Convert the image to a compress message
                self.pub.publish(cmprsmsg)
                rospy.loginfo('Publishing image')
                rate.sleep()

if __name__ == '__main__':
    # create the node
    node = ImageExtraction(node_name='image_extraction')
    # run node
    node.run()
    # keep spinning
    rospy.spin()
