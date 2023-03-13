FROM ubuntu/apache2

COPY ./requirements.txt /var/www/html/requirements.txt
WORKDIR /var/www/html

RUN apt-get update -y
RUN apt-get install pip -y
RUN apt-get install python3-opencv -y
RUN pip install -r requirements.txt
