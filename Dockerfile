FROM python:3
ENV PYTHONUNBUFFERED 1
MAINTAINER olha.rysovana@gmail.com

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
RUN invoke startup

EXPOSE 8000
ENTRYPOINT python3 manage.py runserver 0.0.0.0:8000
