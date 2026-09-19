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

RECOVERY_PATH = os.path.join(
    BASE_DIR,
    "data",
    "recovery.json"
)


# ==========================================
# LOAD RECOVERY DATA
# ==========================================

with open(
    RECOVERY_PATH,
    "r",
    encoding="utf-8"
) as file:

    recovery_data = json.load(file)


# ==========================================
# RECOVERY ESTIMATION
# ==========================================

def estimate_recovery(disease, severity):

    severity = severity.upper()

    # Disease not available
    if disease not in recovery_data:

        return {
            "status": "UNAVAILABLE",
            "message": "Recovery estimate is not available."
        }

    # Severity not available
    if severity not in recovery_data[disease]:

        return {
            "status": "UNAVAILABLE",
            "message": "Recovery estimate is not available for this severity."
        }

    recovery = recovery_data[
        disease
    ][
        severity
    ]

    min_days = recovery["min_days"]
    max_days = recovery["max_days"]

    # Healthy crop
    if disease == "Tomato___healthy":

        return {
            "status": "HEALTHY",
            "min_days": 0,
            "max_days": 0,
            "message": "No disease-related recovery period is estimated."
        }

    return {
        "status": "ESTIMATE",
        "min_days": min_days,
        "max_days": max_days,
        "message": (
            f"Estimated recovery range: "
            f"{min_days}-{max_days} days."
        )
    }


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    disease = "Tomato___Late_blight"

    severity = "MODERATE"

    result = estimate_recovery(
        disease,
        severity
    )

    print("\n====================================")
    print("RECOVERY ESTIMATE")
    print("====================================")

    print(
        "Disease:",
        disease
    )

    print(
        "Severity:",
        severity
    )

    print(
        "Status:",
        result["status"]
    )

    if result["status"] == "ESTIMATE":

        print(
            "Minimum Recovery:",
            result["min_days"],
            "days"
        )

        print(
            "Maximum Recovery:",
            result["max_days"],
            "days"
        )

        print(
            "Message:",
            result["message"]
        )

    else:

        print(
            "Message:",
            result["message"]
        )

    print("====================================")