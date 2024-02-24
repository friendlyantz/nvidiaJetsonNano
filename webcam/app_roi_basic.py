#!/usr/bin/python3

import cv2
import time
import datetime
import threading
import pdb
from flask import Response, Flask, render_template, send_from_directory

# Image frame sent to the Flask object
global video_frame
video_frame = None

# Use locks for thread-safe viewing of frames in multiple browsers
global thread_lock 
thread_lock = threading.Lock()

global last_minute 
last_minute = datetime.datetime.now().minute

# GStreamer Pipeline to access the Raspberry Pi camera
flip=2
dispW=1440
dispH=1080
# dispW=960
# dispH=616
GSTREAMER_PIPELINE = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=1920, height=1080, format=(string)NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink wait-on-eos=false max-buffers=1 drop=True'

# Create the Flask object for the application
app = Flask(__name__)

def captureFrames():
    global video_frame, thread_lock

    # Video capturing from OpenCV
    video_capture = cv2.VideoCapture(GSTREAMER_PIPELINE, cv2.CAP_GSTREAMER)

    while True and video_capture.isOpened():
        return_key, frame = video_capture.read()
        if not return_key:
            break

        # Create a copy of the frame and store it in the global variable,
        # with thread safe access
        with thread_lock:
            # resized_frame = frame[200:800, 0:1100]
            roi = frame[700:800, 0:1100].copy() # height, width
            roiGray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            roiGray = cv2.cvtColor(roiGray, cv2.COLOR_GRAY2BGR)
            frame[700:800, 0:1100]=roiGray
            cropped_frame = frame[200:800, 0:1100] 

            watermark(cropped_frame)
            save_to_disk(cropped_frame)
            video_frame = cropped_frame.copy()
        
        key = cv2.waitKey(30) & 0xff
        if key == 27:
            break

    video_capture.release()
        
def save_to_disk(frame):
    global last_minute
    if datetime.datetime.now().minute != last_minute:
        cv2.imwrite('/home/anton/Desktop/test.jpg', frame)
        print("saved")
        last_minute=datetime.datetime.now().minute

def watermark(frame):
    fnt=cv2.FONT_HERSHEY_DUPLEX
    frame=cv2.putText(frame, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), (30,50),fnt,1.5,(112,0,255),2)
    frame=cv2.putText(frame, "powered by friendlyantz", (30, 100),fnt,1.0,(112,0,55),1)
    frame=cv2.putText(frame, "buy CEO a beer --> PayID: friendlyantz@up.me", (30, len(frame) - 20),fnt,1.0,(255,127,0),2)

def blur(frame):
    # BLUR
    height, width = frame.shape[:2]
    start_x = int(0.55 * width)
    end_x = width
    start_y = int(0.65 * height)
    end_y = height
    region_to_blur = frame[start_y:end_y, start_x:end_x]
    blurred_region = cv2.GaussianBlur(region_to_blur, (25, 25), 0)

    frame[start_y:end_y, start_x:end_x] = blurred_region

    # BLUR
    height, width = frame.shape[:2]
    start_x = int(0.75 * width)  
    end_x = width
    start_y = int(0.00 * height)
    end_y = height
    region_to_blur = frame[start_y:end_y, start_x:end_x]
    blurred_region = cv2.GaussianBlur(region_to_blur, (25, 25), 0)
    frame[start_y:end_y, start_x:end_x] = blurred_region

def encodeFrame():
    global thread_lock
    while True:
        # Acquire thread_lock to access the global video_frame object
        with thread_lock:
            global video_frame
            if video_frame is None:
                continue
            return_key, encoded_image = cv2.imencode(".jpg", video_frame)
            if not return_key:
                continue

        # Output image as a byte array
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
            bytearray(encoded_image) + b'\r\n')

@app.route("/stream")
def streamFrames():
    return Response(encodeFrame(), mimetype = "multipart/x-mixed-replace; boundary=frame")

PICTURE_DIRECTORY = '/home/anton/Desktop'
@app.route('/')
def index():
    return send_from_directory(PICTURE_DIRECTORY , 'test.jpg')

@app.route('/test')
def test():
    return render_template('test.html', picture_files=['test.jpg'])

@app.route('/pictures/<filename>')
def render_picture(filename):
    return send_from_directory(PICTURE_DIRECTORY , filename)

# check to see if this is the main thread of execution
if __name__ == '__main__':

    # Create a thread and attach the method that captures the image frames, to it
    process_thread = threading.Thread(target=captureFrames)
    process_thread.daemon = True

    # Start the thread
    process_thread.start()

    # start the Flask Web Application
    # While it can be run on any feasible IP, IP = 0.0.0.0 renders the web app on
    # the host machine's localhost and is discoverable by other machines on the same network 
    app.run(
            "0.0.0.0", 
            port="5000",
            # debug=True
            )
