# Food detection by image processing for an robotic arm



https://github.com/user-attachments/assets/a2a7212c-d1ae-4683-a3da-b9d132b0de43


<p align="center">
<b>Dror Damari and Orly Behar</b>
<br>
<a href="mailto:Dror781@campus.technion.ac.il" target="_top">Dror781@campus.technion.ac.il</a>
</p>
<p align="center">
<a href="mailto:aorly@campus.technion.ac.il" target="_top">Aorly@campus.technion.ac.il</a>
</p>

------------

<a id="top"></a>
### Contents
1. [Introduction](#1.0)
2. [Building a Data set and model training](#2.0)
3. [Environment Setup](#3.0)
4. [Gaps](#4.0)

------------

   <a name="1.0"></a>
### 1. Introduction
This project focuses on developing a system for detecting food objects using a camera and sending the coordinates of the object's center to a robotic arm. The robotic arm then moves to the precise location of the object's center.

The project integrates the YOLO (You Only Look Once) model for real-time object detection and localization with robotic arm control, creating a seamless interaction between visual detection and physical movement. Additionally, the project includes calibration of the camera and workspace to ensure accurate detection and positioning.

Key features:

Object Detection with YOLO: Identify and locate food objects in the camera's field of view using a state-of-the-art object detection model.

Camera and Workspace Calibration: Ensure precise mapping between the camera's view and the robotic arm's operational area.

Coordinate Calculation: Determine the center coordinates of the detected objects.

- this includes a chessboard calibration to correct lens distortion
    
- pixel-to-millimeter conversion
    
- determining a fixed position in the robot's system for constructing a vector to the object
    
Robotic Arm Control: Send the calculated coordinates to the robotic arm.

Robotic movment: the robot arms moves towards the center of the object.

------------
<a name="2.0"></a>
<!--<div style="text-align:left;">
  <span style="font-size: 1.4em; margin-top: 0.83em; margin-bottom: 0.83em; margin-left: 0; margin-right: 0; font-weight: bold;"> 2. Environment Setup</span><span style="float:right;"><a href="#top">Back to Top</a></span>
</div>-->
### 2. Building a Data set and model training
To build the system for detecting different types of food, we first needed to create an image dataset for training the model. To tailor the dataset specifically to our project, we built it from scratch.

The types of food we aim to detect are: salmon fillet, chicken breast, yellow cheese, and steak. For each category, we captured a large number of images. To ensure effective training of our model, the images were taken from various angles, under different lighting conditions, and at different distances.

We uploaded all the images to the Roboflow platform. On this platform, we created our project, annotated the desired object in each image, and classified it according to its respective category.

![image](https://github.com/user-attachments/assets/87578e50-b324-4bdc-9743-d41d7607721a)

After building a sufficiently large dataset of approximately 200 images per object, we trained the YOLO model and evaluated its accuracy metrics.

We chose to use the YOLOv8 model for our project, a reliable model that works efficiently. It is a fast and accurate model that processes the image only once. These features make it a suitable model for object detection in the food domain, which is why we selected it.

The model is pre-built; we input the labeled image dataset according to the different objects. Then, we train the model on this dataset multiple times to improve its object detection accuracy. We evaluate the model’s accuracy using performance metrics.

Since our lab contains dummy objects representing different food items—salmon, steak, chicken breast, and yellow cheese—but these objects are not identical to the real food products on which our model was trained, we were required to create a new dataset with new images from the lab, featuring the dummy objects.

Since we rebuilt the dataset, we chose to focus on only two objects: yellow cheese and steak. We retrained the model on this new dataset. The model works and detects steak and yellow cheese, but its accuracy is not high. Therefore, we need to expand the image dataset from the lab to improve the accuracy and detection capabilities of our model.

------------
<a name="3.0"></a>
<!--<div style="text-align:left;">
<span style="font-size: 1.4em; margin-top: 0.83em; margin-bottom: 0.83em; margin-left: 0; margin-right: 0; font-weight: bold;">3. Theoretical Background</span><span style="float:right;"><a href="#top">Back to Top</a></span>
</div>-->
### 3. Environment Setup
Now that the model is trained on our new dataset, we need to adapt it to our lab and robotic arm. The robotic arm is connected to a rectangular table, and to align our object detection model with the lab setup, three steps are required. First, we will calibrate the camera, accounting for lens distortion. Then, we will perform pixel-to-meter calibration, and finally, we will identify a fixed point in the image whose location relative to the robot’s coordinate system is constant and unaffected by changes in the camera’s or object’s position.

Once the fixed point is identified, its position in the robot’s system is known and constant. Additionally, through a detection algorithm, the position of this point is also recognized in the camera system. By constructing a vector between this fixed point and the center of the detected object from our model, we can determine the object’s location relative to the fixed point in the camera system. By converting pixels to millimeters, we can create a vector between the object’s center and the robot’s base using vector addition, allowing the robotic arm to reach the object.

### Chessboard calibration to correct lens distortion

![image](https://github.com/user-attachments/assets/df2ee7d6-a681-40e4-80a9-5b3bc410b5bb)

Camera calibration using a chessboard is a common technique in image processing, aimed at calculating the camera's calibration parameters, including lens characteristics and distortion.

How does calibration with a chessboard work? (Part 1: "Setup Environment" code)

A chessboard is an aid tool with black-and-white squares arranged in a grid pattern. The camera can detect reference points in the image due to the distinct corners between the squares.

Main Steps:

## Prepare the Chessboard:

1. Use a chessboard with a known grid size, for example the file "Checkeboard 6x4"
Note: the size of the board refers to the inner corners of the checkeboard. 
2. update the size of your checkeboard at the "setup enviroment" code part 1.
## Capture Images of the Chessboard:

3. Capture around 10 images of the chessboard from various angles in the lab environment.

note: Ensure the entire chessboard is visible in each image.
exampels:
![WhatsApp Image 2025-01-13 at 17 09 47](https://github.com/user-attachments/assets/4f7bb41f-3869-4d7b-84aa-44d9c117603a)
![WhatsApp Image 2025-01-13 at 17 09 47 (1)](https://github.com/user-attachments/assets/a9c3bf3f-6d3a-492d-95df-cef26b29fd42)


4. Save the images in a folder and update the code to point to this folder (only to the folder at the "setup enviroment" code part 1).
   
## Detect Chessboard Corners in the Images:

The algorithm automatically detects the corners of the squares on the chessboard.

## Calculate Calibration Parameters:

The algorithm compares the location of the chessboard points as they appear in the image (2D) with their known positions in space (3D).

These equations are used to compute the camera’s intrinsic matrix, extrinsic matrix, and distortion coefficients.

After the camera is calibrated, we can use the calibration parameters to correct distortion in the images.

5. update the folder path for saving the images after the correction in prat 2 at the "setup enviroment" code.

![image](https://github.com/user-attachments/assets/0e5eb656-fde5-4528-b70d-ff37c724b0d0)

### Pixel-to-millimeter conversion
![image](https://github.com/user-attachments/assets/03458775-4103-4c63-8906-fc26ab7e6c30)

The code is interactive. When running the code, an image is randomly selected from the chessboard calibration folder. The selected image opens, and the user is required to mark two points whose distance is known, for example, the length/width of the table. After marking the two points, the user must input the distance in millimeters. Using this data, the code performs the conversion from pixels to millimeters.

The purpose of this calibration is to enable the translation of the known point's position in the camera system (represented in pixels) to a position in the robot's system (in millimeters).

It is very important that this step is done after correcting for lens distortion to avoid errors caused by image distortion.

### Determining a fixed position in the robot's system for constructing a vector to the object

We chose to find the fixed point by detecting the corner of the table. To achieve this, we placed a purple-colored object at the edge of the table. When running the code, the system captures an image of the table, marks the purple object, and returns the center of the marked object to the user.

In general, for each image, each pixel contains information about the color it represents in a specific color space. For example, RGB is the basic color space representing red, green, and blue, while HSV represents color saturation and brightness. The image, which is automatically captured in the RGB space, is converted to the HSV space for better detection, as this space is more robust for color detection in images. Each color is characterized by a vector of numbers within a certain range, so each range represents a specific color. For example, the red color is characterized by the number range:
[0, 100, 100], [10, 255, 255].

The color detection code scans all the pixels in the image and identifies those that match the predefined number range, in our case, purple. After identifying the matching pixels, the image is converted to shades of black and white, where the pixels of the desired color (purple) are represented in white, and the rest are converted to black. The white color is represented by the number 255, and black by the number 0. Finally, the code marks the white area and calculates the geometric center of mass of the resulting contour. This gives us the contour around the desired purple object and its center of mass. Additionally, the code prints the pixel location of the center of mass so we can determine the fixed point's location in the system and convert it from pixels to millimeters.

An advantage of this method is that it allows us to select the color we wish to detect. We chose purple because there are no purple shades in parts of the system, the robot, the table, or the lab floor, so there is no risk of interference that could cause errors in detecting the table corner. Similarly, other colors can be chosen.

![image](https://github.com/user-attachments/assets/7000de87-374c-414d-a849-68c3d8997eaf)
![image](https://github.com/user-attachments/assets/4dcb38f7-d8f9-49ac-98ed-785d5ac151f3)


When running the code, the user needs to input the desired image in which they want to detect the purple object. If, due to poor lighting, the object is not detected, the user can manually edit the image by marking a known point and drawing a circle in the required color.
In order to start the object detection process, it is necessary to complete these three "calibration" steps because the camera's position is not fixed, and the camera parameters need to be initialized.

### Building the vector from the robot base to the center of the object
So why do we need the table corner? The robot’s base position, which also serves as the origin of the robot's coordinate system, is fixed on the table. In order to provide the robot with the most accurate object location, we need to go through a fixed point that does not change relative to the robot's base, as represented in the image. The distance between the table corner and the robot system is constant and known. Additionally, by using the code to find the table corner, we can determine its position in the camera system in pixels.

Our object detection model provides us with information about the object's center point in the camera system, meaning in pixels. By using the position of the table corner, we construct the vector between the object's center and the table corner in the camera system, convert this vector to the world coordinate system, and through vector addition, we obtain the object’s center position relative to the robot system.

![image](https://github.com/user-attachments/assets/8f77a73c-9e78-4dfd-af39-6c7e70b91681)

Now we will build the fixed vector from the table corner to the center of the robot's base. We identified this point based on the maximum distance the robot can reach and recorded the data according to the robot's coordinate system.

Let’s define the location of the fixed point relative to the robot’s base system as follows:
\
$\overline{BC} = (x_{\text{const}}, y_{\text{const}})$
(Fixed vector from robot base to fixed point)


Next, let’s define the location of the corner in pixels as:

$\{P_{corner}} = (x_{\text{c,pix}}, y_{\text{c,pix}})$


This fixed point is represented in pixels, based on the detection of the purple object in a known position.

We will define the object center in pixels, which we receive from the object detection model as:

$P_{\text{object,pix}} = (x_{\text{obj,pix}}, y_{\text{obj,pix}})$


Now, we will use the conversion factor from pixels to millimeters, which we obtained from size calibration. This factor represents the ratio between pixels and millimeters, and we will denote it as \( \alpha \).

Now, we will construct the vector between the fixed point on the table and the object’s center:

$\overline{OC} = (x_{\text{obj,pix}}- x_{\text{c,pix}}, y_{\text{obj,pix}} - y_{\text{c,pix}})$


We obtain the vector in pixels, and now we multiply it by the conversion factor:

$\overline{OC_{\text{mm}}}= (x_{\text{obj,pix}}- x_{\text{c,pix}}, y_{\text{obj,pix}} - y_{\text{c,pix}})\cdot \alpha$




$\overline{OB_{\text{mm}}} = (x_{\text{const}} - (x_{\text{obj,pix}}- x_{\text{c,pix}}) \cdot \alpha  ,  y_{\text{const}} + (y_{\text{obj,pix}} - y_{\text{c,pix}}) \cdot \alpha )$


Since the coordinate systems of the robot and the camera do not align perfectly, we note that the X-axis of the camera aligns with the X-axis of the robot base, but the Y-axes are inverted. Therefore, the signs for the Y-axis components are reversed.

![image](https://github.com/user-attachments/assets/eb60cb6e-aa33-4f5b-8465-38f53b626b3a)

This is an image from the robot's operation and its arrival at the center of the object identified by the model, with its position obtained through vector calculation, which was input into the robot's operating system.


------------

<a name="4.0"></a>
<!--<div style="text-align:left;">
<span style="font-size: 1.4em; margin-top: 0.83em; margin-bottom: 0.83em; margin-left: 0; margin-right: 0; font-weight: bold;">3. Testing and Review</span><span style="float:right;"><a href="#top">Back to Top</a></span>
</div>-->
### 4. Gaps
There are several gaps that need to be addressed for system improvement.

1. Expanding the image annotation database from images taken in the lab, from the appropriate lab camera, considering the distance from the object and the image quality as it exists in the lab. Additionally, it is preferable to build this database based on images of dummy objects since they are not identical to real food items. Expanding the database and training the model on a larger dataset will improve the model's recognition accuracy.
2. Due to a problem we were unable to resolve during the robot's operation in the lab, the calculation of the object center and the robot's arrival at the center is accurate only in the middle of the lab table (the right side of the table). As the object is moved further left for recognition, the error in the robot's arrival at the center of the object increases, particularly along the X-axis. This error may stem from changes in lighting or disturbances that were not accounted for.
3. Camera fixation - If the ceiling camera can be fixed in place without movement, the calibration steps can be performed less frequently, thus making the system more efficient.
