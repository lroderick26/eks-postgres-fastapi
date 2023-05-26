from sqlalchemy import create_engine, text
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from .db import SessionLocal, engine

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()



@app.get("/")
def main():
    return RedirectResponse(url="/docs/")


@app.get("/data")
def show_records(db: Session = Depends(get_db)):
    sql_statement = text("""SELECT * FROM lwtdemo.script_records;""")
    records = db.query(sql_statement).all()
    return records