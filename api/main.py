from sqlalchemy import create_engine, text
from typing import Union
from typing_extensions import Annotated

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
current_directory = os.path.dirname(__file__)
templates = Jinja2Templates(directory=current_directory+"/templates")

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


@app.get("/data", description="Get all data")
def show_records(db: Session = Depends(get_db)):
    """
        Retrieve all results in database

        Returns:
        - The results for all movies
        """
    sql_statement = text("""SELECT id, title, date_info, sentiment, sentence, sadness_score, joy_score, love_score, anger_score, fear_score, surprise_score FROM lwtdemo.script_records;""")
    records = db.execute(sql_statement)
    rows = [row._asdict() for row in records]
    return rows


@app.get("/data/title/{title_id}", description="Get results of a script by script title")
def show_records(title_id: str, db: Session = Depends(get_db)):
    """
        Retrieve filtered results by title of movie.

        - **title_id**: Title of movie as shown via /data route. Hint: use full title with .html for now

        Returns:
        - The results for movie script
        """
    text_statement = f"""SELECT id, 
                            title, 
                            date_info, 
                            sentiment, 
                            sentence, 
                            sadness_score, 
                            joy_score, 
                            love_score, 
                            anger_score, 
                            fear_score,
                            surprise_score 
                        FROM lwtdemo.script_records 
                        WHERE title = '{title_id}';"""
    sql_statement = text(text_statement)
    records = db.execute(sql_statement)
    rows = [row._asdict() for row in records]
    return rows


@app.get("/data/summary", description="Get overall summary of the records in the system.")
def show_summary_records(db: Session = Depends(get_db)):
    """
        Returns:
        - The summarized results for records in the scripts table
        """
    text_statement = """SELECT CONCAT(ROUND(AVG(sadness_score)*100,2),'%') as avg_sadness, 
                    CONCAT(ROUND(AVG(joy_score)*100,2),'%') as avg_joy, 
                    CONCAT(ROUND(AVG(love_score)*100,2),'%') as avg_love, 
                    CONCAT(ROUND(AVG(anger_score)*100,2),'%') as avg_anger, 
                    CONCAT(ROUND(AVG(fear_score)*100,2),'%') as avg_fear, 
                    CONCAT(ROUND(AVG(surprise_score)*100,2),'%') as avg_surprise, 
                    COUNT(*) AS total_count, 
                    COUNT(DISTINCT title) AS distinct_record_count
                    from lwtdemo.script_records;"""
    sql_statement = text(text_statement)
    records = db.execute(sql_statement)
    rows = [row._asdict() for row in records]
    return rows



@app.get("/data/summary_year", description="Get overall summary of the records in the system by year.")
def show_summary_records(db: Session = Depends(get_db)):
    """
        Returns:
        - The summarized results for records in the scripts table by year
        """
    text_statement = """SELECT ROUND(AVG(sadness_score)*100,2)::float as avg_sadness, 
                    ROUND(AVG(joy_score)*100,2)::float as avg_joy, 
                    ROUND(AVG(love_score)*100,2)::float as avg_love, 
                    ROUND(AVG(anger_score)*100,2)::float as avg_anger, 
                    ROUND(AVG(fear_score)*100,2)::float as avg_fear, 
                    ROUND(AVG(surprise_score)*100,2)::float as avg_surprise, 
                    COUNT(*) AS total_count, 
                    COUNT(DISTINCT title) AS distinct_record_count,
                    date_info_corr 
                    FROM lwtdemo.script_records
                    GROUP BY date_info_corr s
                    ORDER BY date_info_corr;"""
    sql_statement = text(text_statement)
    records = db.execute(sql_statement)
    rows = [row._asdict() for row in records]
    return rows


@app.get("/data/charts", response_class=HTMLResponse)
async def upload_file(request: Request,
                      data: list = Depends(show_summary_records)):
    chart_data_for_google_charts = []
    header_data = ["Year", "Sadness", "Joy", "Love", "Anger", "Fear", "Surprise"]
    chart_data_for_google_charts.append(header_data)
    for row in data:
        row_as_list = [row['date_info_corr'], row['avg_sadness'], row['avg_joy'], row['avg_love'], row['avg_anger'], row['avg_fear'], row['avg_surprise']]
        chart_data_for_google_charts.append(row_as_list)
    return templates.TemplateResponse("charts.html", {"request": request, "charts": chart_data_for_google_charts})



