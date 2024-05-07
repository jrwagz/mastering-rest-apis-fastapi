from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    """Root API response

    Returns:
        simple dictionary hello world
    """
    return {"message": "Hello World"}