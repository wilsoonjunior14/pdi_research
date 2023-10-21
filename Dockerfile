FROM ubuntu/apache2

WORKDIR /var/www/html

RUN apt-get update --fix-missing -y
RUN apt-get install pip -y
RUN apt-get install python3-opencv python3-numpy python3-scipy python3-matplotlib -y
RUN apt-get install python3-sklearn
