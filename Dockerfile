FROM python:3.11

WORKDIR /api

COPY ./requirements.txt /api/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade pip

COPY ./app /api/app
COPY ./helper /api/helper
COPY ./modules /api/modules

ENTRYPOINT ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT"]
