import uvicorn
from api.tools import open_door

from fastapi import FastAPI


app = FastAPI()
err_msg = "Not valid input data"


@app.get("/")
async def root():
    return "Get out of here!"


@app.get("/open_door")
async def door():
    return open_door(56763)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8181)
