from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import App.crud as crud
import App.helper_functions as hf
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


# Serves a base html file where you can access the different APIs
# @app.get("/") tells FastAPI that the func below handles request at path "/" using GET
@app.get("/")
async def serve_index(request: Request, db: Session = Depends(get_db)):
    # Runs a validation check to see if the auth headers are valid
    # flag = crud.authentication(request, db)
    #
    # if not flag:
    #     raise HTTPException(status.HTTP_403_FORBIDDEN, detail='Forbidden')
    return templates.TemplateResponse('index.html', {'request': request})


@app.get("/fullpostcode/{full_postcode}")
async def full_postcode_info(request: Request, full_postcode: str, db: Session = Depends(get_db)):
    # Runs a validation check to see if the auth headers are valid
    flag = crud.authentication(request, db)

    if not flag:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail='Forbidden')
    # Runs query and returns results
    results = crud.get_data_on_postcode(db, full_postcode)
    # Convert results to a JSON object
    json_data = jsonable_encoder(results)
    # Get current time for request
    request_time = hf.get_timestamp()

    # Check if the JSON object is empty, if it is return 404 error. Otherwise, log datetime, postcode and results and
    # return JSON object
    if json_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Postcode not found')
    hf.log_full_to_csv(full_postcode.upper(), request_time)
    return json_data


# Finds a postcode based on a full postcode given by the user, returned as JSON
@app.get("/address/{postcode}")
def find_address(request: Request, postcode: str, db: Session = Depends(get_db)):
    # Runs a validation check to see if the auth headers are valid
    flag = crud.authentication(request, db)
    if not flag:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail='Forbidden')

    results = crud.get_potential_address(db, postcode)
    json_data = jsonable_encoder(results)
    results_list = hf.format_address(json_data)

    if results_list is None or len(results_list) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Postcode not found')

    return results_list


# Autocomplete for the text field on the home.html, overrides jQuery func
@app.get("/address/outcode/")
async def autocomplete(request: Request, term: Optional[str], db: Session = Depends(get_db)):
    # Runs a validation check to see if the auth headers are valid
    flag = crud.authentication(request, db)

    if not flag:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail='Forbidden')
    results = crud.autocomplete(db, term)

    request_time = hf.get_timestamp()
    print(f'TIME OF REQUEST: {request_time}')

    json_data = jsonable_encoder(results)

    postcode_list = [i['fullpostcode'] for i in json_data]

    if not postcode_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Postcode not found')
    # Log to csv
    hf.log_partial_to_csv(term, postcode_list, request_time)
    return postcode_list
