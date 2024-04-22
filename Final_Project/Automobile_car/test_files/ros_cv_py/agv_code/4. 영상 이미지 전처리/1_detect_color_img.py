import cv2
import numpy as np

# 이미지 읽기
img_path = "rgb.png"
image = cv2.imread(img_path)

# BGR을 HSV 컬러 스페이스로 변환
# HSV는 Hue에서 색상을 한 차원으로만 다루기 때문에 RGB보다 색상 처리가 간단함
# Hue(색상), Saturation(채도, 높을수록 순수한 색, 낮을수록 회색), Value(명도, 밝기 높낮이 조절)
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# 흰색 영역 검출
lower_white = np.array([0, 0, 200], dtype=np.uint8)
upper_white = np.array([255, 30, 255], dtype=np.uint8)

# lower ~ upper 범위에 있는 모든 hsv pixel 검출
white_mask = cv2.inRange(hsv, lower_white, upper_white)

# image를 white_mask 값을 기반으로 bitwise_and 연산
# Masking 통해서 흰색 부분만 반영되고, 나머지는 검정색으로 설정
white_result = cv2.bitwise_and(image, image, mask=white_mask)

# 결과 이미지 표시
cv2.imshow("Original", image)
cv2.imshow("White", white_result)

# 창 종료 
cv2.waitKey(0)
cv2.destroyAllWindows()
