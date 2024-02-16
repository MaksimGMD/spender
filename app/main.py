from fastapi import FastAPI
import os

app = FastAPI(title="Spender API")

test = os.getenv("POSTGRES_USER")
print(test)

@app.get("/")
async def root():
    return {"message": "Hello World"}
