from ultralytics import YOLO
import cv2

# Load the YOLOv8 model
model = YOLO(r'PATH\TO\YOLO\MODEL.pt')  
# Load the image
image_path = r"PATH\TO\IMAGE.jpg"  # Replace with the path to your image
image = cv2.imread(image_path)

# Run the YOLO model on the image
results = model(image)

# Extract results and visualize
annotated_image = results[0].plot()  # Visualize the detections on the image

# Display the image with detections
cv2.namedWindow('YOLOv8 Detection', cv2.WINDOW_NORMAL)
cv2.imshow("YOLOv8 Detection", annotated_image)
cv2.waitKey(0)  # Wait until a key is pressed
cv2.destroyAllWindows()

## Save the result (optional)
#output_path = "path/to/save/detected_image.jpg"  # Replace with the desired output path
#cv2.imwrite(output_path, annotated_image)

# Iterate through detections
for detection in results[0].boxes.data:
    # Extract bounding box coordinates
    x_min, y_min, x_max, y_max, confidence, class_id = detection.cpu().numpy()
    
    # Calculate the center of the bounding box
    x_center = round((x_min + x_max) / 2)
    y_center = round((y_min + y_max) / 2)

    # Print the center coordinates
    print(f"Object detected: Class ID {int(class_id)}, Confidence {confidence:.2f}")
    print(f"Bounding Box Center: ({x_center:.2f}, {y_center:.2f})")