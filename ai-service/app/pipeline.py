import os
import sys
import json

# ==========================================
# ADD PROJECT ROOT TO PYTHON PATH
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(
    0,
    BASE_DIR
)


# ==========================================
# IMPORT LIBRARIES
# ==========================================

import torch
from torchvision import models, transforms
from torch import nn
from PIL import Image


# ==========================================
# IMPORT CROP-TO-CASH MODULES
# ==========================================

from notebooks.severity import estimate_severity
from notebooks.treatment import get_treatment
from notebooks.recovery import estimate_recovery
from notebooks.sale_readiness import calculate_sale_readiness


# ==========================================
# PATHS
# ==========================================

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


# ==========================================
# DEVICE
# ==========================================

device = torch.device(
    "cuda" if torch.cuda.is_available()
    else "cpu"
)

print("Using device:", device)


# ==========================================
# LOAD CLASS NAMES
# ==========================================

with open(
    CLASS_NAMES_PATH,
    "r",
    encoding="utf-8"
) as file:

    class_names = json.load(file)


# ==========================================
# LOAD MODEL
# ==========================================

model = models.mobilenet_v2(
    weights=None
)

number_of_classes = len(
    class_names
)

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


# ==========================================
# IMAGE TRANSFORMATION
# ==========================================

transform = transforms.Compose([

    transforms.Resize(
        (224, 224)
    ),

    transforms.ToTensor(),

    transforms.Normalize(
        mean=[
            0.485,
            0.456,
            0.406
        ],

        std=[
            0.229,
            0.224,
            0.225
        ]
    )
])


# ==========================================
# DISEASE PREDICTION
# ==========================================

def predict_disease(image_path):

    image = Image.open(
        image_path
    ).convert("RGB")

    image_tensor = transform(
        image
    )

    image_tensor = image_tensor.unsqueeze(
        0
    )

    image_tensor = image_tensor.to(
        device
    )

    with torch.no_grad():

        outputs = model(
            image_tensor
        )

        probabilities = torch.softmax(
            outputs,
            dim=1
        )

        confidence, predicted_class = torch.max(
            probabilities,
            1
        )

    predicted_index = (
        predicted_class.item()
    )

    disease = class_names[
        predicted_index
    ]

    confidence_value = (
        confidence.item()
    )

    return disease, confidence_value


# ==========================================
# COMPLETE CROP-TO-CASH PIPELINE
# ==========================================

def analyze_crop(
    image_path,
    crop_age_days=70,
    expected_maturity_days=80
):

    # --------------------------------------
    # 1. DISEASE DETECTION
    # --------------------------------------

    disease, confidence = predict_disease(
        image_path
    )


    # --------------------------------------
    # 2. SEVERITY ESTIMATION
    # --------------------------------------

    severity_result = estimate_severity(
        image_path
    )

    severity = severity_result[
        "severity"
    ]


    # --------------------------------------
    # 3. TREATMENT GUIDANCE
    # --------------------------------------

    treatment = get_treatment(
        disease
    )


    # --------------------------------------
    # 4. RECOVERY ESTIMATION
    # --------------------------------------

    recovery = estimate_recovery(
        disease,
        severity
    )


    # --------------------------------------
    # 5. SALE READINESS
    # --------------------------------------

    if recovery["status"] == "ESTIMATE":

        sale_readiness = (
            calculate_sale_readiness(

                recovery["min_days"],

                recovery["max_days"],

                crop_age_days,

                expected_maturity_days
            )
        )

    else:

        sale_readiness = {

            "status": "UNAVAILABLE",

            "message":
                "Sale-readiness estimate "
                "is unavailable."
        }


    # ======================================
    # FINAL RESULT
    # ======================================

    result = {

        "crop": "Tomato",

        "disease": disease,

        "confidence": round(
            confidence,
            4
        ),

        "confidence_percent": round(
            confidence * 100,
            2
        ),

        "severity": severity,

        "affected_area_percent":
            severity_result.get(
                "affected_area_percent",
                0
            ),

        "treatment": treatment,

        "recovery": recovery,

        "sale_readiness":
            sale_readiness
    }


    return result


# ==========================================
# API-FRIENDLY PREDICTION FUNCTION
# ==========================================
#
# FastAPI will call this function.
#
# React
#    ↓
# Spring Boot
#    ↓
# FastAPI
#    ↓
# predict_image()
#    ↓
# analyze_crop()
#
# ==========================================

def predict_image(image_path):

    result = analyze_crop(
        image_path
    )

    return result


# ==========================================
# TEST PIPELINE DIRECTLY
# ==========================================

if __name__ == "__main__":

    TEST_IMAGE_DIR = os.path.join(
        BASE_DIR,
        "data",
        "PlantVillage",
        "test_images"
    )


    # --------------------------------------
    # CHECK TEST IMAGE DIRECTORY
    # --------------------------------------

    if not os.path.exists(
        TEST_IMAGE_DIR
    ):

        print(
            "\nTest image directory not found:"
        )

        print(
            TEST_IMAGE_DIR
        )

        exit()


    # --------------------------------------
    # FIND IMAGE
    # --------------------------------------

    image_files = [

        file

        for file in os.listdir(
            TEST_IMAGE_DIR
        )

        if file.lower().endswith(
            (
                ".jpg",
                ".jpeg",
                ".png"
            )
        )
    ]


    # --------------------------------------
    # CHECK IMAGE
    # --------------------------------------

    if len(image_files) == 0:

        print(
            "No test image found."
        )

        exit()


    image_path = os.path.join(
        TEST_IMAGE_DIR,
        image_files[0]
    )


    print(
        "\nTesting image:",
        image_files[0]
    )


    # --------------------------------------
    # RUN COMPLETE PIPELINE
    # --------------------------------------

    result = analyze_crop(
        image_path
    )


    # ======================================
    # DISPLAY RESULT
    # ======================================

    print(
        "\n===================================="
    )

    print(
        "CROP-TO-CASH AI PIPELINE"
    )

    print(
        "===================================="
    )


    print(
        "\nCrop:",
        result["crop"]
    )


    print(
        "Disease:",
        result["disease"]
    )


    print(
        "Confidence:",
        f'{result["confidence_percent"]}%'
    )


    print(
        "Severity:",
        result["severity"]
    )


    print(
        "Affected Area:",
        f'{result["affected_area_percent"]}%'
    )


    # --------------------------------------
    # TREATMENT
    # --------------------------------------

    print(
        "\nTreatment:"
    )

    for step in result[
        "treatment"
    ]["steps"]:

        print(
            "-",
            step
        )


    # --------------------------------------
    # RECOVERY
    # --------------------------------------

    print(
        "\nRecovery:"
    )

    print(
        result["recovery"]
    )


    # --------------------------------------
    # SALE READINESS
    # --------------------------------------

    print(
        "\nSale Readiness:"
    )

    print(
        result["sale_readiness"]
    )


    print(
        "\n===================================="
    )