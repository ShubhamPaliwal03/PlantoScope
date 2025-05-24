import os
import numpy as np
from PIL import Image
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix
from tqdm import tqdm

# Paths
model_path = './plantoscope_model.tflite'
dataset_path = './dataset'  # Update this to the actual dataset folder path

# Load class indices (str: label_name)
import json
with open('class_indices.json') as f:
    class_indices = json.load(f)

# Invert the dictionary to get label_name -> index
label_to_index = {v: int(k) for k, v in class_indices.items()}
index_to_label = {int(k): v for k, v in class_indices.items()}

# Load the TFLite model
interpreter = tf.lite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Preprocessing function
def preprocess_image(img_path):
    img = Image.open(img_path).convert('RGB').resize((224, 224))
    img_array = np.array(img) / 255.0
    return np.expand_dims(img_array.astype(np.float32), axis=0)

# Collect data
y_true = []
y_pred = []

for folder in tqdm(os.listdir(dataset_path)):
    folder_path = os.path.join(dataset_path, folder)
    if not os.path.isdir(folder_path):
        continue
    true_label = label_to_index.get(folder, None)
    if true_label is None:
        continue  # Skip unknown folders

    for img_file in os.listdir(folder_path):
        img_path = os.path.join(folder_path, img_file)

        try:
            img = preprocess_image(img_path)

            interpreter.set_tensor(input_details[0]['index'], img)
            interpreter.invoke()

            output = interpreter.get_tensor(output_details[0]['index'])
            pred_label = np.argmax(output)

            y_true.append(true_label)
            y_pred.append(pred_label)
        except Exception as e:
            print(f"Skipping {img_path}: {e}")

# Evaluation Metrics
print("\nClassification Report:")
print(classification_report(y_true, y_pred, target_names=[index_to_label[i] for i in sorted(index_to_label)]))

print("\nConfusion Matrix:")
print(confusion_matrix(y_true, y_pred))