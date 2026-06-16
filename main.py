from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from routers import frogs

app = FastAPI(title="FrogAPI 🐸", description="The ultimate source for frog content.")

app.include_router(frogs.router)

@app.get("/")
def root():
    return {"message": "Quack! Welcome to FrogAPI! Go to /docs to see all endpoints."}
