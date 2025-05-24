import os
import numpy as np
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import json

# --- Load Model ---
model = tf.keras.models.load_model("plantoscope_model.h5")

# print the model summary
model.summary()

# --- Load Class Index Mapping ---
with open("class_indices.json") as f:
    class_indices = json.load(f)

# Invert the class index mapping
index_to_class = {int(v): k for v, k in class_indices.items()}

# --- Image Data Generator for Test Images ---
img_size = (224, 224)
batch_size = 32

test_datagen = ImageDataGenerator(rescale=1./255)

test_generator = test_datagen.flow_from_directory(
    "./dataset",  # path to your dataset folder
    target_size=img_size,
    batch_size=batch_size,
    class_mode='categorical',
    shuffle=False
)

# --- Predictions ---
y_true = test_generator.classes
y_pred_probs = model.predict(test_generator, verbose=1)
y_pred = np.argmax(y_pred_probs, axis=1)

# --- Evaluation Metrics ---
print("\nClassification Report:")
print(classification_report(y_true, y_pred, target_names=test_generator.class_indices.keys()))

print("\nConfusion Matrix:")
print(confusion_matrix(y_true, y_pred))

# Classification Report:
#                                                     precision    recall  f1-score   support

#                                 Apple___Apple_scab       0.91      0.93      0.92       630
#                                  Apple___Black_rot       0.97      0.97      0.97       621
#                           Apple___Cedar_apple_rust       0.95      0.93      0.94       275
#                                    Apple___healthy       0.97      0.94      0.95      1645
#                                Blueberry___healthy       0.87      1.00      0.93      1502
#           Cherry_(including_sour)___Powdery_mildew       1.00      0.96      0.98      1052
#                  Cherry_(including_sour)___healthy       1.00      0.75      0.86       854
# Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot       0.86      0.89      0.88       513
#                        Corn_(maize)___Common_rust_       1.00      0.99      1.00      1192
#                Corn_(maize)___Northern_Leaf_Blight       0.96      0.93      0.94       985
#                             Corn_(maize)___healthy       0.99      0.99      0.99      1162
#                                  Grape___Black_rot       0.93      0.99      0.96      1180
#                       Grape___Esca_(Black_Measles)       0.95      0.98      0.96      1383
#         Grape___Leaf_blight_(Isariopsis_Leaf_Spot)       1.00      0.96      0.97      1076
#                                    Grape___healthy       0.98      0.96      0.97       423
#           Orange___Haunglongbing_(Citrus_greening)       1.00      0.98      0.99      5507
#                             Peach___Bacterial_spot       0.96      0.95      0.96      2297
#                                    Peach___healthy       0.98      0.88      0.93       360
#                      Pepper,_bell___Bacterial_spot       0.94      0.90      0.92       997
#                             Pepper,_bell___healthy       0.88      0.98      0.93      1478
#                              Potato___Early_blight       0.96      0.98      0.97      1000
#                               Potato___Late_blight       0.98      0.90      0.94      1000
#                                   Potato___healthy       0.97      0.82      0.89       152
#                                Raspberry___healthy       0.97      0.97      0.97       371
#                                  Soybean___healthy       0.95      0.99      0.97      5090
#                            Squash___Powdery_mildew       0.96      1.00      0.98      1835
#                           Strawberry___Leaf_scorch       0.98      0.95      0.97      1109
#                               Strawberry___healthy       0.99      0.98      0.98       456
#                            Tomato___Bacterial_spot       0.95      0.97      0.96      2127
#                              Tomato___Early_blight       0.94      0.84      0.89      1000
#                               Tomato___Late_blight       0.91      0.95      0.93      1909
#                                 Tomato___Leaf_Mold       0.97      0.92      0.94       952
#                        Tomato___Septoria_leaf_spot       0.96      0.87      0.91      1771
#      Tomato___Spider_mites Two-spotted_spider_mite       0.97      0.96      0.96      1676
#                               Tomato___Target_Spot       0.97      0.90      0.93      1404
#             Tomato___Tomato_Yellow_Leaf_Curl_Virus       0.96      1.00      0.98      5357
#                       Tomato___Tomato_mosaic_virus       0.95      0.97      0.96       373
#                                   Tomato___healthy       1.00      0.98      0.99      1591

#                                           accuracy                           0.96     54305
#                                          macro avg       0.96      0.94      0.95     54305
#                                       weighted avg       0.96      0.96      0.96     54305


# Confusion Matrix:
# [[ 589    1    1 ...    1    0    0]
#  [   0  605    0 ...    0    0    0]
#  [   1    0  256 ...    8    0    0]
#  ...
#  [   0    0    0 ... 5335    0    0]
#  [   0    0    0 ...    0  362    0]
#  [   4    0    0 ...    0    0 1557]]

# import os
# import json
# import numpy as np
# import tensorflow as tf
# import matplotlib.pyplot as plt
# import seaborn as sns
# from sklearn.metrics import classification_report, confusion_matrix
# from tensorflow.keras.preprocessing.image import ImageDataGenerator

# # --- Load Model ---
# model = tf.keras.models.load_model("plantoscope_model.h5")
# model.summary()

# # --- Load Class Index Mapping ---
# with open("class_indices.json") as f:
#     class_indices = json.load(f)

# # Invert class index mapping: index (int) -> class label (str)
# index_to_class = {int(k): v for k, v in class_indices.items()}

# # --- Data Generator ---
# img_size = (224, 224)
# batch_size = 32

# test_datagen = ImageDataGenerator(rescale=1./255)

# test_generator = test_datagen.flow_from_directory(
#     "./dataset",  # path to your dataset folder
#     target_size=img_size,
#     batch_size=batch_size,
#     class_mode='categorical',
#     shuffle=False
# )

# # --- Predictions ---
# y_true = test_generator.classes
# y_pred_probs = model.predict(test_generator, verbose=1)
# y_pred = np.argmax(y_pred_probs, axis=1)

# # --- Classification Report ---
# print("\nClassification Report:")
# print(classification_report(
#     y_true,
#     y_pred,
#     target_names=[index_to_class[i] for i in range(len(index_to_class))]
# ))

# # --- Confusion Matrix ---
# cm = confusion_matrix(y_true, y_pred)
# class_labels = [index_to_class[i] for i in range(len(index_to_class))]

# # --- Plot Confusion Matrix ---
# plt.figure(figsize=(24, 22))
# sns.heatmap(cm, annot=False, fmt='d', xticklabels=class_labels, yticklabels=class_labels, cmap='YlGnBu')
# plt.xlabel('Predicted')
# plt.ylabel('Actual')
# plt.title('Confusion Matrix - PlantoScope .h5 Model')
# plt.xticks(rotation=90)
# plt.yticks(rotation=0)
# plt.tight_layout()
# plt.show()