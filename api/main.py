from fastapi import FastAPI
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine
import os

app = FastAPI()
engine = create_async_engine(os.getenv("POSTGRES_URI"))
# conn = engine.connect()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/data")
async def get_data():
    async with engine.connect() as conn:
        sql_statement = text("""SELECT * FROM lwtdemo.script_records;""")
        result = await conn.execute(sql_statement)
    return result
