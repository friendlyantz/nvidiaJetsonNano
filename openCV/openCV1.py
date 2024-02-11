import cv2
print("openCV version ====> ", cv2.__version__) # testing openCV VER

# ==> RESOLUTION OPTIONS
# # =>OPT1 - XS
# dispW=320
# dispH=240

# # =>OPT1 - S
# dispW=480
# dispH=320

# =>OPT1 - M
dispW=640
dispH=480

# FLIP OUTPUT
flip=0

# CAM SETTINGS
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

# ==VIDEO CAPTURE MODES -FILE or -CAMERA
videoPathRead = '/home/anton/Videos/nvidiaJetsonStream/jetsonStream2.avi'
# =FROM CAMERA
cam=cv2.VideoCapture(camSet)
# =FROM FILE
# cam=cv2.VideoCapture(videoPathRead)


# ====> WRITE VIDEO TO FILE SETTINGS
# =FILEPATH
# =WRITING - UNCOMMENT THIS OR CHANGE VIDEOPATH WHEN READING FROM FILE - also ENABLE WRITING IN WINDOW 1
videoPathWrite = '/home/anton/Videos/nvidiaJetsonStream/jetsonStream.avi'
outVid=cv2.VideoWriter(videoPathWrite,cv2.VideoWriter_fourcc(*'XVID'),21,(dispW,dispH))

# ~~~~~~~~~~~MAIN SEQUENCE~~~~~~~~~~~~
while True:
    ret, frame=cam.read()
    # ===========God's particle===========

    # rectangual-circle frames,corner,corner/radius, BGR, thickness(-1 for fill shape)
    xAxis=340+1
    frame=cv2.rectangle(frame,(xAxis+30,100),(400,170),(255,0,0),6)
    
    # frame=cv2.circle(frame,(340,240),50,(0,0,255),-1)

    # PUT TEXT 
    fnt=cv2.FONT_HERSHEY_DUPLEX
    frame=cv2.putText(frame,"My First Text", (300,300),fnt,1.5,(112,0,255),2)
   # # PUT LINE
    frame=cv2.line(frame,(10,10),(630,470),(0,0,44),4)
    # # PUT ARROW
    frame=cv2.arrowedLine(frame,(10,470),(430,250),(44,75,142),2)

    # ============Prometheus==============

# Window 1 - DISPLAY AND WRITE!!!!!
    cv2.imshow('nanoCam',frame)
    # window position
    cv2.moveWindow('nanoCam',0,0)
# ===> WRITE VIDEO
    outVid.write(frame)

# # Window 2
#     cv2.imshow('nanoCam2',frame)
#     cv2.moveWindow('nanoCam2',705,0)
# # GREY MOD
#     gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
# # GREY - RESIZE
#     graySmall=cv2.resize(gray,(320,240))
# # Window 3
#     cv2.imshow('grayVideo',gray)
#     cv2.moveWindow('grayVideo',0,520)  
# # Window 4 -RESIZED - S
#     cv2.imshow('grayVideo2',graySmall)
#     cv2.moveWindow('grayVideo2',705,520)

    # exit algorithm (WAITKEY: 1msec for no delay OR LAGGY 50sec wait to match 21 framerate roughly)
    if cv2.waitKey(1)==ord('q'):
        break

# CLEARING MEMORY
cam.release()
outVid.release()
cv2.destroyAllWindows()
