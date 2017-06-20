# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 22:18:54 2017

@author: tamji
"""

import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('rotate.png',1)

# Initiate STAR detector
orb = cv2.ORB_create()

# find the keypoints with ORB
kp = orb.detect(img,None)

# compute the descriptors with ORB
kp, des = orb.compute(img, kp)
print type(kp[0])
print (des[0])
# draw only keypoints location,not size and orientation
img2 = cv2.drawKeypoints(img,kp, None, color=(0,255,0), flags=0)

plt.imshow(img2),plt.show()