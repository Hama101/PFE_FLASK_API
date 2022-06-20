FROM python:3.9

# Environment Varaibles
ENV DISPLAY=:10
RUN apt-get update -y
RUN apt-get install -y python3-pip build-essential python3-dev nginx
RUN apt-get install -y 1ibasound2
RUN pip install -u gunicorn

# Firefox Setup
RUN wget https://ftp.mozilla.org/pub/mozilla.org/firefox/releases/45.0.2/linux-x86_64/en-US/firefox-45.0.2. tar.bz2
RUN tar -xjvf firefox".tar.bz2
RUN mv firefox /opt/firefox
RUN In -sf /opt/firefox/firefox /usr/bin/firefox

# xvfb install
RUN apt-get install -y xvfb

# Make working directory
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app

# Install requirements
RUN pip install -r requirements.txt

# Copy project to docker work directory
ADD . /app
EXPOSE 5056
ENTRYPOINT ["sh", "start.sh"]
