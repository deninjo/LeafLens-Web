"""
Django ML Engine
Everything here is loaded ONCE at startup (fast inference)
"""
import numpy as np
from PIL import Image
from django.conf import settings

# To skip ML loading during tests (and keep production behavior unchanged)
# and Guard heavy ML imports
if not getattr(settings, 'TESTING', False):
      import torch
      import clip
      from tensorflow.lite.python.interpreter import Interpreter

      # ---------------------------
      # Device for CLIP
      # ---------------------------
      device = "cuda" if torch.cuda.is_available() else "cpu"

      # ---------------------------
      # TFLite model
      # ---------------------------
      TFLITE_PATH = str(settings.BASE_DIR / 'ml/models/mobilenetv2_v1_44_0.996.tflite')
      classifier_interpreter = Interpreter(model_path=TFLITE_PATH)
      classifier_interpreter.allocate_tensors()

      # ---------------------------
      # CLIP model
      # ---------------------------
      clip_model, clip_preprocess = clip.load("ViT-B/32", device=device)
      maize_prompts = [
          "maize leaf",
          "maize plant leaf",
          "corn leaf",
          "maize crop leaf",
          "closeup of maize leaf",
          "maize disease leaf",
          "healthy maize leaf"
      ]
      text_tokens = clip.tokenize(maize_prompts).to(device)


# ---------------------------
# Class names
# ---------------------------
CLASSES = ['Blight', 'Common Rust', 'Gray Leaf Spot', 'Healthy']

# ---------------------------
# CLIP prefilter
# ---------------------------
def is_maize_clip(img_path, threshold=0.29):
    """Return True if image passes maize prefilter."""
    try:
        image_pil = Image.open(img_path).convert("RGB")
        image_tensor = clip_preprocess(image_pil).unsqueeze(0).to(device)

        with torch.no_grad():
            image_features = clip_model.encode_image(image_tensor)
            text_features = clip_model.encode_text(text_tokens)

            # Normalize
            image_features /= image_features.norm(dim=-1, keepdim=True)
            text_features /= text_features.norm(dim=-1, keepdim=True)

            similarity = (image_features @ text_features.T).squeeze(0)
            max_sim = similarity.max().item()

        return max_sim > threshold
    except Exception as e:
        print("CLIP error:", e)
        return False

# ---------------------------
# TFLite inference
# ---------------------------
"""Return predicted class and probabilities from TFLite model"""


def run_tflite_inference(img_path):
    """
    Perform classification and return predicted class and probabilities from TFLite model

    The preprocessing pipeline replicates exactly how images were prepared
    during model training to ensure consistent results.
    """
    # Import here to avoid circular imports
    from tensorflow.keras.preprocessing import image as keras_image


    # 1. Image Loading & Preprocessing
    # ---------------------------
    # Load image with same parameters used during training
    img = keras_image.load_img(img_path, target_size=(224, 224))

    # Convert to array and normalize to [0,1] range
    # This matches the training data preprocessing pipeline
    img_array = keras_image.img_to_array(img) / 255.0

    # Expand dimensions to create batch of size 1
    # Required format: (batch_size, height, width, channels)
    img_array_expanded = np.expand_dims(img_array, axis=0).astype(np.float32)


    # 2. Model Inference
    # ---------------------------
    # Get model input/output tensor indices
    input_index = classifier_interpreter.get_input_details()[0]['index']
    output_index = classifier_interpreter.get_output_details()[0]['index']

    # Set input tensor with preprocessed image
    classifier_interpreter.set_tensor(input_index, img_array_expanded)

    # Execute inference
    classifier_interpreter.invoke()

    # Retrieve model predictions
    # Output is a 2D array: [[class1_prob, class2_prob, ...]]
    output_data = classifier_interpreter.get_tensor(output_index)

    # Extract probabilities for the single image in batch
    probabilities = output_data[0]


    # 3. Result Interpretation
    # ---------------------------
    # Get index of highest probability class
    predicted_index = int(np.argmax(probabilities))

    # Map index to human-readable class name
    predicted_class = CLASSES[predicted_index]

    # Create dictionary with probabilities for all classes
    probabilities_dict = {
        CLASSES[i]: float(probabilities[i])
        for i in range(len(CLASSES))
    }

    return predicted_class, probabilities_dict