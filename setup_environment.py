# Import required modules 
import cv2 
import numpy as np 
import glob 
import os
import random
## Setup environment 
# Part one checkboard clibration
folder_path = r'PATH\TO\THE\FOLDER\THAT\CONTAINS\THE\IMAGES\FOR\CHECKBOARD\CALIBRATION' # Replace the path to the FOLDER with the checkboard images
image_files = os.listdir(folder_path)
random_image = random.choice(image_files)
image_path = os.path.join(folder_path, random_image) # Takes a random image from the folder with the checkboard images

img = cv2.imread(image_path) 
 
# Define the dimensions of checkerboard 
CHECKERBOARD = (6, 4)

# Stop the iteration when specified 
# accuracy, epsilon, is reached or 
# specified number of iterations are completed. 
criteria = (cv2.TERM_CRITERIA_EPS +
            cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001) 

# Vector for 3D points 
threedpoints = [] 

# Vector for 2D points 
twodpoints = [] 

# 3D points real world coordinates 
objectp3d = np.zeros((1, CHECKERBOARD[0] 
                     * CHECKERBOARD[1], 
                     3), np.float32) 
objectp3d[0, :, :2] = np.mgrid[0:CHECKERBOARD[0], 
                              0:CHECKERBOARD[1]].T.reshape(-1, 2) 
prev_img_shape = None
 
# The path is to a folder that contain several images of a checkboard images in the lab.

temp = '\*.jpg'
images = glob.glob(folder_path+temp)

for filename in images: 
    image = cv2.imread(filename) 
    grayColor = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 

    # Find the chess board corners 
    ret, corners = cv2.findChessboardCorners( 
                    grayColor, CHECKERBOARD, 
                    cv2.CALIB_CB_ADAPTIVE_THRESH 
                    + cv2.CALIB_CB_FAST_CHECK +
                    cv2.CALIB_CB_NORMALIZE_IMAGE) 

    if ret == True: 
        threedpoints.append(objectp3d) 

        # Refining pixel coordinates 
        corners2 = cv2.cornerSubPix( 
            grayColor, corners, (11, 11), (-1, -1), criteria) 

        twodpoints.append(corners2) 

        # Draw and display the corners 
        image = cv2.drawChessboardCorners(image, 
                                          CHECKERBOARD, 
                                          corners2, ret) 

    # Make the display window resizable
    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.imshow('img', image) 
    cv2.waitKey(0) 

cv2.destroyAllWindows() 

h, w = image.shape[:2]



# Perform camera calibration by 
# passing the value of above found out 3D points (threedpoints) 
# and its corresponding pixel coordinates of the 
# detected corners (twodpoints) 
ret, matrix, distortion, r_vecs, t_vecs = cv2.calibrateCamera( 
	threedpoints, twodpoints, grayColor.shape[::-1], None, None) 

# Save the calibration result
np.savez('calibration_data_lab_cam.npz', camera_matrix=matrix, dist_coeffs=distortion)


#%% part 2 saving the undistored image. The image is being taken randomly from the folder with the checkboard images from part 1.
# Load the calibration data
calibration_data = np.load('calibration_data_lab_cam.npz')
camera_matrix = calibration_data['camera_matrix']
dist_coeffs = calibration_data['dist_coeffs']

# Load an image to undistort

h, w = img.shape[:2]
new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (w, h), 1, (w, h))

# Undistort the image
undistorted_img = cv2.undistort(img, camera_matrix, dist_coeffs, None, new_camera_matrix)

# Crop the image to the valid region
x, y, w, h = roi
undistorted_img = undistorted_img[y:y+h, x:x+w]
save_path = r'PATH-TO-YOUR-DESIRE-FOLDER\IMAGE.jpg' # Replace the location you want to save the undistored image
cv2.imwrite(save_path, undistorted_img)  

#%% part 3 finding the pixle/mm ratio 
# Global variables
points = []
image = None

