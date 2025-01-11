!pip install ultralytics
from ultralytics import YOLO
from google.colab import drive
from PIL import Image
import matplotlib.pyplot as plt
import multiprocessing as mp
#mp.set_start_method('spawn')
# Set multiprocessing start method if required
if mp.get_start_method(allow_none=True) != 'spawn':
    mp.set_start_method('spawn')

drive.mount('/content/drive')
!unzip "/content/drive/My Drive/Colab Notebooks/THE-ROBOFLOW-FILE-AFTER-ANNOTATINS.zip" -d /content/dataset
data_path = '/content/dataset/data.yaml'  # Path to your dataset YAML file
model_path = 'yolov8n.pt'  # You can use yolov8n, yolov8s, yolov8m, yolov8l, or yolov8x

model = YOLO(model_path)

# Training the model
model.train(
    data=data_path,
    epochs=50,
    imgsz=640,
    batch=16,
    workers=2
)

# Validation
model.val()

# Prediction
results = model.predict(source='/content/dataset/valid/images')
for result in results:
    result.show()

# Save the model
model.save('/content/drive/MyDrive/ENTER-NAME-FOR-TRAINED-MODEL.pt')

# YOLOv8 automatically saves training graphs; let's display them
!ls runs/detect/train  # List files in the training directory to find the plot
img = Image.open('runs/detect/train/results.png')  # Load the saved plot using PIL
plt.imshow(img)
plt.axis('off')  # Hide axis
plt.show()
