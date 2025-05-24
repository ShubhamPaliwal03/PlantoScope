import tensorflow as tf

model = tf.keras.models.load_model("./plantoscope_model.h5")
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [] # no quantization
tflite_model = converter.convert()

# Save the compressed model
with open("model.tflite", "wb") as f:
    f.write(tflite_model)