import os
import json


# ==========================================
# PATH
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

TREATMENT_PATH = os.path.join(
    BASE_DIR,
    "data",
    "treatments.json"
)


# ==========================================
# LOAD TREATMENTS
# ==========================================

with open(
    TREATMENT_PATH,
    "r",
    encoding="utf-8"
) as file:

    treatments = json.load(file)


# ==========================================
# GET TREATMENT
# ==========================================

def get_treatment(disease):

    if disease not in treatments:

        return {
            "disease_name": disease,
            "description": "Treatment information is not available.",
            "steps": [
                "Consult a local agricultural expert."
            ],
            "prevention": []
        }

    return treatments[disease]


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    disease = "Tomato___Late_blight"

    result = get_treatment(disease)

    print("\n====================================")
    print("TREATMENT GUIDANCE")
    print("====================================")

    print(
        "\nDisease:",
        result["disease_name"]
    )

    print(
        "\nDescription:",
        result["description"]
    )

    print("\nRecommended Steps:")

    for number, step in enumerate(
        result["steps"],
        start=1
    ):

        print(
            f"{number}. {step}"
        )

    print("\nPrevention:")

    for number, step in enumerate(
        result["prevention"],
        start=1
    ):

        print(
            f"{number}. {step}"
        )

    print("\n====================================")