# syntax=docker/dockerfile:1
FROM python:3.10.6-slim-buster 
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-b", ":5000", "wsgi:server"]