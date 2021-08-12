FROM python:3.8-buster
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5001
CMD ["/bin/bash", "-c", "gunicorn --bind 0.0.0.0:5001 api:__hug_wsgi__"]
