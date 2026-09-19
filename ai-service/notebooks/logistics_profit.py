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

LOGISTICS_PATH = os.path.join(
    BASE_DIR,
    "data",
    "logistics.json"
)


# ==========================================
# LOAD LOGISTICS DATA
# ==========================================

with open(
    LOGISTICS_PATH,
    "r",
    encoding="utf-8"
) as file:

    logistics_data = json.load(file)


# ==========================================
# GET SUITABLE TRANSPORT
# ==========================================

def get_transport_options(
    quantity_kg
):

    options = []

    for transport in logistics_data[
        "transport_options"
    ]:

        if (
            transport["capacity_kg"]
            >= quantity_kg
        ):

            options.append(
                transport
            )

    return options


# ==========================================
# CALCULATE TRANSPORT COST
# ==========================================

def calculate_transport_cost(
    distance_km,
    transport
):

    return (
        distance_km
        * transport["cost_per_km"]
    )


# ==========================================
# CALCULATE STORAGE COST
# ==========================================

def calculate_storage_cost(
    quantity_kg,
    storage_cost_per_kg_per_day,
    storage_days
):

    return (
        quantity_kg
        * storage_cost_per_kg_per_day
        * storage_days
    )


# ==========================================
# CALCULATE NET RETURN
# ==========================================

def calculate_net_return(
    quantity_kg,
    market_price_per_kg,
    transport_cost,
    storage_cost=0,
    other_costs=0
):

    gross_revenue = (
        quantity_kg
        * market_price_per_kg
    )

    total_cost = (
        transport_cost
        + storage_cost
        + other_costs
    )

    net_return = (
        gross_revenue
        - total_cost
    )

    return {
        "gross_revenue": round(
            gross_revenue,
            2
        ),

        "transport_cost": round(
            transport_cost,
            2
        ),

        "storage_cost": round(
            storage_cost,
            2
        ),

        "other_costs": round(
            other_costs,
            2
        ),

        "total_cost": round(
            total_cost,
            2
        ),

        "estimated_net_return": round(
            net_return,
            2
        )
    }


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    # Demo farmer crop
    quantity = 3000

    # Demo market
    market = "Vijayawada"

    market_price = 30

    # Demo distance
    distance = 80

    # Demo storage
    storage_cost_per_kg_per_day = 0.40

    storage_days = 5

    # ======================================
    # TRANSPORT OPTIONS
    # ======================================

    transports = get_transport_options(
        quantity
    )

    print("\n====================================")
    print("LOGISTICS OPTIONS")
    print("====================================")

    for transport in transports:

        transport_cost = (
            calculate_transport_cost(
                distance,
                transport
            )
        )

        print("\n------------------------------------")

        print(
            "Provider:",
            transport["provider"]
        )

        print(
            "Vehicle:",
            transport["vehicle_type"]
        )

        print(
            "Capacity:",
            transport["capacity_kg"],
            "kg"
        )

        print(
            "Transport Cost:",
            f"₹{transport_cost:.2f}"
        )

    # ======================================
    # SELECT FIRST TRANSPORT OPTION
    # ======================================

    selected_transport = transports[0]

    transport_cost = calculate_transport_cost(
        distance,
        selected_transport
    )

    # ======================================
    # STORAGE COST
    # ======================================

    storage_cost = calculate_storage_cost(
        quantity,
        storage_cost_per_kg_per_day,
        storage_days
    )

    # ======================================
    # NET RETURN
    # ======================================

    result = calculate_net_return(

        quantity_kg=quantity,

        market_price_per_kg=market_price,

        transport_cost=transport_cost,

        storage_cost=storage_cost
    )

    # ======================================
    # DISPLAY
    # ======================================

    print("\n====================================")
    print("EXPECTED NET RETURN")
    print("====================================")

    print(
        "Market:",
        market
    )

    print(
        "Quantity:",
        quantity,
        "kg"
    )

    print(
        "Market Price:",
        f"₹{market_price}/kg"
    )

    print(
        "Gross Revenue:",
        f'₹{result["gross_revenue"]:.2f}'
    )

    print(
        "Transport Cost:",
        f'₹{result["transport_cost"]:.2f}'
    )

    print(
        "Storage Cost:",
        f'₹{result["storage_cost"]:.2f}'
    )

    print(
        "Total Cost:",
        f'₹{result["total_cost"]:.2f}'
    )

    print(
        "Estimated Net Return:",
        f'₹{result["estimated_net_return"]:.2f}'
    )

    print("====================================")