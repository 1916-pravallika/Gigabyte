import os

import cv2
import numpy as np


# ==========================================
# ESTIMATE VISUAL DAMAGE
# ==========================================

def estimate_severity(image_path):

    image = cv2.imread(image_path)

    if image is None:
        raise ValueError(
            "Could not read image: " + image_path
        )

    # Resize for faster processing
    image = cv2.resize(
        image,
        (224, 224)
    )

    # Convert BGR to HSV
    hsv = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2HSV
    )

    # ==========================================
    # FIND LEAF-COLORED AREA
    # ==========================================

    lower_green = np.array(
        [25, 30, 30]
    )

    upper_green = np.array(
        [100, 255, 255]
    )

    green_mask = cv2.inRange(
        hsv,
        lower_green,
        upper_green
    )

    # ==========================================
    # FIND NON-GREEN COLORED AREA
    # ==========================================

    lower_damage = np.array(
        [5, 40, 20]
    )

    upper_damage = np.array(
        [30, 255, 255]
    )

    damage_mask = cv2.inRange(
        hsv,
        lower_damage,
        upper_damage
    )

    # ==========================================
    # CALCULATE AREAS
    # ==========================================

    leaf_area = np.sum(
        green_mask > 0
    )

    damage_area = np.sum(
        damage_mask > 0
    )

    if leaf_area == 0:

        return {
            "severity": "UNKNOWN",
            "affected_area_percent": 0.0,
            "message": "Leaf area could not be detected."
        }

    affected_percentage = (
        damage_area / leaf_area
    ) * 100

    # Limit unreasonable values
    affected_percentage = min(
        affected_percentage,
        100
    )

    # ==========================================
    # SEVERITY RULES
    # ==========================================

    if affected_percentage < 10:

        severity = "MILD"

    elif affected_percentage < 30:

        severity = "MODERATE"

    else:

        severity = "SEVERE"

    # ==========================================
    # RESULT
    # ==========================================

    return {
        "severity": severity,
        "affected_area_percent": round(
            affected_percentage,
            2
        )
    }


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    BASE_DIR = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    TEST_IMAGE_DIR = os.path.join(
        BASE_DIR,
        "data",
        "PlantVillage",
        "test_images"
    )

    image_files = [
        file
        for file in os.listdir(
            TEST_IMAGE_DIR
        )
        if file.lower().endswith(
            (".jpg", ".jpeg", ".png")
        )
    ]

    if len(image_files) == 0:

        print(
            "No test image found."
        )

        exit()

    image_path = os.path.join(
        TEST_IMAGE_DIR,
        image_files[0]
    )

    result = estimate_severity(
        image_path
    )

    print("\n====================================")
    print("SEVERITY ESTIMATION")
    print("====================================")

    print(
        "Image:",
        image_files[0]
    )

    print(
        "Severity:",
        result["severity"]
    )

    print(
        "Affected Area:",
        f'{result["affected_area_percent"]}%'
    )

    if "message" in result:

        print(
            "Message:",
            result["message"]
        )

    print("====================================")