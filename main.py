from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os
import random

app = FastAPI()

IMG_DIR = "/app/images"

@app.get("/randomfrog")
def get_random_frog():
    try:
        files = [f for f in os.listdir(IMG_DIR) if os.path.isfile(os.path.join(IMG_DIR, f))]

        if not files:
            raise HTTPException(status_code=404, detail="No frogs found :(")

        random_img = random.choice(files)
        img_path = os.path.join(IMG_DIR, random_img)
        return FileResponse(img_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))