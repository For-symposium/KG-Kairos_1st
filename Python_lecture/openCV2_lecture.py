import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# img_file = cv2.imread("./image/cat.jpg", cv2.IMREAD_UNCHANGED)
# cv2.imshow("Image", img_file)

########################################################

# img = np.zeros((300, 400, 3), np.uint8)
# img[:,:] = (0, 0, 255) # BGR
# cv2.imshow("Red_image", img)

# ## img title만 다르면 여러 창 띄울 수 있음
# img[:,:] = (255, 0, 0) # BGR
# cv2.imshow("Blue_image", img)

# cv2.imshow("Color", img_color)
# cv2.imshow("Gray", img_gray)

########################################################

# img_color = cv2.imread("./image/cat.jpg", cv2.IMREAD_COLOR)
# img_gray = cv2.imread("./image/cat.jpg", cv2.IMREAD_GRAYSCALE)

# img_gray_3dim = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR) ## convert gray scale 2-dim to 3-dim
# h_image_horz = np.hstack((img_color, img_gray_3dim)) ## concatenate horizontally using hstack
# h_image_vert = np.vstack((img_color, img_gray_3dim)) ## concatenate vertically using hstack
# # h_image_horz = np.concatenate((img_color, img_gray_3dim), axis=1) ## concatenate horizontally
# # h_image_vert = np.concatenate((img_color, img_gray_3dim), axis=0) ## concatenate vertically

# cv2.imshow("Concatenate_Horizontal", h_image_horz)
# cv2.imshow("Concatenate_Vertical", h_image_vert)

########################################################

### 3개의 이미지를 컬러-흑백으로 변환해서 각 이미지의 컬러,흑백을 가로로, 이미지별로는 수직으로 3개 이어붙이기

# # img_color = cv2.imread("./image/cat.jpg", cv2.IMREAD_COLOR)
# # cv2.imshow('win', img_color)

# img_color_1 = cv2.imread("./image/picture1.png", cv2.IMREAD_COLOR)
# img_gray_1 = cv2.imread("./image/picture1.png", cv2.IMREAD_GRAYSCALE)
# img_color_2 = cv2.imread("./image/picture2.png", cv2.IMREAD_COLOR)
# img_gray_2 = cv2.imread("./image/picture2.png", cv2.IMREAD_GRAYSCALE)
# img_color_3 = cv2.imread("./image/picture3.png", cv2.IMREAD_COLOR)
# img_gray_3 = cv2.imread("./image/picture3.png", cv2.IMREAD_GRAYSCALE)

# common_width = img_color_1.shape[1] ## for fix width size same

# img_gray_3dim_1 = cv2.cvtColor(img_gray_1, cv2.COLOR_GRAY2BGR) ## convert gray scale 2-dim to 3-dim
# img_gray_3dim_2 = cv2.cvtColor(img_gray_2, cv2.COLOR_GRAY2BGR) ## convert gray scale 2-dim to 3-dim
# img_gray_3dim_3 = cv2.cvtColor(img_gray_3, cv2.COLOR_GRAY2BGR) ## convert gray scale 2-dim to 3-dim

# ## Resizing images with fixed width and proportional ratio of height
# ## size(height, width, channel)
# ## resize(img, Fixed width, New height)
# ## New height = original height * (fixed width / original width)
# img_color_2 = cv2.resize(img_color_2, (common_width, int(img_color_2.shape[0] * common_width / img_color_2.shape[1])))
# img_color_3 = cv2.resize(img_color_3, (common_width, int(img_color_3.shape[0] * common_width / img_color_3.shape[1])))
# img_gray_3dim_2 = cv2.resize(img_gray_3dim_2, (common_width, int(img_gray_3dim_2.shape[0] * common_width / img_gray_3dim_2.shape[1])))
# img_gray_3dim_3 = cv2.resize(img_gray_3dim_3, (common_width, int(img_gray_3dim_3.shape[0] * common_width / img_gray_3dim_3.shape[1])))

