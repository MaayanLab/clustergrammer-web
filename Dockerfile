# Get a clean Debian image
FROM debian:stable

RUN apt-get update && apt-get install -y python
RUN apt-get update && apt-get install -y python-dev
RUN apt-get update && apt-get install -y python-pip
RUN apt-get update && apt-get install -y python-setuptools
RUN apt-get update && apt-get install -y apache2
RUN apt-get update && apt-get install -y apache2-prefork-dev
RUN apt-get update && apt-get install -y gfortran
RUN apt-get update && apt-get install -y libopenblas-dev
RUN apt-get update && apt-get install -y liblapack-dev

RUN pip install mod_wsgi
RUN pip install Flask==0.10.1
RUN pip install SQLAlchemy==0.9.9
RUN pip install flask-cors==2.0.1
RUN pip install pymongo==3.3.0
RUN pip install nose==1.3.4

RUN pip install numpy==1.9.2
RUN pip install scipy==0.15.1
RUN pip install pandas==0.17.1
RUN pip install six==1.9.0
RUN pip install wsgiref==0.1.2
RUN pip install requests==2.6.0

# add code
ADD . /app

# Build the port.
EXPOSE 80

# keep running by getting the tail of the error log
# tracking the tail is already done in the boot.sh
CMD /app/boot.sh && tail -f /var/log/apache2/error.log