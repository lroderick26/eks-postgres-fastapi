from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import json

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

# @app.get("/data/{content_partner}")
# def get_data(content_partner: str):
#     if content_partner=='barre3':
#         with open('./data/barre3.json', 'r') as json_file:
#             data = json.load(json_file)
#     elif content_partner=='brookeburkebody':
#         with open('./data/brookeburkebody.json', 'r') as json_file:
#             data = json.load(json_file)
#     elif content_partner=='obe':
#         with open('./data/obe.json', 'r') as json_file:
#             data = json.load(json_file)
#     else:
#         data = None
#     return data