# h_image_horz_1 = np.hstack((img_color_1, img_gray_3dim_1)) ## concatenate horizontally using hstack
# h_image_horz_2 = np.hstack((img_color_2, img_gray_3dim_2)) ## concatenate horizontally using hstack
# h_image_horz_3 = np.hstack((img_color_3, img_gray_3dim_3)) ## concatenate horizontally using hstack

# h_image_vert_1 = np.vstack((h_image_horz_1, h_image_horz_2)) ## concatenate vertically using hstack
# h_image_vert_2 = np.vstack((h_image_vert_1, h_image_horz_3)) ## concatenate vertically using hstack

# # h_image_horz = np.concatenate((img_color, img_gray_3dim), axis=1) ## concatenate horizontally
# # h_image_vert = np.concatenate((img_color, img_gray_3dim), axis=0) ## concatenate vertically

########################################################

### 3개의 이미지를 컬러-흑백으로 변환해서 각 이미지의 컬러,흑백을 가로로, 이미지별로는 수직으로 3개 이어붙이기
### 정윤진 ver.

## Get fixed width
# img_for_width = cv2.imread("./image/picture1.png", cv2.IMREAD_COLOR)
# fixed_width = img_for_width.shape[1] 

# def load_img_cvt_gray(path):
#     global fixed_width

#     ## Load images and cvt gray to color
#     img_color = cv2.imread(path, cv2.IMREAD_COLOR)
#     img_gray = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
#     img_gray = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)

#     ## Resize to fixed size
#     img_color = cv2.resize(img_color, dsize=(fixed_width, int(img_color.shape[0] * (fixed_width / img_color.shape[1]))))
#     img_gray = cv2.resize(img_gray, dsize=(fixed_width, int(img_gray.shape[0] * (fixed_width / img_gray.shape[1]))))

#     return img_color, img_gray

# if __name__ == "__main__":
#     img_path = "./image"
#     img_files = ["picture1.png", "picture2.png", "picture3.png"]

#     imgs = list()
#     for name in img_files:
#         IMG_PATH = os.path.join(img_path, name)
#         rimg_color, rimg_gray = load_img_cvt_gray(IMG_PATH)

#         imgs.append(np.concatenate((rimg_color, rimg_gray), axis=1)) ## horizontally

#     ret = np.concatenate(imgs, axis=0) ## vertically


#     cv2.imshow("Concatenate all", ret)

#     while True:
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cv2.destroyAllWindows()

########################################################

## Show image by plotting

# img_file = cv2.imread("./image/cat.jpg", cv2.IMREAD_UNCHANGED)
# img_file = cv2.cvtColor(img_file, cv2.COLOR_BGR2RGB)

# plt.imshow(img_file)
# plt.xticks([])
# plt.yticks([])
# plt.show()

########################################################

## Using CAM

# cap = cv2.VideoCapture("./image/Remote_MQTT_control.mov")
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

# if not cap.isOpened():
#     print("Camera ERROR!")
#     sys.exit()

# while (cap.isOpened()):
#     ret, img = cap.read()
#     if not ret: ## 영상 종료할 타이밍 확인
#         break

#     ## change video to grayscale
#     # img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
#     # img = cv2.flip(img, 1)
#     cv2.namedWindow("img", cv2.WINDOW_NORMAL)
#     # cv2.imshow("CAM", img_gray)
#     cv2.imshow("CAM", img)
    
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()

########################################################

## Recording Video

# cap = cv2.VideoCapture(0)
# cam_width = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# cam_height = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# fps = cap.get(cv2.CAP_PROP_FPS)

# file = './store_vidio.avi'
# fourcc = cv2.VideoWriter_fourcc(*'MJPG')
# out = cv2.VideoWriter(file, fourcc, 25.0, (cam_width, cam_height))

# if not cap.isOpened():
#     print("Camera ERROR!")
#     sys.exit()

# while (cap.isOpened()):
#     ret, frame = cap.read()
#     if not ret: ## 영상 종료할 타이밍 확인
#         break
    
#     frame = cv2.flip(frame, 1)
#     cv2.namedWindow("img", cv2.WINDOW_NORMAL)
#     cv2.imshow("CAM", frame)
#     out.write(frame)
    
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# out.release()
# cap.release()
# cv2.destroyAllWindows()

