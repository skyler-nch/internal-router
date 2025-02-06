import os
from fastapi import FastAPI, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from typing import Annotated
from dotenv import load_dotenv

from src.router import routes
from src.structs import PathDetailStruct, PathStruct

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR,'.env'))

app = FastAPI()

origins = [
    "http://172.18.0.1:5001",
    "http://172.18.0.1:5003",

    "http://127.0.0.1:8000",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Route = routes()

@app.get("/route")
async def route(path:Annotated[PathStruct,Query()]):
    return RedirectResponse(Route.redirect(path))

@app.post("/route")
async def route(path:PathStruct):
    return RedirectResponse(Route.redirect(path))

@app.post("/addroute")
async def addroute(payload:PathDetailStruct):
    return Route.create_route(payload)

@app.post("/removeroute")
async def removeroute():
    return

@app.get("/")
async def root():
    return {"message":"Hello World", "detail":"internal-router"}