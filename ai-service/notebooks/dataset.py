import os

# Find the ai-service folder automatically
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

TRAIN_PATH = os.path.join(
    BASE_DIR,
    "data",
    "PlantVillage",
    "train"
)

VAL_PATH = os.path.join(
    BASE_DIR,
    "data",
    "PlantVillage",
    "val"
)


def count_images(folder_path):

    valid_extensions = (
        ".jpg",
        ".jpeg",
        ".png",
        ".JPG",
        ".JPEG",
        ".PNG"
    )

    count = 0

    if not os.path.exists(folder_path):
        return 0

    for file in os.listdir(folder_path):

        if file.endswith(valid_extensions):
            count += 1

    return count


def check_dataset(base_path):

    print("\n====================================")
    print(f"Checking: {base_path}")
    print("====================================")

    if not os.path.exists(base_path):

        print("ERROR: Folder not found!")

        return

    classes = sorted(os.listdir(base_path))

    for class_name in classes:

        class_path = os.path.join(
            base_path,
            class_name
        )

        if os.path.isdir(class_path):

            image_count = count_images(
                class_path
            )

            print(
                f"{class_name:<60} "
                f"{image_count}"
            )


print("\n========== TRAIN DATASET ==========")

check_dataset(TRAIN_PATH)


print("\n========== VALIDATION DATASET ==========")

check_dataset(VAL_PATH)