FROM python:3.11-slim

WORKDIR /api

COPY ./requirements.txt /api/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade pip

COPY ./app /api/app
COPY ./helpers /api/helpers
COPY ./modules /api/modules

ENTRYPOINT ["sh", "-c", "uvicorn app.main:app --proxy-headers --host 0.0.0.0 --port $PORT"]
