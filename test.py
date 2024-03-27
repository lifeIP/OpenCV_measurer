import numpy as np
import cv2

cap0 = cv2.VideoCapture(0)
cap1 = cv2.VideoCapture(1)

while(True):
    
    ret0, frame0 = cap0.read()
    ret1, frame1 = cap1.read()



    if ret0 and ret1:
        img = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)

        cv2.imshow('Source 1',frame1)
        cv2.imshow('Source 2',img)

        rand = cv2.inRange(img, (20, 80, 80), (45, 255, 255))
        frame1[rand==255] = (0,0,255)
        cv2.imshow('rand',rand)

    

        # edges = cv2.Canny(img2, 50, 150)
        # frame1[edges==255] = (0,0,255)
        # cv2.imshow("frame_edges", frame1)
        

        
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap0.release()
cap1.release()
cv2.destroyAllWindows()