@app.get("/data/joy", description="Get filtered results for joy. Optional query params: "
                                  "'gte' (greater than or equal to) score or 'lte' (less than or equal to) score: float."
                                  "One, neither, but not both are accepted.")
def show_records(gte: float = None,
                 lte: float = None,
                 db: Session = Depends(get_db)):
    """
        Retrieve filtered results for joy.

        - **gte**: An optional decimal parameter for joy scores greater than or equal to value i.e. 0.12.
        - **lte**: An optional decimal parameter for joy scores less than or equal to value i.e. 0.12.

        Only one of gte or lte should be provided.

        Returns:
        - The results for joy score
        """
    if gte and lte:
        raise HTTPException(status_code=400, detail="One parameter of gte or lte should be provided, not both")
    elif gte and not lte:
        where_statement = f"""WHERE joy_score >= {gte}"""
    elif lte and not gte:
        where_statement = f"""WHERE joy_score <= {lte}"""
    else:
        where_statement = ""
    text_statement = f"""SELECT id, 
                               title, 
                               date_info, 
                               sentence, 
                               sadness_score, 
                               joy_score, 
                               love_score, 
                               anger_score, 
                               fear_score,
                               surprise_score 
                           FROM lwtdemo.script_records """ + where_statement
    sql_statement = text(text_statement)
    records = db.execute(sql_statement)
    rows = [row._asdict() for row in records]
    return rows


@app.get("/data/anger", description="Get filtered results for anger. Optional query params: "
                                  "'gte' (greater than or equal to) score or 'lte' (less than or equal to) score: float."
                                  "One, neither, but not both are accepted.")
def show_records_anger(gte: float = None,
                 lte: float = None,
                 db: Session = Depends(get_db)):
    """
        Retrieve filtered results for anger.

        - **gte**: An optional decimal parameter for scores greater than or equal to value i.e. 0.12.
        - **lte**: An optional decimal parameter for scores less than or equal to value i.e. 0.12.

        Only one of gte or lte should be provided.

        Returns:
        - The results for anger score
        """
    if gte and lte:
        raise HTTPException(status_code=400, detail="One parameter of gte or lte should be provided, not both")
    elif gte and not lte:
        where_statement = f"""WHERE anger_score >= {gte}"""
    elif lte and not gte:
        where_statement = f"""WHERE anger_score <= {lte}"""
    else:
        where_statement = ""
    text_statement = f"""SELECT id, 
                               title, 
                               date_info, 
                               sentence, 
                               sadness_score, 
                               joy_score, 
                               love_score, 
                               anger_score, 
                               fear_score,
                               surprise_score 
                           FROM lwtdemo.script_records """ + where_statement
    sql_statement = text(text_statement)
    records = db.execute(sql_statement)
    rows = [row._asdict() for row in records]
    return rows


@app.get("/data/love", description="Get filtered results for love. Optional query params: "
                                  "'gte' (greater than or equal to) score or 'lte' (less than or equal to) score: float."
                                  "One, neither, but not both are accepted.")
def show_records_love(gte: float = None,
                     lte: float = None,
                     db: Session = Depends(get_db)):
    """
        Retrieve filtered results for love.

        - **gte**: An optional decimal parameter for scores greater than or equal to value i.e. 0.12.
        - **lte**: An optional decimal parameter for scores less than or equal to value i.e. 0.12.

        Only one of gte or lte should be provided.

        Returns:
        - The results for love score
        """
    if gte and lte:
        raise HTTPException(status_code=400, detail="One parameter of gte or lte should be provided, not both")
    elif gte and not lte:
        where_statement = f"""WHERE love_score >= {gte}"""
    elif lte and not gte:
        where_statement = f"""WHERE love_score <= {lte}"""
    else:
        where_statement = ""
    text_statement = f"""SELECT id, 
                               title, 
                               date_info, 
                               sentence, 
                               sadness_score, 
                               joy_score, 
                               love_score, 
                               anger_score, 
                               fear_score,
                               surprise_score 
                           FROM lwtdemo.script_records """ + where_statement
    sql_statement = text(text_statement)
    records = db.execute(sql_statement)
    rows = [row._asdict() for row in records]
    return rows


