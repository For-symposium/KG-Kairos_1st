# Video 처리 잘 안 됌

import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while cap.isOpened():
    # ret : Check the validation of data
    ret, frame = cap.read()
    if not ret:
        break

    # 흰색 영역 검출
    lower_white = np.array([0, 0, 100], dtype=np.uint8)
    upper_white = np.array([255, 150, 255], dtype=np.uint8)
    white_mask = cv2.inRange(frame, lower_white, upper_white)
    white_result = cv2.bitwise_and(frame, frame, mask=white_mask)
    
    # 결과 이미지 표시
    cv2.imshow("Original", frame)
    cv2.imshow("White", white_result)

    # 'q' 키 누르면 종료 
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cv2.release()
cv2.destroyAllWindows()
