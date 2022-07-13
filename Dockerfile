FROM python:3.10-alpine
WORKDIR ./code

RUN pip install --upgrade pip
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./App /code/App
CMD ["uvicorn", "App.main:app", "--host", "0.0.0.0", "--port", "80"]
