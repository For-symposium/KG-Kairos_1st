from pymycobot.myagv import MyAgv
import cv2

# mc = MyAgv('/dev/ttyAMA2', 115200)
# while True:
#     mc.stop()

# 90 : 240 = x : 480
cap = cv2.VideoCapture(0)
while True:
    cap.set(3, 640)
    cap.set(4, 480)
    ret, img  = cap.read()
    if not ret:
        break
    cv2.imshow('img', img)
    key = cv2.waitKey(1)
    if key&0xff == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()