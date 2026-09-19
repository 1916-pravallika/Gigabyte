import os
import json
import math


# ==========================================
# PATH
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

STORAGE_PATH = os.path.join(
    BASE_DIR,
    "data",
    "cold_storages.json"
)


# ==========================================
# LOAD DATA
# ==========================================

with open(
    STORAGE_PATH,
    "r",
    encoding="utf-8"
) as file:

    storage_data = json.load(file)


# ==========================================
# HAVERSINE DISTANCE
# ==========================================

def calculate_distance(
    latitude1,
    longitude1,
    latitude2,
    longitude2
):

    earth_radius_km = 6371.0

    lat1 = math.radians(latitude1)
    lat2 = math.radians(latitude2)

    delta_lat = math.radians(
        latitude2 - latitude1
    )

    delta_lon = math.radians(
        longitude2 - longitude1
    )

    a = (
        math.sin(delta_lat / 2) ** 2
        +
        math.cos(lat1)
        *
        math.cos(lat2)
        *
        math.sin(delta_lon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return earth_radius_km * c


# ==========================================
# FIND NEARBY STORAGE
# ==========================================

def find_nearby_storage(
    crop,
    farmer_latitude,
    farmer_longitude,
    required_quantity_kg=0
):

    results = []

    for storage in storage_data[
        "cold_storages"
    ]:

        # Check crop compatibility
        supported_crops = [
            crop_name.lower()
            for crop_name in storage[
                "supported_crops"
            ]
        ]

        if crop.lower() not in supported_crops:

            continue

        # Check available capacity
        if (
            storage["available_capacity_kg"]
            < required_quantity_kg
        ):

            continue

        # Calculate distance
        distance = calculate_distance(
            farmer_latitude,
            farmer_longitude,
            storage["latitude"],
            storage["longitude"]
        )

        result = storage.copy()

        result["distance_km"] = round(
            distance,
            2
        )

        results.append(result)

    # Sort by distance
    results.sort(
        key=lambda storage:
        storage["distance_km"]
    )

    return results


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    # Demo farmer location
    farmer_latitude = 15.9129
    farmer_longitude = 79.7400

    crop = "Tomato"

    required_quantity = 3000

    storages = find_nearby_storage(

        crop,

        farmer_latitude,

        farmer_longitude,

        required_quantity
    )

    print("\n====================================")
    print("COLD STORAGE RECOMMENDATIONS")
    print("====================================")

    print(
        "\nCrop:",
        crop
    )

    print(
        "Required Quantity:",
        required_quantity,
        "kg"
    )

    print(
        "Farmer Location:",
        farmer_latitude,
        farmer_longitude
    )

    if not storages:

        print(
            "\nNo suitable cold storage found."
        )

    else:

        for storage in storages:

            print(
                "\n------------------------------------"
            )

            print(
                "Storage:",
                storage["name"]
            )

            print(
                "Location:",
                storage["location"]
            )

            print(
                "Distance:",
                storage["distance_km"],
                "km"
            )

            print(
                "Available Capacity:",
                storage[
                    "available_capacity_kg"
                ],
                "kg"
            )

            print(
                "Cost:",
                f'₹{storage["cost_per_kg_per_day"]}/kg/day'
            )

            print(
                "Contact:",
                storage["contact"]
            )

    print(
        "\n===================================="
    )