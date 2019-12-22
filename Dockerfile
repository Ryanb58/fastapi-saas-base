FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

ADD ./requirements.txt /app
RUN pip install --no-cache-dir --upgrade pip
RUN pip install -r requirements.txt

ADD ./ /app
WORKDIR /app/


ENV PYTHONPATH=/app

EXPOSE 80
