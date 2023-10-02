from fastapi import FastAPI
import random

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/random/{max}")
async def get_random(max: int):
    rand: int = random.randint(0, max)
    return {"random": rand, "min":0, "max": max}