import cv2
import datetime
print("openCV version ====> ", cv2.__version__) # testing openCV VER
dispW=1440
dispH=1080
flip=2
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=1920, height=1080, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam=cv2.VideoCapture(camSet)

last_minute=datetime.datetime.now().minute
while True:
    current_time = datetime.datetime.now()
    ret, frame=cam.read()

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

    # cv2.imshow('nanoCam',frame)
    # cv2.moveWindow('nanoCam',0,0)

    # WATERMARK
    fnt=cv2.FONT_HERSHEY_DUPLEX
    frame=cv2.putText(frame, current_time.strftime("%Y-%m-%d %H:%M:%S"), (30,50),fnt,1.5,(112,0,255),2)
    frame=cv2.putText(frame, "powered by friendlyantz", (30, 100),fnt,1.0,(112,0,55),1)
    frame=cv2.putText(frame, "buy me a beer --> PayID: friendlyantz@up.me", (dispW - 800, dispH - 30),fnt,1.0,(255,127,0),2)

    # SAVE to FILE
    if current_time.minute != last_minute:
        cv2.imwrite('/home/anton/Desktop/test.jpg', frame)
        print("saved")
        last_minute=current_time.minute
    if cv2.waitKey(1)==ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
