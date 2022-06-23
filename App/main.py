from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import App.crud as crud
from App.db import SessionLocal, engine
from App.model import Base
from typing import Optional
from datetime import datetime
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
import csv

Base.metadata.create_all(bind=engine)
# An instance of class FastAPI which becomes the main point of interaction of APIs
app = FastAPI()

# Sets the directory for the html files
templates = Jinja2Templates(directory='App/html')
# Mounts the folder static so fastapi can find the js file
app.mount("/static", StaticFiles(directory="App/static"), name="static")


# Creates a connection to the db, run each time a func is called
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Used to create a timestamp when a query is made, for now prints to termianl
def get_timestamp():
    dt = datetime.now()
    dt_now = str(dt)
    return dt_now[:-7]


# Write to csv file
def log_to_csv(term: str, postcode_list: list, date: str):
    with open('App/results.csv', 'a', encoding='UTF-8', newline='') as file:

        writer = csv.writer(file)
        writer.writerow([term, len(postcode_list), date])
        print(f'{term}, {len(postcode_list)}, {date}')


# Serves a base html file where you can access the different APIs
# @app.get("/") tells FastAPI that the func below handles request at path "/" using GET
@app.get("/")
async def serve_index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


# Finds a postcode based on a full postcode given by the user, returned as JSON
@app.get("/address/{postcode}")
async def read_postcode(postcode: str, db: Session = Depends(get_db)):
    results = crud.get_postcode(db, postcode)
    request_time = get_timestamp()
    print(f'TIME OF REQUEST TEST: {request_time}')
    json_data = jsonable_encoder(results)

    if json_data is None:
        raise HTTPException(status_code=404, detail="Postcode not found")
    return json_data


# Autocomplete for the text field on the home.html, overrides jQuery func
@app.get("/address/outcode/")
async def autocomplete(term: Optional[str], db: Session = Depends(get_db)):
    results = crud.get_postcode_from_outcode(db, term)

    request_time = get_timestamp()
    print(f'TIME OF REQUEST: {request_time}')

    json_data = jsonable_encoder(results)

    postcode_list = [i['fullpostcode'] for i in json_data]

    if json_data is None:
        raise HTTPException(status_code=404, detail='Postcode not found')
    # Log to csv
    log_to_csv(term, postcode_list, request_time)
    return postcode_list