########################################################

## Plotting line, square, etc

# img_width = 512
# img_height = 512
# img_mid_width = img_width//2
# img_mid_height = img_height//2

# def img_square_center(img, length, thkn=6):
#     img = cv2.rectangle(img, pt1=(img_mid_width-length//2,img_mid_height-length//2), pt2=(img_mid_width+length//2,img_mid_height+length//2), color=(125,100,255), thickness=thkn)
#     return img

# def on_mouse(event, x, y, flags, param):
#     if event == cv2.EVENT_MOUSEMOVE:
#         # 랜덤 색상
#         print("check")
#         R = np.random.randint(0,255)
#         G = np.random.randint(0,255)
#         B = np.random.randint(0,255)
        
#         # 랜덤 크기 원
#         radius = np.random.randint(5,50)
#         cv2.circle(img,(x,y), radius,(R,G,B),-1)
#         cv2.imshow('image', img)
        

# cv2.namedWindow('image')
# img = np.zeros((img_width, img_height, 3), np.uint8) ## black background
# # img = np.full((img_width, img_height, 3), 1, np.float32) ## white background >> But white swallows all other RGB. So set background as black.
# img = cv2.line(img, pt1=(0,0), pt2=(511, 511), color=(255,100,100), thickness=5)
# img = cv2.rectangle(img, pt1=(img_mid_width-50,img_mid_height-50), pt2=(img_mid_width+50,img_mid_height+50), color=(100,255,75), thickness=6)
# img = img_square_center(img, 150)
# img = cv2.circle(img, (img_mid_width,img_mid_height), radius=47, color=(125,125,255), thickness=-1)

# pts = np.array([[10,5], [100,30], [300,170], [280,511]], np.int32) ## poly angular
# img = cv2.polylines(img, [pts], True, (255, 255, 0), 5)

# img = cv2.putText(img, "Hello", (25,img_height//2), cv2.FONT_HERSHEY_COMPLEX, fontScale=3, color=(0,0,0), thickness=3, bottomLeftOrigin=False)

# # cv2.setMouseCallback('image', on_mouse, img)
# cv2.imshow('image', img)

# while True:
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# cv2.destroyAllWindows()

########################################################

## 사각형, 원 모드 변경

# import cv2
# import numpy as np
# drawing = False # Mouse 가 클릭된 상태 확인용
# mode = True # True이면 사각형, false면 원
# ix, iy = -1,-1

# # Mouse callback 함수
# def draw_circle(event, x, y, flags, param):
#     global ix, iy, drawing, ModuleNotFoundError
#     if event == cv2.EVENT_LBUTTONDOWN: # 마우스 누르지 않은 상태
#         drawing = True
#         ix,iy = x,y
#     elif event == cv2.EVENT_MOUSEMOVE: # 마우스 이동
#         if drawing == True:
#             if mode == True:
#                 cv2.rectangle(img,(ix,iy),(x,y),(255,0,0),-1)
#             else:
#                 cv2.circle(img,(x,y),5,(0,255,0),-1)
#     elif event==cv2.EVENT_LBUTTONUP:
#         drawing=False # 마우스 누르면
#         if mode==True:
#             cv2.rectangle(img,(ix,iy),(x,y),(255,0,0),-1)
#         else:
#             cv2.circle(img,(x,y),5,(0,255,0),-1)

# img = np.zeros((512,512,3),np.uint8)
# cv2.namedWindow('image')
# cv2.setMouseCallback('image',draw_circle)

# while True:
#     cv2.imshow('image',img)
#     k=cv2.waitKey(1)&0xFF
#     if k==ord('m'):#사각형 원 mode 변경
#         mode=not mode
#     elif k==ord('q'):
#         break
# cv2.destroyAllWindows()

########################################################

## Trackbar로 color 출력

# def nothing():
#     pass

# img = np.zeros((300,512,3), np.uint8)
# cv2.namedWindow('image') ## image window 먼저 만들고 진행

