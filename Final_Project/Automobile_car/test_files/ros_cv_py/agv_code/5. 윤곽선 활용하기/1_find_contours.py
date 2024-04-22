import cv2
import numpy as np

image = cv2.imread('rgb.png')

# Convert to gray scale
# 색상 정보 제거하고, 픽셀의 밝기만 나타내므로 데이터 처리량 줄임
# Edge 검출에 유리
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 가우시안 블러 적용
# 노이즈 줄이고, 이미지의 고주파 성분 줄여서 주요 edge에 집중할 수 있도록 변환
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
# cv2.imshow('blurred', blurred)

# Canny 에지 검출
# Canny의 두 숫자는 minVal, maxVal
# 약한 edge를 제거하고 싶다면 minVal 올리기
# 더 다양한 edge를 표현하고 싶다면 maxVal 내리기
edges = cv2.Canny(blurred, 70, 100)
cv2.imshow('edge', edges)

# 윤곽선 찾기
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 이미지에 윤곽선 그리기
cv2.drawContours(image, contours, -1, (0, 0, 0), 2)

# 결과 보기
cv2.imshow('Contours', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
