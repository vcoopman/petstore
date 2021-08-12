FROM python:3.8-buster
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["/bin/bash", "-c", "gunicorn --bind 0.0.0.0:5000 api:__hug_wsgi__"]