# ## Create trackbar and listed in named window
# cv2.createTrackbar('R', 'image', 0, 255, nothing)
# cv2.createTrackbar('G', 'image', 0, 255, nothing)
# cv2.createTrackbar('B', 'image', 0, 255, nothing)

# switch = '0:OFF\n1:ON'
# cv2.createTrackbar(switch, 'image', 1, 1, nothing)

# while (True):
#     cv2.imshow('image', img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

#     r = cv2.getTrackbarPos('R', 'image')
#     g = cv2.getTrackbarPos('G', 'image')
#     b = cv2.getTrackbarPos('B', 'image')
#     s = cv2.getTrackbarPos(switch, 'image')

#     if s == 0:
#         img[:] = 0 ## Change all row/col value to 0. Turn to black.
#     else:
#         img[:] = [b,g,r] ## Change color according to r,g,b trackbar

# cv2.destroyAllWindows()

########################################################

## picture brightness toughly control

# src = cv2.imread('./image/cat.jpg', cv2.IMREAD_COLOR)
# dst_1 = cv2.add(src, (100, 100, 100, 0))
# dst_2 = cv2.add(src, (-100, -100, -100, 0))

# cv2.imshow('image_org', src)
# cv2.imshow('image1', dst_1)
# cv2.imshow('image2', dst_2)

# while True:
#     k=cv2.waitKey(1)&0xFF
#     if k==ord('q'):
#         break
# cv2.destroyAllWindows()

########################################################

## 두 사진이 자연스럽게 합쳐지도록! addweighted

# def onChange(x):
#     alpha = x/100
#     dst = cv2.addWeighted(img1, 1-alpha, img2, alpha, 0)
#     cv2.imshow("Addweighted", dst)

# img1 = cv2.imread("./image/cat.jpg")
# img2 = cv2.imread("./image/london.jpg")

# ## img1 shape
# h, w, _ = img2.shape
# img1 = cv2.resize(img1, dsize=(w, h), interpolation=cv2.INTER_AREA)


# cv2.imshow('Addweighted', img1)
# cv2.moveWindow('Addweighted', 200, 100)  # Move to position on the screen
# cv2.createTrackbar('fade', 'Addweighted', 0, 100, onChange)

# while True:
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# cv2.destroyAllWindows()

########################################################

## 카툰 필터 카메라
# import sys
# import numpy as np
# import cv2


# def cartoon_filter(img):
#     h, w = img.shape[:2]
#     img2 = cv2.resize(img, (w//2, h//2))

#     blr = cv2.bilateralFilter(img2, -1, 20, 7)
#     edge = 255 - cv2.Canny(img2, 80, 120)
#     edge = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)

#     dst = cv2.bitwise_and(blr, edge)
#     dst = cv2.resize(dst, (w, h), interpolation=cv2.INTER_NEAREST)

#     return dst


# def pencil_sketch_filter(img):
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     blr = cv2.GaussianBlur(gray, (0, 0), 3)
#     dst = cv2.divide(gray, blr, scale=255)
#     return dst


# # --------------------
# # 시작
# # --------------------
# cap = cv2.VideoCapture(0) 
# if not cap.isOpened():
#     print('video open failed!')
#     sys.exit()

# cam_mode = 0

# while True:
#     ret, frame = cap.read()
#     if not ret: break

#     if cam_mode == 1:
#         frame = cartoon_filter(frame)
#         title = 'filter: cartoon_filter' 
#     elif cam_mode == 2:
#         frame = pencil_sketch_filter(frame)
#         frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
#         title = 'filter: pencil_sketch'
#     else:
#         title = ''   

#     cv2.putText(frame, title, (30, 30),
#             cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 255), 2, cv2.LINE_AA)

#     cv2.imshow('frame', frame)
#     key = cv2.waitKey(1)

#     if key == 27:
#         break
#     elif key == ord(' '): # 스페이스키를 눌러 cam_mode 바꾸기
#         cam_mode += 1
#         if cam_mode == 3:
#             cam_mode = 0


# cap.release()
# cv2.destroyAllWindows()

########################################################

## Canny edge

# src = cv2.imread('./image/london.jpg', cv2.IMREAD_GRAYSCALE)
# dst = cv2.Canny(src, 50, 150)

