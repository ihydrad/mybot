import uvicorn
import config, tools

from fastapi import FastAPI


app = FastAPI()
err_msg = "Not valid input data"


@app.get("/")
async def root():
    return "Get out of here!"


@app.get("/open_door")
async def door():
    tools.open_door(config.ufanet_username, config.ufanet_password)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8181)
