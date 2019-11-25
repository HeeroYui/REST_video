FROM python:alpine

RUN pip install --upgrade pip

RUN pip install flask

RUN pip install flask_restful

RUN pip install python-dateutil

RUN pip install realog

EXPOSE 80

ADD src /application/
WORKDIR /application/
CMD ["python", "-u", "./app_video.py"]



