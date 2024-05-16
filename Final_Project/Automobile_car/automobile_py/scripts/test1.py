import cv2

def list_cameras():
    index = 0
    arr = []
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            break
        else:
            arr.append(index)
        cap.release()
        index += 1
    return arr

camera_indices = list_cameras()
print("Available camera indices: ", camera_indices)

# Check each camera index
for i in camera_indices:
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Camera {i} is working")
        cap.release()
    else:
        print(f"Camera {i} is not working")
