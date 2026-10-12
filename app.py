from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "status": "healthy",
        "message": "Welcome to my production CloudOps container deployment!",
        "version": "1.0.0"
    }
