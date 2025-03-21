# -*- coding: utf-8 -*-
"""Brain Tumor Detection DL Project .ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/19ayPlAZYqycC2PC_HH8Wy43RrquhLGya
"""

!pip install ultralytics

from google.colab import drive
drive.mount('/content/drive')

!tar -xvf mri.tar

!yolo task=detect mode=train epochs=50, batch=32 plots=True model=yolov8n.pt data=/content/MRI-3/data.yaml

from ultralytics import YOLO

model_path = "/content/runs/detect/train2/weights/best.pt"
model = YOLO(model_path)

result = model(source = "/content/MRI-3/valid/images", conf = 0.25, save=True)

import glob
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

images = glob.glob("/content/runs/detect/predict/*.jpg")

images_to_display = images[:10]

fig, axes = plt.subplots(2,5, figsize=(20,10))

for i, ax in enumerate(axes.flat):
  if i < len(images_to_display):
    img = mpimg.imread(images_to_display[i])
    ax.imshow(img)
    ax.axis('off')
  else:
    ax.axis('off')
plt.tight_layout()
plt.show()

result = model.predict(source = "/content/MRI-3/valid/images/Tr-me_0880_jpg.rf.9c8db6c26c3658dc54dcd0e511f6fc95.jpg", imgsz = 640, conf = 0.25)
annotated_img = result[0].plot()
annotated_img[:, :, ::-1]

!pip install gradio

import gradio as gr
import cv2
import numpy as np

# Placeholder for the model (Ensure you load your actual model)
def predict(image):
    if image is None:
        return None, "Please upload a valid MRI scan."

    # Perform prediction
    result = model.predict(source=image, imgsz=640, conf=0.25)

    # Check if a tumor is detected
    if len(result[0].boxes) == 0:  # No bounding boxes → No tumor detected
        return image, "**No Tumor Detected**"

    # If tumor is detected, process and return annotated image
    annotated_img = result[0].plot()
    annotated_img = cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB)
    return annotated_img, "**Tumor Detected**"

# Custom CSS for better UI
def custom_css():
    return """
    body {background-color: #f8f9fa;}
    .gradio-container {max-width: 800px; margin: auto; border-radius: 15px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); padding: 20px; background:black;}
    .gradio-title {font-size: 28px; font-weight: bold; text-align: center; margin-bottom: 10px;}
    .gradio-description {text-align: center; color: #555; margin-bottom: 20px;}
    .result-text {font-size: 18px; font-weight: bold; text-align: center; color: #d9534f; margin-top: 10px;}
    """

# JavaScript to change the tab title
js_script = """
<script>
document.title = "Brain Tumor Detection App";
</script>
"""

# Define the Gradio interface with side-by-side layout
with gr.Blocks(css=custom_css()) as app:
    gr.Markdown("# 🧠 **Brain Tumor Detection App**")
    gr.Markdown("Upload an MRI scan for advanced AI-driven brain tumor detection.")

    with gr.Row():
        image_input = gr.Image(type="numpy", label="Upload Brain MRI Scan")
        image_output = gr.Image(type="numpy", label="Brain Tumor Detection Output")

    result_text = gr.Markdown("")  # This will be updated dynamically

    btn = gr.Button("Analyze")
    btn.click(predict, inputs=image_input, outputs=[image_output, result_text])

    # Inject JavaScript to change the tab title
    gr.HTML(js_script)

app.launch()
