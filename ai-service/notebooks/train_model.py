import os
import json
import time

import torch
from torchvision import datasets, transforms, models
from torch import nn, optim
from torch.utils.data import DataLoader


# ============================================================
# 1. PROJECT PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

TRAIN_DIR = os.path.join(
    BASE_DIR,
    "data",
    "PlantVillage",
    "train"
)

VAL_DIR = os.path.join(
    BASE_DIR,
    "data",
    "PlantVillage",
    "val"
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models"
)

os.makedirs(MODEL_DIR, exist_ok=True)


# ============================================================
# 2. DEVICE
# ============================================================

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("====================================")
print("DEVICE:", device)
print("====================================")


# ============================================================
# 3. IMAGE TRANSFORMS
# ============================================================

train_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


val_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


# ============================================================
# 4. LOAD DATASET
# ============================================================

print("\nLoading datasets...")

train_dataset = datasets.ImageFolder(
    TRAIN_DIR,
    transform=train_transform
)

val_dataset = datasets.ImageFolder(
    VAL_DIR,
    transform=val_transform
)


print("\nClasses:")
for index, class_name in enumerate(train_dataset.classes):
    print(f"{index} -> {class_name}")


print("\nTraining images:", len(train_dataset))
print("Validation images:", len(val_dataset))


# ============================================================
# 5. SAVE CLASS NAMES
# ============================================================

class_names_path = os.path.join(
    MODEL_DIR,
    "class_names.json"
)

with open(
    class_names_path,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        train_dataset.classes,
        file,
        indent=4
    )

print("\nClass names saved.")


# ============================================================
# 6. DATA LOADERS
# ============================================================

train_loader = DataLoader(
    train_dataset,
    batch_size=16,
    shuffle=True,
    num_workers=0
)

val_loader = DataLoader(
    val_dataset,
    batch_size=16,
    shuffle=False,
    num_workers=0
)


# ============================================================
# 7. LOAD MOBILENETV2
# ============================================================

print("\nLoading MobileNetV2...")

model = models.mobilenet_v2(
    weights=models.MobileNet_V2_Weights.DEFAULT
)


# ============================================================
# 8. CHANGE FINAL LAYER
# ============================================================

number_of_classes = len(
    train_dataset.classes
)

model.classifier[1] = nn.Linear(
    model.classifier[1].in_features,
    number_of_classes
)

model = model.to(device)


# ============================================================
# 9. LOSS + OPTIMIZER
# ============================================================

criterion = nn.CrossEntropyLoss()

optimizer = optim.Adam(
    model.parameters(),
    lr=0.0001
)


# ============================================================
# 10. ONE EPOCH
# ============================================================

EPOCHS = 1

best_val_accuracy = 0.0


# ============================================================
# 11. TRAIN
# ============================================================

for epoch in range(EPOCHS):

    print("\n====================================")
    print(f"EPOCH {epoch + 1}/{EPOCHS}")
    print("====================================")

    start_time = time.time()

    model.train()

    running_loss = 0.0
    correct = 0
    total = 0

    for batch_number, (images, labels) in enumerate(train_loader):

        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()

        outputs = model(images)

        loss = criterion(
            outputs,
            labels
        )

        loss.backward()

        optimizer.step()

        running_loss += (
            loss.item() * images.size(0)
        )

        _, predicted = torch.max(
            outputs,
            1
        )

        total += labels.size(0)

        correct += (
            predicted == labels
        ).sum().item()

        # Show progress every 50 batches
        if (batch_number + 1) % 50 == 0:

            print(
                f"Processed batches: "
                f"{batch_number + 1}/"
                f"{len(train_loader)}"
            )


    train_loss = (
        running_loss / len(train_dataset)
    )

    train_accuracy = (
        correct / total
    ) * 100


    # ========================================================
    # 12. VALIDATION
    # ========================================================

    print("\nRunning validation...")

    model.eval()

    val_correct = 0
    val_total = 0
    val_loss_total = 0.0

    with torch.no_grad():

        for images, labels in val_loader:

            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)

            loss = criterion(
                outputs,
                labels
            )

            val_loss_total += (
                loss.item() * images.size(0)
            )

            _, predicted = torch.max(
                outputs,
                1
            )

            val_total += labels.size(0)

            val_correct += (
                predicted == labels
            ).sum().item()


    val_loss = (
        val_loss_total / len(val_dataset)
    )

    val_accuracy = (
        val_correct / val_total
    ) * 100


    elapsed_time = (
        time.time() - start_time
    )


    # ========================================================
    # 13. RESULTS
    # ========================================================

    print("\n====================================")
    print("EPOCH RESULTS")
    print("====================================")

    print(
        f"Train Loss: {train_loss:.4f}"
    )

    print(
        f"Train Accuracy: "
        f"{train_accuracy:.2f}%"
    )

    print(
        f"Validation Loss: "
        f"{val_loss:.4f}"
    )

    print(
        f"Validation Accuracy: "
        f"{val_accuracy:.2f}%"
    )

    print(
        f"Epoch Time: "
        f"{elapsed_time / 60:.2f} minutes"
    )


    # ========================================================
    # 14. SAVE MODEL
    # ========================================================

    if val_accuracy > best_val_accuracy:

        best_val_accuracy = val_accuracy

        model_path = os.path.join(
            MODEL_DIR,
            "tomato_disease_model.pth"
        )

        torch.save(
            model.state_dict(),
            model_path
        )

        print("\nModel saved:")
        print(model_path)


print("\n====================================")
print("TRAINING COMPLETE")
print("====================================")

print(
    f"Best Validation Accuracy: "
    f"{best_val_accuracy:.2f}%"
)