def click_event(event, x, y, flags, param):
    """
    Mouse callback function to capture points when the user clicks on the image.
    """
    global points, image
    if event == cv2.EVENT_LBUTTONDOWN:
        # Store the clicked point
        points.append((x, y))
        cv2.circle(image, (x, y), 5, (0, 0, 255), -1)  # Draw a red dot at the clicked point
        cv2.imshow("Image", image)

        # If two points are selected, allow the ratio calculation
        if len(points) == 2:
            calculate_ratio()

def calculate_ratio():
    """
    Calculate and display the pixel-to-mm ratio based on user input.
    """
    global points, image
    # Calculate pixel distance between the two points
    pixel_distance = ((points[1][0] - points[0][0]) ** 2 + (points[1][1] - points[0][1]) ** 2) ** 0.5

    # Get real-world distance from the user
    real_world_distance = float(input("Enter the real-world distance between the two points (in mm): "))

    # Calculate pixel-to-mm ratio and invert it
    pixels_per_mm = pixel_distance / real_world_distance
    mm_per_pixel = 1 / pixels_per_mm
    print(f"\nPixel distance: {pixel_distance:.2f} pixels")
    print(f"Real-world distance: {real_world_distance:.2f} mm")
    print(f"Pixel-to-mm ratio (mm per pixel): {mm_per_pixel:.5f}")

    # Change the color of the dots to green
    for point in points:
        cv2.circle(image, point, 5, (0, 255, 0), -1)  # Draw a green dot at the selected points
    cv2.imshow("Image", image)

    # Reset points for another measurement
    points.clear()

def main():
    global image
    # Load the image
    image_path = save_path
    image = cv2.imread(image_path)

    if image is None:
        print("Failed to load image. Please check the path and try again.")
        return

    # Resize image if necessary
    max_dimension = 1500
    scale = min(max_dimension / max(image.shape[:2]), 1.0)
    image = cv2.resize(image, (int(image.shape[1] * scale), int(image.shape[0] * scale)))

    # Display the image
    cv2.imshow("Image", image)
    print("Click on two points in the image to measure the pixel distance.")

    # Set the mouse callback function
    cv2.setMouseCallback("Image", click_event)

    # Wait until the user closes the window
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()


#%% mark the boundris of a purple (or other color if desire) object and print its (x,y) in pixels
def detect_colored_corner(image_path, lower_color, upper_color):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Image not found.")
        return

    # Convert the image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Create a mask for the specified color range
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours by area in descending order and keep the largest contour
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    if not contours:
        print("No contours found.")
        return

    largest_contour = contours[0]

    # Calculate the center of the colored mark
    M = cv2.moments(largest_contour)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:
        cX, cY = 0, 0
    print(f"Center of the colored mark: ({cX}, {cY})")

    # Approximate the contour to a polygon to detect the corner
    epsilon = 0.02 * cv2.arcLength(largest_contour, True)
    approx = cv2.approxPolyDP(largest_contour, epsilon, True)

    # Draw the detected contour and corner points on the original image
    output = image.copy()
    cv2.drawContours(output, [largest_contour], -1, (0, 255, 0), 2)

    # Highlight corner points
    for point in approx:
        x, y = point.ravel()
        cv2.circle(output, (x, y), 5, (0, 0, 255), -1)

    # Highlight the center point
    cv2.circle(output, (cX, cY), 7, (255, 0, 0), -1)

    # Display the results
    # Resize the image to fit within a reasonable size if needed
    max_dimension = 1500
    scale = min(max_dimension / max(image.shape[:2]), 1.0)
    output = cv2.resize(output, (int(image.shape[1] * scale), int(image.shape[0] * scale)))
    
    cv2.imshow("Detected Colored Corner", output)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return cX, cY
# Example usage
image_path = r'IMAGE\WITH\PURPLE\OBJECT'  # Replace with the path to your image with a purple object
lower_purple = np.array([125, 50, 50])  # Adjust HSV range for purple
upper_purple = np.array([150, 255, 255])
[cX, cY] = detect_colored_corner(image_path, lower_purple, upper_purple)




