import cv2
import numpy as np
import time

i = 0

def func_test():
    global i
    epsilon_offset = 0.03

    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    if not cap.isOpened():
        print("Error: Unable to open camera")
        return
    
    cap.set(3, 640)
    cap.set(4, 480)

    cx = 0
    cy = 0
    normal_pub_cam_mode = True

    while True:
        ret, img = cap.read()
        if not ret:
            break

        height, width, _ = img.shape # 640x480

        # Black line
        roi_height = round(height * 0.90)
        roi_width = 0
        roi = img[roi_height:, roi_width:(width - roi_width)]
        img_cvt = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        img_mask = cv2.inRange(img_cvt, np.array([0, 0, 0]), np.array([200, 120, 50]))
        cont_list, _ = cv2.findContours(img_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        offset = width // 4
        try:
            if cont_list:
                c = max(cont_list, key=cv2.contourArea)
                M = cv2.moments(c)
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])

                if normal_pub_cam_mode: # if only normal driving mode
                    print(f"Center point (Normal) : {cx} {i}")
                    i += 1
                    cv2.drawContours(roi, c, -1, (0, 0, 255), 1)
                    cv2.circle(roi, (cx, cy), 5, (0, 255, 0), -1)

                    epsilon = epsilon_offset * cv2.arcLength(c, True)
                    approx = cv2.approxPolyDP(c, epsilon, True)

                    sorted_points = sorted(approx, key=lambda point: point[0][1])
                    top_two_points = sorted_points[:2]
                    top_x_distance = abs(top_two_points[0][0][0] - top_two_points[1][0][0])

                    sorted_points_reverse = sorted(approx, key=lambda point: point[0][1], reverse=True)
                    bottom_two_points = sorted_points_reverse[:2]
                    bottom_x_distance = abs(bottom_two_points[0][0][0] - bottom_two_points[1][0][0])

                    for point in sorted_points:
                        x, y = point[0]
                        cv2.circle(roi, (x, y), 5, (255, 0, 0), -1)

                    if len(approx) > 4:
                        i = 0
                        while i < 1000:
                            another_func()

        except Exception as e:
            print(f"Exception STOP: {e}")

        finally:
            key = cv2.waitKey(5)
            cv2.imshow('mask', img)
            if key & 0xff == ord('q'):
                print("q sign off")
                break
    cv2.destroyAllWindows()
    cap.release()

def another_func():
    global i
    print(f"another_func {i}")
    i += 1

if __name__ == '__main__':
    try:
        func_test()

    except:
        print("STOP")