import os
import json

import torch
from torchvision import models, transforms
from torch import nn
from PIL import Image


# ==========================================
# PATHS
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "tomato_disease_model.pth"
)

CLASS_NAMES_PATH = os.path.join(
    BASE_DIR,
    "models",
    "class_names.json"
)

# Test images are inside PlantVillage
TEST_IMAGE_DIR = os.path.join(
    BASE_DIR,
    "data",
    "PlantVillage",
    "test_images"
)


# ==========================================
# DEVICE
# ==========================================

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("Device:", device)


# ==========================================
# LOAD CLASS NAMES
# ==========================================

with open(
    CLASS_NAMES_PATH,
    "r",
    encoding="utf-8"
) as file:

    class_names = json.load(file)

print("\nClasses:")

for index, class_name in enumerate(class_names):
    print(index, "->", class_name)


# ==========================================
# LOAD MODEL
# ==========================================

print("\nLoading model...")

model = models.mobilenet_v2(weights=None)

number_of_classes = len(class_names)

model.classifier[1] = nn.Linear(
    model.classifier[1].in_features,
    number_of_classes
)

model.load_state_dict(
    torch.load(
        MODEL_PATH,
        map_location=device
    )
)

model = model.to(device)

model.eval()

print("Model loaded successfully.")


# ==========================================
# IMAGE TRANSFORMATION
# ==========================================

transform = transforms.Compose([
    transforms.Resize((224, 224)),

    transforms.ToTensor(),

    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


# ==========================================
# FIND TEST IMAGE
# ==========================================

supported_extensions = (
    ".jpg",
    ".jpeg",
    ".png"
)

image_files = [
    file
    for file in os.listdir(TEST_IMAGE_DIR)
    if file.lower().endswith(supported_extensions)
]


if len(image_files) == 0:

    print("\nERROR: No image found.")

    print(
        "Put an image inside:"
    )

    print(TEST_IMAGE_DIR)

    exit()


# Use the first image found
IMAGE_PATH = os.path.join(
    TEST_IMAGE_DIR,
    image_files[0]
)


# ==========================================
# LOAD IMAGE
# ==========================================

print("\n====================================")
print("TEST IMAGE")
print("====================================")

print("Image:", image_files[0])

image = Image.open(
    IMAGE_PATH
).convert("RGB")


# ==========================================
# PREPROCESS IMAGE
# ==========================================

image_tensor = transform(image)

image_tensor = image_tensor.unsqueeze(0)

image_tensor = image_tensor.to(device)


# ==========================================
# PREDICTION
# ==========================================

with torch.no_grad():

    outputs = model(image_tensor)

    probabilities = torch.softmax(
        outputs,
        dim=1
    )

    confidence, predicted_class = torch.max(
        probabilities,
        1
    )


# ==========================================
# RESULT
# ==========================================

predicted_index = predicted_class.item()

predicted_disease = class_names[
    predicted_index
]

confidence_value = confidence.item() * 100


# ==========================================
# DISPLAY RESULT
# ==========================================

print("\n====================================")
print("PREDICTION RESULT")
print("====================================")

print("Crop: Tomato")

print(
    f"Disease: {predicted_disease}"
)

print(
    f"Confidence: {confidence_value:.2f}%"
)

print("====================================")