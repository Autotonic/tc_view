import json
import re
from pathlib import Path
from typing import Optional

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

static_path = Path.cwd() / "static"

class Response(BaseModel):
    error_: bool
    status_code: int
    promoted: Optional[list]
    rooms: Optional[dict]


app = FastAPI()
app.mount(
    "/static", StaticFiles(directory=static_path), name="static"
)


async def get_tc():
    # async with httpx.AsyncClient(proxies="http://localhost:8118") as client:
    async with httpx.AsyncClient() as client:
        res = await client.get("https://tinychat.com/#category=all")
        if res.status_code == 200:
            promoted = json.loads(
                re.findall(r"data.promoted = JSON.parse\('(.+)'\);", res.text)[0]
            )
            allrooms = json.loads(
                re.findall(r"data.rooms = JSON.parse\('(.+)'\);", res.text)[0]
            )
            return Response(
                error_=False,
                status_code=res.status_code,
                promoted=promoted,
                rooms=allrooms,
            )
        else:
            return Response(error_=True, status_code=res.status_code)


@app.get("/api", response_model=Response)
async def root(request: Request):
    return await get_tc()


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    with open("index.html", "r") as index:
        return HTMLResponse(content=index.read(), status_code=200)
