from ultralytics import YOLO
import cv2

# Load the YOLO model
model = YOLO("your_YOLO_model.pt")  # Replace with your model path

# Start video capture (use 0 for the default camera)
cap = cv2.VideoCapture(1)

# Initialize a list to store the centers of bounding boxes
centers = []

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    # Capture a frame from the camera
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break

    # Run YOLO detection on the frame
    results = model(frame)

    # Process each detection
    for detection in results[0].boxes.data:
        # Extract bounding box coordinates
        x_min, y_min, x_max, y_max, confidence, class_id = detection.cpu().numpy()

        # Calculate the center of the bounding box
        x_center = int((x_min + x_max) / 2)
        y_center = int((y_min + y_max) / 2)

        # Save the center coordinates
        centers.append((x_center, y_center))

        # Draw the bounding box and center point on the frame
        cv2.rectangle(frame, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 255, 0), 2)
        cv2.circle(frame, (x_center, y_center), 5, (0, 0, 255), -1)  # Red dot for center
        cv2.putText(frame, f"({x_center}, {y_center})", (x_center + 10, y_center - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

    # Display the frame with detections
    cv2.imshow("Real-Time YOLO Detection", frame)

    # Break the loop if the user presses 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()