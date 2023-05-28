from sqlalchemy import create_engine, text
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

SQLALCHEMY_DATABASE_URL = os.getenv("POSTGRES_URI")

engine = create_engine(SQLALCHEMY_DATABASE_URL)


def get_db():
    try:
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        Base = declarative_base()
        db = SessionLocal()
        yield db
    finally:
        db.close()



@app.get("/")
def main():
    return RedirectResponse(url="/docs/")


@app.get("/data")
def show_records(db: Session = Depends(get_db)):
    sql_statement = text("""SELECT id, title, date_info, sentiment, sentence, sadness_score, joy_score, love_score, anger_score, fear_score, surprise_score FROM lwtdemo.script_records;""")
    records = db.execute(sql_statement)
    rows = [row._asdict() for row in records]
    return rows
