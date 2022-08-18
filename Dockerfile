FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

ENV PYTHONPATH "${PYTHONPATH}:/"
ENV PORT=8000
ENV IS_IN_DOCKER Yes

RUN pip install --upgrade pip

COPY requirements.txt /app/
COPY prestart.sh /app/
COPY alembic.ini /app/
COPY main.py /app/

RUN pip install -r requirements.txt

ADD src /app/src
