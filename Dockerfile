FROM python:3.7-slim-stretch

RUN apt-get update && apt-get install -y git python3-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt --upgrade

COPY app app/

RUN python app/server.py

RUN set FLASK_APP=flaskr
RUN flask init-db
RUN flask RUN

EXPOSE 5042

CMD ["python", "app/server.py", "serve"]