# cv2.imshow('src', src)
# cv2.moveWindow('src', 0, 75)  # Move to position on the screen
# cv2.imshow('dst', dst)
# cv2.moveWindow('dst', 700, 75)  # Move to position on the screen

# while(1):
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# cv2.destroyAllWindows()

########################################################

# path = './image/lovebird.mp4'
# cap = cv2.VideoCapture(0)
# while True:
#     ret, img = cap.read()
    
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     blur = cv2.GaussianBlur(gray, (5, 5), 0)
#     canny = cv2.Canny(blur, 10, 150)
#     ret, mask = cv2.threshold(canny, 70, 255, cv2.THRESH_BINARY)
#     cv2.imshow('Video feed', mask)
    
#     if cv2.waitKey(1) == ord('q'):
#         break
# cap.release()
# cv2.destroyAllWindows()

########################################################

## Canny edge : image to trackbar

# def onChange(pos):
#     pass

# def edge_detection():
#     img = cv2.imread('./image/london.jpg', cv2.IMREAD_GRAYSCALE)
#     title = 'edge detection'
#     cv2.namedWindow(title)

#     cv2.createTrackbar('low threshold', title, 0, 255, onChange)
#     cv2.createTrackbar('high threshold', title, 0, 255, onChange)
#     cv2.imshow(title, img)

#     while True:
#         if cv2.waitKey(33) == 27:
#             break

#         low = cv2.getTrackbarPos('low threshold', title)
#         high = cv2.getTrackbarPos('high threshold', title)
        
#         if (low==0) and (high==0):
#             cv2.imshow(title, img)
#         elif low > high:
#             print('Low threshold must be low than high threshold!')
#         else:
#             canny = cv2.Canny(img, low, high)
#             cv2.imshow(title, canny)

#     cv2.destroyAllWindows()

# edge_detection()

########################################################

## Canny edge : Video to trackbar

# def onChange(pos):
#     pass

# def edge_tracking():
#     try:
#         print('비디오 재생')
#         video = './image/lovebird.mp4'
#         cap = cv2.VideoCapture(video)
        
#         title = 'edge traking'
#         cv2.namedWindow(title)
#         cv2.createTrackbar('low threshold', title, 0, 255, onChange)
#         cv2.createTrackbar('high threshold', title, 0, 255, onChange)
#     except:
#         print('비디오 재생 실패')
#         return

#     while True:
#         ret, frame = cap.read()

#         if ret:
#             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 

#             if cv2.waitKey(10) == 27:
#                 break

#             low = cv2.getTrackbarPos('low threshold', title)
#             high = cv2.getTrackbarPos('high threshold', title)
        
#             if (low==0) and (high==0):
#                 cv2.imshow(title, frame)
#             elif low > high:
#                 print('Low threshold must be low than high threshold!')
#                 continue
#             else:
#                 frame = cv2.Canny(frame, low, high)
#                 cv2.imshow(title, frame)
#         else:
#             print('비디오 종료')
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# edge_tracking()

########################################################

## Fourier transform

# import cv2
# import matplotlib.pyplot as plt
# import numpy as np

# def fourier(path):
#     img = cv2.imread(path)
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     height, width = gray.shape

#     dft = cv2.dft(np.float32(gray), flags=cv2.DFT_COMPLEX_OUTPUT)
#     dft_shift = np.fft.fftshift(dft)
#     out = 20*np.log(cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1]))

#     inverse_shift = np.fft.fftshift(dft_shift)
#     inverse_dft = cv2.dft(inverse_shift, flags=cv2.DFT_INVERSE)
#     out2 = cv2.magnitude(inverse_dft[:, :, 0], inverse_dft[:, :, 1])

#     plt.subplot(131)
#     plt.imshow(gray, cmap='gray')
#     plt.title('original')
#     plt.subplot(132)
#     plt.imshow(out, cmap='gray')
#     plt.title('dft')
#     plt.subplot(133)
#     plt.imshow(out2, cmap='gray')
#     plt.title('inverse')

#     plt.show()

# fourier('./image/london.jpg')