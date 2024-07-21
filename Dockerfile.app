FROM python:3.10.6-slim-buster 
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD [ "gunicorn", "--workers=1", "--threads=1", "-b 0.0.0.0:5000", "callbacks:index.app"]