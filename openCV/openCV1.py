import cv2
# print("openCV version ====> ", cv2.__version__)
# dispW=320
# dispH=240

dispW=640
dispH=480
flip=0
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam=cv2.VideoCapture(camSet)
while True:
    ret, frame=cam.read()
    # ===========God's particle===========

    # ============Prometheus==============
    # Window 1
    cv2.imshow('nanoCam',frame)
    cv2.moveWindow('nanoCam',0,0)

    # Window 2
    cv2.imshow('nanoCam2',frame)
    cv2.moveWindow('nanoCam2',705,0)
    # grey mod
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    # Window 3
    cv2.imshow('grayVideo',gray)
    cv2.moveWindow('grayVideo',0,520)  
    # Window 4
    cv2.imshow('grayVideo2',gray)
    cv2.moveWindow('grayVideo2',705,520)
    # exit algorithm
    if cv2.waitKey(1)==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()
