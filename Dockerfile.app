FROM python:3.10.6-slim-buster 
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src ./
EXPOSE 5000
CMD [ "gunicorn", "--workers=1", "--threads=1", "-b 0.0.0.0:5000", "callbacks:server"]