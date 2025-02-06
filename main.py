import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from dotenv import load_dotenv

from src.router import routes

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

@app.get("/route/{path}")
async def route(path:str):
    return RedirectResponse(Route.redirect(path))

@app.post("/route/{path}")
async def route(path:str):
    return RedirectResponse(Route.redirect(path))

@app.get("/addroute")
async def addroute(path:str, link:str, method:str):
    return Route.create_route(path, link, method)

@app.get("/removeroute")
async def removeroute():
    return

@app.get("/")
async def root():
    return {"message":"Hello World", "detail":"internal-router"}