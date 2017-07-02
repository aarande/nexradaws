FROM python:3.6

RUN mkdir /app
WORKDIR /app

COPY requirements_devel.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app
