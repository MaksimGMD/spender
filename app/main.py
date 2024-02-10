from fastapi import FastAPI

app = FastAPI(title="Spender API")


@app.get("/")
async def root():
    return {"message": "Hello World"}
