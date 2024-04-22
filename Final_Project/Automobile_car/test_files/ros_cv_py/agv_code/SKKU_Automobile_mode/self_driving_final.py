import cv2
import numpy as np
import matplotlib.pyplot as plt
import Function_Library as fl
import csv
import numpy as np
import serial
import get_data_coor_and_speed
import time
results = []

f = open('full_course_final.csv','r',encoding='utf-8')
rdr = csv.reader(f)
label = np.array(list(rdr))

minpix = 5

lane_bin_th = 145


fps=30.
mp4_width=640
mp4_height=480
codec=cv2.VideoWriter_fourcc(*'DIVX')

result_path='sdf.mp4'
mp4_result=cv2.VideoWriter(result_path, codec, fps, (mp4_width, mp4_height))


##### Video setup #####
cap=cv2.VideoCapture(0)
ser = get_data_coor_and_speed.libARDUINO()
ser.init('COM6',9600)
start = 0

prev_target_pixel= None
prev_target_pixel_2= None
prev_target_pixel_3= None
prev_target_pixel_4= None
count = 0
middle_point = np.array([0, 0])

train_data = []
while cap.isOpened(): # cap 정상동작 확인
    time1 = time.time()
    count += 1
    ret, image = cap.read()
    # 프레임이 올바르게 읽히면 ret은 True
    if not ret:
        print("프레임을 수신할 수 없습니다. 종료 중 ...")
        break
    
    ##### Perspective Transform #####
    #카메라 영상 촬영후 좌표조정하기
    pts1 = np.float32([[65,240], [575, 240], [0,480], [640, 480]])
    pts2 = np.float32([[0,0], [640,0], [0,480], [640,480]])
    # 변환 행렬 계산 
    mtrx = cv2.getPerspectiveTransform(pts1, pts2)
    # 원근 변환 적용
    result = cv2.warpPerspective(image, mtrx, (640, 480))
    result = image

    ##### Edge and Color detection #####
    edges = cv2.Canny(result, 80, 120)# threshold : 어느 정도 세기를 edge로 인식할건지
    lower_white = np.array([160, 160, 160])
    upper_white = np.array([255, 255, 255])
    rgb_mask = cv2.inRange(result, lower_white, upper_white)

    red = (0, 0,255)
    blue = (255, 0, 0)

    
    # reference line 
    # reference_line_coordinate = [(311, 479), (318, 357)]
    # middle_point = (312,479)
    reference_line_coordinate = [(518, 477),(460, 271)]
    reference_line_inclination = ((reference_line_coordinate[1][0] - reference_line_coordinate[0][0]))*2 , ((reference_line_coordinate[1][1] - reference_line_coordinate[0][1])*2)
    # cv2.line(rgb_mask, reference_line_coordinate[0], reference_line_coordinate[1], red, 3)
   
    # white = cv2.bitwise_and(result, result, mask=hsv_mask) # 원래 이미지와 마스크를 합성
    white_pixels = np.where(rgb_mask == 255)
    l_target_pixels = []
    l_target_pixel_2s = []
    l_target_pixel_3s = []
    l_target_pixel_4s = []

    # 처음 시작할 때, y축이 470 && x > 250 인 pixel만 추출
    if start == 0:
        for i in range(len(white_pixels[0])):
            if white_pixels[0][i] == 450:# y축이 470인 픽셀만 추출
                if white_pixels[1][i] > 250:
                    l_target_pixels.append(white_pixels[1][i])
    # 나중에도 offset 20인 범위에 있는 pixel만 추출
    else:            
        for i in range(len(white_pixels[0])):
            if white_pixels[0][i] == 450:# y축이 470인 픽셀만 추출
                if prev_target_pixel+20 >white_pixels[1][i] > prev_target_pixel-20:
                    l_target_pixels.append(white_pixels[1][i])
                
    l_target_pixels.sort()
    l_target_pixel_2s.sort()
    l_target_pixel_3s.sort()
    l_target_pixel_4s.sort()
    
   
    
    # 여기서부터 시작 만약 픽셀이 연속적이면 가장 앞의 픽셀을 target으로 삼고 끝 픽셀과의 거리가 내가 설정한 범위면 그 픽셀을 target으로 삼는다.
    temp_target = []
    print(l_target_pixels)
    for i in range(len(l_target_pixels)):
        
        if i == len(l_target_pixels)-1:
            if temp_target == []:
                target_pixel = prev_target_pixel
                break
            pixel_difference = abs(temp_target[0] - temp_target[-1])

            if 30 > pixel_difference > 9:
                
                l_target_pixel = temp_target[-1]
                break
            
            else:
                temp_target = []
            break
        if abs(l_target_pixels[i] - l_target_pixels[i+1])<4:
            temp_target.append(l_target_pixels[i])
           
        else:
            temp_target.append(l_target_pixels[i])
            pixel_difference = abs(temp_target[0] - temp_target[-1])
            if 30>pixel_difference > 9:
                
                l_target_pixel = temp_target[-1]
                break
            elif pixel_difference > 50:
                l_target_pixel = temp_target[-1]
                break
            else:
                temp_target = []
    temp_target = []
  
    if start == 0:
        for i in range(len(white_pixels[0])):
            if white_pixels[0][i] == 400:# y축이 450인 픽셀만 추출
                
                if l_target_pixel+60 >white_pixels[1][i] > l_target_pixel-60:
                    l_target_pixel_2s.append(white_pixels[1][i])
                    
            if white_pixels[0][i] == 350:# y축이 430인 픽셀만 추출
                if l_target_pixel+60>white_pixels[1][i] > l_target_pixel-120:
                    l_target_pixel_3s.append(white_pixels[1][i])
                    
        
            if white_pixels[0][i] == 300:# y축이 430인 픽셀만 추출
                if l_target_pixel+100 >white_pixels[1][i] > l_target_pixel-180:
                    l_target_pixel_4s.append(white_pixels[1][i])
    else:
        for i in range(len(white_pixels[0])):
            if white_pixels[0][i] == 400:# y축이 450인 픽셀만 추출
                
                if prev_target_pixel_2+20 >white_pixels[1][i] > prev_target_pixel_2-20:
                    l_target_pixel_2s.append(white_pixels[1][i])
                    
            if white_pixels[0][i] == 350:# y축이 430인 픽셀만 추출
                if prev_target_pixel_3+20 >white_pixels[1][i] > prev_target_pixel_3-20:
                    l_target_pixel_3s.append(white_pixels[1][i])
                    
        
            if white_pixels[0][i] == 300:# y축이 430인 픽셀만 추출
                if prev_target_pixel_4+20 >white_pixels[1][i] > prev_target_pixel_4-20:
                    l_target_pixel_4s.append(white_pixels[1][i])
    
    for i in range(len(l_target_pixel_2s)):
        
        if i == len(l_target_pixel_2s)-1:
            if temp_target == []:
                target_pixel_2 = prev_target_pixel_2
                break
            pixel_difference = abs(temp_target[0] - temp_target[-1])
            
            if 25>pixel_difference > 7:
                
                l_target_pixel_2 = temp_target[-1]
                break
            else:
                temp_target = []
            break

        if abs(l_target_pixel_2s[i] - l_target_pixel_2s[i+1])<4:
            temp_target.append(l_target_pixel_2s[i])
        else:
            if temp_target == []:
                continue
            temp_target.append(l_target_pixel_2s[i])
            pixel_difference = abs(temp_target[0] - temp_target[-1])
            if 25>pixel_difference > 7:
                l_target_pixel_2 = temp_target[-1]
                break
            elif pixel_difference > 35:
                l_target_pixel_2 = temp_target[-1]
                break
            else:
                temp_target = []
    temp_target = []
    for i in range(len(l_target_pixel_3s)):
        
        if i == len(l_target_pixel_3s)-1:
            if temp_target == []:
                target_pixel_3 = prev_target_pixel_3
                break
            pixel_difference = abs(temp_target[0] - temp_target[-1])
            if 20>pixel_difference > 7:
                
                l_target_pixel_3 = temp_target[-1]
                break
            else:
                temp_target = []
            break
        if abs(l_target_pixel_3s[i] - l_target_pixel_3s[i+1])<4:
            temp_target.append(l_target_pixel_3s[i])
        else:
            if temp_target == []:
                continue
            temp_target.append(l_target_pixel_3s[i])
            pixel_difference = abs(temp_target[0] - temp_target[-1])
            if 20>pixel_difference > 7:
                l_target_pixel_3 = temp_target[-1]
                break
            elif pixel_difference > 35:
                l_target_pixel_3 = temp_target[-1]
                break
            else:
                temp_target = []
    temp_target = []
    for i in range(len(l_target_pixel_4s)):
        
        if i == len(l_target_pixel_4s)-1:
            if temp_target == []:
                target_pixel_4 = prev_target_pixel_4
                break
            pixel_difference = abs(temp_target[0] - temp_target[-1])
            if 20>pixel_difference > 7:
                
                l_target_pixel_4 = temp_target[-1]
                break
            else:
                temp_target = []
            break
        if abs(l_target_pixel_4s[i] - l_target_pixel_4s[i+1])<4:
            temp_target.append(l_target_pixel_4s[i])
        else:
            if temp_target == []:
                continue
            temp_target.append(l_target_pixel_4s[i])
            pixel_difference = abs(temp_target[0] - temp_target[-1])
            if 20>pixel_difference > 7:
                l_target_pixel_4 = temp_target[-1]
                break
            elif pixel_difference > 40:
                l_target_pixel_4 = temp_target[-1]
                break
            else:
                temp_target = []
    temp_target = []    

    # 첫 좌표를 잡고난 후에 진행
   
   
    
   

    target_pixel = [l_target_pixel,450]
    target_pixel_2 = [l_target_pixel_2,400]
    target_pixel_3 = [l_target_pixel_3,350]
    target_pixel_4 = [l_target_pixel_4,300 ]
    target_pixel = np.array(target_pixel)
    target_pixel_2 = np.array(target_pixel_2)
    target_pixel_3 = np.array(target_pixel_3)
    target_pixel_4 = np.array(target_pixel_4)
    
    #print(target_pixel, target_pixel_2, target_pixel_3, target_pixel_4)
    
    
    prev_target_pixel = l_target_pixel
    prev_target_pixel_2 = l_target_pixel_2
    prev_target_pixel_3 = l_target_pixel_3
    prev_target_pixel_4 = l_target_pixel_4
    
    reference_400 = l_target_pixel - 23
    reference_350 = l_target_pixel - 50
    reference_300 = l_target_pixel - 70
    
    
    middle_point[0] = target_pixel[0]-230
    middle_point[1] = target_pixel[1]
    car_middle_point = np.array([280, 450])

    rgb_mask = cv2.cvtColor(rgb_mask, cv2.COLOR_GRAY2BGR)

    cv2.circle(rgb_mask, (target_pixel), 5, red, -1)
    cv2.circle(rgb_mask, (target_pixel_2), 5, red, -1)  
    cv2.circle(rgb_mask, (target_pixel_3), 5, red, -1)
    cv2.circle(rgb_mask, (target_pixel_4), 5, red, -1)        
    # cv2.circle(edges2, (r_target_pixel), 5, red, -1)
    # cv2.circle(edges2, (r_target_pixel_2), 5, red, -1)  
    # cv2.circle(edges2, (r_target_pixel_3), 5, red, -1)
    # cv2.circle(edges2, (r_target_pixel_4), 5, red, -1)  
    cv2.line(rgb_mask, (target_pixel),(reference_300,300), blue, 3)
    cv2.circle(rgb_mask, car_middle_point, 5, red, -1)
    cv2.circle(rgb_mask, middle_point, 5, blue, -1)
    cv2.line(rgb_mask, (309, 479), (325, 187), blue, 3)
 
      
    cv2.imshow('image', image)   

    mp4_result.write(rgb_mask)
   
    if cv2.waitKey(1) == ord('q'):
        break
    start += 1
    reference_line = np.array(([309, 479], [317, 333]))
    reference_line = reference_line.reshape(2,2)
    data = [ l_target_pixel_2 - reference_400, l_target_pixel_3 - reference_350, l_target_pixel_4 - reference_300]
    print(data)
    train_data.append(data)
    if -10<=sum(data) <=10:
        speed = 150
        coor = 460
        coor = coor - (middle_point[0] - car_middle_point[0])/2
    else:
        if middle_point[0] - car_middle_point[0] > 0:
                coor = 460
                speed = 100
                coor = coor - (middle_point[0] - car_middle_point[0])/2
        elif middle_point[0] - car_middle_point[0] < 0:    
            coor = 460
            speed = 100
            coor = coor - (middle_point[0] - car_middle_point[0])/2
    
        
    # elif sum(data) > 10:
    #     speed = 50
    #     coor = 460 - sum(data)/4
    # elif sum(data) < -10:
    #     speed = 50
    #     coor = 460 - sum(data)/4
    coor = int(coor/4)
    speed = int(speed)
    print("coor")
    print(coor)
    print("speed")
    print(speed)
    #data = np.array(data)
    print("middle")
    print(middle_point[0] - car_middle_point[0])
    print(sum(data))
    ser.send_speed_coor(speed,coor)

    speed_car, coor_car = ser.get_data()

    cv2.putText(rgb_mask,"speed:" + str(speed_car) +"coor:"+ str(coor_car), (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('bird_view', rgb_mask)  
    
    # result = model(data).to(device)
    # result = result.tolist()
    # results.append(result)
    time2 = time.time()
    

train_data = np.array(train_data)
# results = np.array(results)

# results = results.reshape(-1,1)

#np.save("full_course_train_data_final_by_full_course_final.npy", train_data)
# np.save("train_data.npy", train_data)
# np.savetxt('result.csv',results,delimiter=",")
# np.save("result.npy", results)
# 작업 완료 후 해제
cap.release()

mp4_result.release()
cv2.destroyAllWindows()
