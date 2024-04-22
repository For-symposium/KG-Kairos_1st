import cv2

# Define a callback function that gets executed when a mouse event happens
def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # Left button click
        print(f"Mouse click at: (x={x}, y={y})")

# Initialize the video capture object
cap = cv2.VideoCapture(0)  # 0 is usually the default camera

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open video device.")
    exit()

# Set a window name
window_name = "Camera Feed"
cv2.namedWindow(window_name)

# Set the mouse callback function to the window
cv2.setMouseCallback(window_name, click_event)

try:
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        
        # Display the resulting frame
        cv2.imshow(window_name, frame)
        
        # Break the loop on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # When everything is done, release the capture and destroy all windows
    cap.release()
    cv2.destroyAllWindows()

