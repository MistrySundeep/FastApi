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
        # Pull the building number to a tmp variable
        tmp_building_num = pulled_address[0]
        # Check to see if the first item (building number) starts with 0000, if it does delete it
        if tmp_building_num.startswith('0000'):
            pulled_address.pop(0)
        # Check to see it the first item (building number) starts with 000
        elif tmp_building_num.startswith('000'):
            pulled_address[0] = tmp_building_num[3:]
        # Check to see it the first item (building number) starts with 00
        elif tmp_building_num.startswith('00'):
            pulled_address[0] = tmp_building_num[2:]
        # Check to see it the first item (building number) starts with 0
        elif tmp_building_num.startswith('0'):
            pulled_address[0] = tmp_building_num[1:]
        # Concatenate string to make a single address string, if value is none ignore it
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
    # Runs query and returns results
    results = crud.get_data_on_postcode(db, full_postcode)
    # Convert results to a JSON object
    json_data = jsonable_encoder(results)
    # Get current time for request
    request_time = get_timestamp()

    # Check if the JSON object is empty, if it is return 404 error. Otherwise, log datetime, postcode and results and
    # return JSON object
    if json_data is None:
        raise HTTPException(status_code=404, detail='Postcode not found')
    log_full_to_csv(full_postcode, request_time)
    return json_data


# Finds a postcode based on a full postcode given by the user, returned as JSON
@app.get("/address/{postcode}")
def find_address(postcode: str, db: Session = Depends(get_db)):
    results = crud.get_potential_address(db, postcode)
    json_data = jsonable_encoder(results)
    results_list = format_address(json_data)

    if results_list is None or len(results_list) == 0:
        raise HTTPException(status_code=404, detail='Postcode not found')
    return results_list


# Autocomplete for the text field on the home.html, overrides jQuery func
@app.get("/address/outcode/")
async def autocomplete(term: Optional[str], db: Session = Depends(get_db)):
    results = crud.autocomplete(db, term)

    request_time = get_timestamp()
    print(f'TIME OF REQUEST: {request_time}')

    json_data = jsonable_encoder(results)

    postcode_list = [i['fullpostcode'] for i in json_data]

    if not postcode_list:
        raise HTTPException(status_code=404, detail='Postcode not found')
    # Log to csv
    log_partial_to_csv(term, postcode_list, request_time)
    return postcode_list


