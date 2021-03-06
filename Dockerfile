#USING PYTHON 3.8.5 VERSION
FROM python:3.8.5-slim-buster
#INSTALLING wkhtml2pdf, THAT GENERATES DE REPORTS
RUN apt-get update && apt-get install --no-install-recommends -y wkhtmltopdf 
#COPYING FILES TO DOCKER CONTAINER & INSTALLING PYTHON LIBRARIES
COPY . /app/
WORKDIR /app
RUN pip install -r requirements.txt
#CREATION OF ALL THE DB MODELS
RUN python dbcreate.py 
#FLASK ENV VARIABLE TO RUN THE SERVER IN PRODUCTION
ENV FLASK_ENV=production

#EXPOSE THE PORT 5000 OF THE CONTAINER TO THE PORT 80
EXPOSE 80:5000
#RUN GUNICORN WEBSERVER
CMD gunicorn --bind 0.0.0.0:5000 wsgi:app