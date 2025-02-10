import os
from fastapi import FastAPI, Query, Body, Request, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, Response
from typing import Annotated,Optional
from dotenv import load_dotenv

from src.router import routes
from src.structs import PathDetailStruct, PathStruct, PayloadStruct

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

@app.get("/")
async def root():
    return {"message":"Hello World", "detail":"internal-router"}

@app.post("/addroute")
async def addroute(payload:PathDetailStruct):
    return Route.create_route(payload)

@app.post("/removeroute")
async def removeroute():
    return

@app.get("/{pathinput}")
async def route(pathinput: str, request: Request):
    path = PathStruct(id=pathinput)
    query = request.query_params
    redirect_link = Route.retrieve_route(path)
    if redirect_link == None:
        raise HTTPException(status_code=404, detail="path does not exist (internal-router)")
    url = redirect_link["link"]+f"?{query}"
    return RedirectResponse(url)

@app.post("/{pathinput}")
async def route(pathinput:str, request: Request):
    path = PathStruct(id=pathinput)
    redirect_link = Route.retrieve_route(path)
    if redirect_link == None:
        raise HTTPException(status_code=404, detail="path does not exist (internal-router)")
    header = {'Location':redirect_link["link"]}
    payload = await request.body()
    return Response(headers=header, content=payload, status_code=status.HTTP_307_TEMPORARY_REDIRECT)



