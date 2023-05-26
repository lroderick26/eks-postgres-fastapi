from fastapi import FastAPI
from sqlalchemy import create_engine
import os

app = FastAPI()
engine = create_engine(os.getenv("POSTGRES_URI"))
conn = engine.connect()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/data")
def get_data():
    sql_statement = "SELECT * FROM lwtdemo.script_records"
    returned_data = conn.execute(sql_statement).fetchall()
    return returned_data
