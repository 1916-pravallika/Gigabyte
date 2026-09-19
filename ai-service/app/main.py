from fastapi import FastAPI, File, UploadFile, HTTPException
from PIL import Image
import io
import os
import sys

# Make project root available
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(0, BASE_DIR)

from app.pipeline import predict_image


app = FastAPI(
    title="Crop-to-Cash AI Service",
    description="AI service for crop disease detection and crop recovery analysis",
    version="1.0"
)


@app.get("/")
def home():
    return {
        "message": "Crop-to-Cash AI Service is running",
        "status": "success"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    # Check file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Please upload an image file."
        )

    try:
        # Read uploaded image
        contents = await file.read()

        image = Image.open(
            io.BytesIO(contents)
        ).convert("RGB")

        # Save temporary image
        temp_path = os.path.join(
            BASE_DIR,
            "data",
            "temp_upload.jpg"
        )

        image.save(temp_path)

        # Run AI pipeline
        result = predict_image(temp_path)

        # Delete temporary image
        if os.path.exists(temp_path):
            os.remove(temp_path)

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )