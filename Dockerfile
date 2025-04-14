FROM python:3.10-slim

ADD .bashrc /root/

COPY requirements.txt /app/requirements.txt

COPY app.py /app/app.py

WORKDIR /app

RUN mkdir -p app/_logs

RUN pip install --no-cache-dir -r requirements.txt

CMD python ./app.py
