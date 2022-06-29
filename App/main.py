import csv
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import null
from sqlalchemy.orm import Session

import App.crud as crud
from App.db import SessionLocal, engine
from App.model import Base

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
def log_partial_to_csv(term: str, postcode_list: list, date: str):
    with open('results.csv', 'a', encoding='UTF-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([term.upper(), len(postcode_list), date])
        print(f'{term}, {len(postcode_list)}, {date}')


# Write to csv file
def log_full_to_csv(postcode: str, date: str):
    with open('results.csv', 'a', encoding='UTF-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([postcode.upper(), 1, date])
        print(f'{postcode}, 1, {date}')


def format_address(address):
    tmp_dict = {}
    final_address = []

    for i in range(len(address)):
        # Taking first dict from the list and looping through that
        tmp_dict = address[i]
        # Looping through the vals in tmp_dict and adding them to a new list
        pulled_address = [tmp_dict[v] for v in tmp_dict if type(tmp_dict[v]) != type(null)]
        # Check to see if the first item (building number) starts with 0
        tmp_building_num = pulled_address[0]
        if tmp_building_num.startswith('0000'):
            pulled_address.pop(0)
        elif tmp_building_num.startswith('000'):
            pulled_address[0] = tmp_building_num[3:]
        elif tmp_building_num.startswith('00'):
            pulled_address[0] = tmp_building_num[2:]
        elif tmp_building_num.startswith('0'):
            pulled_address[0] = tmp_building_num[1:]
        # Concatenate string to make a single address string
        res = ' '.join(filter(lambda x: x if x is not None else '', pulled_address))
        # Insert new string into final_list
        final_address.insert(i, res)
        # Clear the tmp_dict
        tmp_dict.clear()
        # Clear res
        res = ''

    return final_address


# Serves a base html file where you can access the different APIs
# @app.get("/") tells FastAPI that the func below handles request at path "/" using GET
@app.get("/")
async def serve_index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.get("/fullpostcode/{full_postcode}")
async def full_postcode_info(full_postcode: str, db: Session = Depends(get_db)):
    results = crud.get_data_on_postcode(db, full_postcode)

    json_data = jsonable_encoder(results)
    request_time = get_timestamp()

    if json_data is None:
        raise HTTPException(status_code=404, detail='Postcode not found')
    log_full_to_csv(full_postcode, request_time)
    return json_data


# Finds a postcode based on a full postcode given by the user, returned as JSON
@app.get("/address/{postcode}")
async def find_address(postcode: str, db: Session = Depends(get_db)):
    results = crud.get_potential_address(db, postcode)
    json_data = jsonable_encoder(results)
    results_list = format_address(json_data)
    for i in results_list:
        print(i)

    if results_list is None:
        raise HTTPException(status_code=404, detail='Postcode not found')
    return results_list


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
    log_partial_to_csv(term, postcode_list, request_time)
    return postcode_list
