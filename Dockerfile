# Get a clean Debian image
FROM debian:stable

# Get the latest available repos.
RUN apt-get update

# Install Python as well as the dev version and toolchain.
RUN apt-get -y install python
RUN apt-get -y install python-dev
RUN apt-get -y install python-pip
RUN apt-get -y install python-setuptools

# Install Apache and Apache dev; the latter is used for recompiling for
# mod_wsgi.
RUN apt-get -y install apache2
RUN apt-get -y install apache2-prefork-dev
RUN pip install mod_wsgi

# Get application-specific dependencies.
RUN pip install -Iv Flask==0.10.1
RUN pip install -Iv SQLAlchemy==0.9.9
RUN pip install -Iv mysql-connector-python==2.0.3
RUN pip install -Iv nose==1.3.4
RUN pip install -Iv numpy==1.9.2
RUN pip install -Iv requests==2.6.0
RUN apt-get -y install gfortran libopenblas-dev liblapack-dev
RUN pip install -Iv singledispatch==3.4.0.3
RUN pip install -Iv six==1.9.0
RUN pip install -Iv wsgiref==0.1.2
RUN pip install poster

# use apt-get to install scipy
RUN apt-get -y install python-numpy python-scipy python-matplotlib 

RUN pip install pandas==0.17.1

RUN pip install pymongo
RUN pip install -Iv flask-cors==2.0.1

# add code
ADD . /app


# Build the port.
EXPOSE 80

# keep running by getting the tail of the error log 
# tracking the tail is already done in the boot.sh 
CMD /app/boot.sh && tail -f /var/log/apache2/error.log