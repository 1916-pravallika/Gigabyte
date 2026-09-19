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

MARKET_PATH = os.path.join(
    BASE_DIR,
    "data",
    "market_prices.json"
)


# ==========================================
# LOAD MARKET DATA
# ==========================================

with open(
    MARKET_PATH,
    "r",
    encoding="utf-8"
) as file:

    market_data = json.load(file)


# ==========================================
# GET MARKET PRICES
# ==========================================

def get_market_prices(crop):

    if crop not in market_data:

        return []

    return market_data[crop]


# ==========================================
# FIND HIGHEST PRICE MARKET
# ==========================================

def get_highest_price_market(crop):

    markets = get_market_prices(crop)

    if not markets:

        return None

    highest_market = max(
        markets,
        key=lambda market: market["price_per_kg"]
    )

    return highest_market


# ==========================================
# DISPLAY MARKET INFORMATION
# ==========================================

if __name__ == "__main__":

    crop = "Tomato"

    markets = get_market_prices(crop)

    print("\n====================================")
    print("MARKET PRICE INFORMATION")
    print("====================================")

    print(
        "\nCrop:",
        crop
    )

    if not markets:

        print(
            "No market information available."
        )

    else:

        for market in markets:

            print("\n------------------------------------")

            print(
                "Market:",
                market["market"]
            )

            print(
                "Location:",
                market["location"]
            )

            print(
                "Price:",
                f'₹{market["price_per_kg"]}/kg'
            )

            print(
                "Buyer Type:",
                market["buyer_type"]
            )

            print(
                "Demand:",
                market["demand"]
            )

    # ======================================
    # HIGHEST PRICE
    # ======================================

    highest = get_highest_price_market(crop)

    if highest:

        print("\n====================================")
        print("HIGHEST DEMO PRICE")
        print("====================================")

        print(
            "Market:",
            highest["market"]
        )

        print(
            "Price:",
            f'₹{highest["price_per_kg"]}/kg'
        )

        print(
            "Demand:",
            highest["demand"]
        )

    print("\n====================================")