@app.get("/data/fear", description="Get filtered results for fear. Optional query params: "
                                  "'gte' (greater than or equal to) score or 'lte' (less than or equal to) score: float."
                                  "One, neither, but not both are accepted.")
def show_records_fear(gte: float = None,
                     lte: float = None,
                     db: Session = Depends(get_db)):
    """
        Retrieve filtered results for fear.

        - **gte**: An optional decimal parameter for scores greater than or equal to value i.e. 0.12.
        - **lte**: An optional decimal parameter for scores less than or equal to value i.e. 0.12.

        Only one of gte or lte should be provided.

        Returns:
        - The results for fear score
        """
    if gte and lte:
        raise HTTPException(status_code=400, detail="One parameter of gte or lte should be provided, not both")
    elif gte and not lte:
        where_statement = f"""WHERE fear_score >= {gte}"""
    elif lte and not gte:
        where_statement = f"""WHERE fear_score <= {lte}"""
    else:
        where_statement = ""
    text_statement = f"""SELECT id, 
                               title, 
                               date_info, 
                               sentence, 
                               sadness_score, 
                               joy_score, 
                               love_score, 
                               anger_score, 
                               fear_score,
                               surprise_score 
                           FROM lwtdemo.script_records """ + where_statement
    sql_statement = text(text_statement)
    records = db.execute(sql_statement)
    rows = [row._asdict() for row in records]
    return rows


@app.get("/data/surprise", description="Get filtered results for surprise. Optional query params: "
                                  "'gte' (greater than or equal to) score or 'lte' (less than or equal to) score: float."
                                  "One, neither, but not both are accepted.")
def show_records_surprise(gte: float = None,
                     lte: float = None,
                     db: Session = Depends(get_db)):
    """
        Retrieve filtered results for surprise.

        - **gte**: An optional decimal parameter for scores greater than or equal to value i.e. 0.12.
        - **lte**: An optional decimal parameter for scores less than or equal to value i.e. 0.12.

        Only one of gte or lte should be provided.

        Returns:
        - The results for surprise score
        """
    if gte and lte:
        raise HTTPException(status_code=400, detail="One parameter of gte or lte should be provided, not both")
    elif gte and not lte:
        where_statement = f"""WHERE surprise_score >= {gte}"""
    elif lte and not gte:
        where_statement = f"""WHERE surprise_score <= {lte}"""
    else:
        where_statement = ""
    text_statement = f"""SELECT id, 
                               title, 
                               date_info, 
                               sentence, 
                               sadness_score, 
                               joy_score, 
                               love_score, 
                               anger_score, 
                               fear_score,
                               surprise_score 
                           FROM lwtdemo.script_records """ + where_statement
    sql_statement = text(text_statement)
    records = db.execute(sql_statement)
    rows = [row._asdict() for row in records]
    return rows

@app.get("/data/sadness", description="Get filtered results for sadness. Optional query params: "
                                  "'gte' (greater than or equal to) score or 'lte' (less than or equal to) score: float."
                                  "One, neither, but not both are accepted.")
def show_records_sadness(gte: float = None,
                         lte: float = None,
                         db: Session = Depends(get_db)):
    """
        Retrieve filtered results for sadness.

        - **gte**: An optional decimal parameter for scores greater than or equal to value i.e. 0.12.
        - **lte**: An optional decimal parameter for scores less than or equal to value i.e. 0.12.

        Only one of gte or lte should be provided.

        Returns:
        - The results for sadness
        """
    if gte and lte:
        raise HTTPException(status_code=400, detail="One parameter of gte or lte should be provided, not both")
    elif gte and not lte:
        where_statement = f"""WHERE sadness_score >= {gte}"""
    elif lte and not gte:
        where_statement = f"""WHERE sadness_score <= {lte}"""
    else:
        where_statement = ""
    text_statement = f"""SELECT id, 
                               title, 
                               date_info, 
                               sentence, 
                               sadness_score, 
                               joy_score, 
                               love_score, 
                               anger_score, 
                               fear_score,
                               surprise_score 
                           FROM lwtdemo.script_records """ + where_statement
    sql_statement = text(text_statement)
    records = db.execute(sql_statement)
    rows = [row._asdict() for row in records]
    return rows