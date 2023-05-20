FROM python:3.8-slim-buster

RUN apt-get update && apt-get install -y \
    libaio1 \ 
    && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y unzip 
ADD https://download.oracle.com/otn_software/linux/instantclient/199000/instantclient-basic-linux.x64-19.9.0.0.0dbru.zip /tmp/
ADD https://download.oracle.com/otn_software/linux/instantclient/199000/instantclient-sdk-linux.x64-19.9.0.0.0dbru.zip /tmp/
RUN unzip /tmp/instantclient-basic-linux.x64-19.9.0.0.0dbru.zip -d /usr/local/
RUN unzip /tmp/instantclient-sdk-linux.x64-19.9.0.0.0dbru.zip -d /usr/local/
ENV LD_LIBRARY_PATH /usr/local/instantclient_19_9
RUN pip install --upgrade pip
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
COPY . /app/
WORKDIR /app
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
