from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os
import random

router = APIRouter(
    prefix="/frogs",
    tags=["Frog Images"]
)

IMG_DIR = "/app/images"

@router.get("/random")
def get_random_frog():
    try:
        files = [f for f in os.listdir(IMG_DIR) if os.path.isfile(os.path.join(IMG_DIR, f))]

        if not files:
            raise HTTPException(status_code=404, detail="No frogs found :(")

        random_img = random.choice(files)
        img_path = os.path.join(IMG_DIR, random_img)
        return FileResponse(img_path)
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))