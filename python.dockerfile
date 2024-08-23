FROM python:3

WORKDIR /usr/src/app/
EXPOSE 8000

RUN apt-get update

RUN pip install pyjwt
RUN pip install fastapi
RUN pip install uvicorn
RUN pip install "passlib[bcrypt]"
RUN pip install datetime
RUN pip install cryptography
RUN pip install sqlalchemy
RUN pip install python-multipart
