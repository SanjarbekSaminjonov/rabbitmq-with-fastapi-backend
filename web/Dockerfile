FROM python:3.11.0

WORKDIR /app

COPY ./requirements.txt ./requirements.txt

# cache packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8555
