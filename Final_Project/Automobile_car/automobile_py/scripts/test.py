from pymycobot.myagv import MyAgv
import cv2

mc = MyAgv('/dev/ttyAMA2', 115200)
while True:
    mc.stop()


# cap = cv2.VideoCapture(0)
# while True:
#     cap.set(3, 320)
#     cap.set(4, 240)
#     ret, img  = cap.read()
#     if not ret:
#         break
#     cv2.imshow('img', img)
#     key = cv2.waitKey(1)
#     if key&0xff == ord('q'):
#         break

# cv2.destroyAllWindows()
# cap.release()