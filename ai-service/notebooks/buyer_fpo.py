import os
import json


# ==========================================
# PATHS
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

BUYERS_PATH = os.path.join(
    BASE_DIR,
    "data",
    "buyers.json"
)

FPOS_PATH = os.path.join(
    BASE_DIR,
    "data",
    "fpos.json"
)


# ==========================================
# LOAD DATA
# ==========================================

with open(
    BUYERS_PATH,
    "r",
    encoding="utf-8"
) as file:

    buyers_data = json.load(file)


with open(
    FPOS_PATH,
    "r",
    encoding="utf-8"
) as file:

    fpos_data = json.load(file)


# ==========================================
# GET BUYERS
# ==========================================

def get_buyers(crop):

    return buyers_data.get(
        crop,
        []
    )


# ==========================================
# GET FPOS
# ==========================================

def get_fpos(crop):

    return fpos_data.get(
        crop,
        []
    )


# ==========================================
# DISPLAY BUYERS
# ==========================================

def display_buyers(crop):

    buyers = get_buyers(crop)

    print("\n====================================")
    print("AVAILABLE BUYERS")
    print("====================================")

    if not buyers:

        print(
            "No buyers available."
        )

        return

    for buyer in buyers:

        print("\n------------------------------------")

        print(
            "Buyer:",
            buyer["name"]
        )

        print(
            "Location:",
            buyer["location"]
        )

        print(
            "Distance:",
            buyer["distance_km"],
            "km"
        )

        print(
            "Required Quantity:",
            buyer["required_quantity_kg"],
            "kg"
        )

        print(
            "Indicative Price:",
            f'₹{buyer["indicative_price_per_kg"]}/kg'
        )

        print(
            "Contact:",
            buyer["contact"]
        )


# ==========================================
# DISPLAY FPOS
# ==========================================

def display_fpos(crop):

    fpos = get_fpos(crop)

    print("\n====================================")
    print("AVAILABLE FPOS")
    print("====================================")

    if not fpos:

        print(
            "No FPOs available."
        )

        return

    for fpo in fpos:

        print("\n------------------------------------")

        print(
            "FPO:",
            fpo["name"]
        )

        print(
            "Location:",
            fpo["location"]
        )

        print(
            "Distance:",
            fpo["distance_km"],
            "km"
        )

        print(
            "Members:",
            fpo["member_count"]
        )

        print(
            "Required Quantity:",
            fpo["required_quantity_kg"],
            "kg"
        )

        print(
            "Indicative Price:",
            f'₹{fpo["indicative_price_per_kg"]}/kg'
        )

        print(
            "Contact:",
            fpo["contact"]
        )


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    crop = "Tomato"

    display_buyers(crop)

    display_fpos(crop)

    print("\n====================================")
    print("BUYER + FPO MODULE COMPLETE")
    print("====================================")