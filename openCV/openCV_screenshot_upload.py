
# Set your Cloudinary credentials
# ==============================
from dotenv import load_dotenv
load_dotenv()

# Import the Cloudinary libraries
# ==============================
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Import to format the JSON responses
# ==============================
import json

# Set configuration parameter: return "https" URLs by setting secure=True  
# ==============================
config = cloudinary.config(secure=True)

# Log the configuration
# ==============================
print("****1. Set up and configure the SDK:****\nCredentials: ", config.cloud_name, config.api_key, "\n")

import cv2
import datetime
import time
print("openCV version ====> ", cv2.__version__) # testing openCV VER

dispW=1280
dispH=960
flip=0
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

last_minute=datetime.datetime.now().minute
while True:
    current_time = datetime.datetime.now()
    if current_time.minute != last_minute:
        cam=cv2.VideoCapture(camSet)
        ret, frame=cam.read()
        cv2.imwrite('/home/anton/Desktop/test.jpg', frame)
        cloudinary.uploader.upload('/home/anton/Desktop/test.jpg', public_id="nanocam", unique_filename = False, overwrite=True, invalidate=True)
        print("saved")
        # srcURL = cloudinary.CloudinaryImage("nanocam").build_url()
        # print("****2. Upload an image****\nDelivery URL: ", srcURL, "\n")
        last_minute=current_time.minute
        cam.release()

