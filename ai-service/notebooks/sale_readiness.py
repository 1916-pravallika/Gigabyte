# ==========================================
# CROP-TO-CASH
# SALE READINESS ENGINE
# ==========================================


def calculate_sale_readiness(
    recovery_min_days,
    recovery_max_days,
    crop_age_days,
    expected_maturity_days
):

    # ==========================================
    # VALIDATION
    # ==========================================

    if crop_age_days < 0:

        raise ValueError(
            "Crop age cannot be negative."
        )

    if expected_maturity_days <= 0:

        raise ValueError(
            "Expected maturity must be greater than zero."
        )

    if recovery_min_days < 0 or recovery_max_days < 0:

        raise ValueError(
            "Recovery days cannot be negative."
        )

    if recovery_min_days > recovery_max_days:

        raise ValueError(
            "Minimum recovery cannot exceed maximum recovery."
        )


    # ==========================================
    # MATURITY CALCULATION
    # ==========================================

    maturity_remaining = max(
        expected_maturity_days - crop_age_days,
        0
    )


    # ==========================================
    # SALE READINESS WINDOW
    # ==========================================

    earliest_sale_day = max(
        recovery_min_days,
        maturity_remaining
    )

    latest_sale_day = max(
        recovery_max_days,
        maturity_remaining
    )


    # ==========================================
    # STATUS
    # ==========================================

    if (
        maturity_remaining == 0
        and recovery_max_days == 0
    ):

        status = "READY"

        message = (
            "The crop is estimated to be "
            "ready for sale."
        )

    elif maturity_remaining > recovery_max_days:

        status = "MATURITY_PENDING"

        message = (
            "The crop may recover before it "
            "reaches the expected maturity period."
        )

    elif recovery_max_days > maturity_remaining:

        status = "RECOVERY_PENDING"

        message = (
            "The crop is expected to need "
            "additional recovery time before sale."
        )

    else:

        status = "RECOVERY_AND_MATURITY_PENDING"

        message = (
            "Both recovery and crop maturity "
            "should be monitored before sale."
        )


    # ==========================================
    # RESULT
    # ==========================================

    return {

        "status": status,

        "maturity_remaining_days":
            maturity_remaining,

        "earliest_sale_estimate_days":
            earliest_sale_day,

        "latest_sale_estimate_days":
            latest_sale_day,

        "message":
            message
    }


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    # Example:
    #
    # Disease recovery:
    # 10-16 days
    #
    # Crop age:
    # 70 days
    #
    # Expected maturity:
    # 80 days

    recovery_min = 10
    recovery_max = 16

    crop_age = 70

    expected_maturity = 80


    result = calculate_sale_readiness(

        recovery_min,

        recovery_max,

        crop_age,

        expected_maturity
    )


    print("\n====================================")

    print(
        "CROP-TO-CASH SALE READINESS"
    )

    print("====================================")

    print(
        "Crop Age:",
        crop_age,
        "days"
    )

    print(
        "Expected Maturity:",
        expected_maturity,
        "days"
    )

    print(
        "Maturity Remaining:",
        result[
            "maturity_remaining_days"
        ],
        "days"
    )

    print(
        "Earliest Sale Estimate:",
        result[
            "earliest_sale_estimate_days"
        ],
        "days from now"
    )

    print(
        "Latest Sale Estimate:",
        result[
            "latest_sale_estimate_days"
        ],
        "days from now"
    )

    print(
        "Status:",
        result["status"]
    )

    print(
        "Message:",
        result["message"]
    )

    print("====================================")