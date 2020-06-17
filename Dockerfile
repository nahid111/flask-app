FROM python:3.8-slim
LABEL MAINTAINER="Muhammad Nahid"
LABEL "Maintainer email"="mdnahid22@gmail.com"
LABEL version="1.0"

# set env var
ENV INSTALL_PATH /opt/flask_app
# create app directory
RUN mkdir -p $INSTALL_PATH
# set the app directory as Work Directory
WORKDIR $INSTALL_PATH

# copy the requirements.txt inside workdir
COPY requirements.txt requirements.txt
#  install dependencies
RUN pip install -r requirements.txt
# copy all files to workdir
COPY . .

# run app
# CMD gunicorn -b 0.0.0.0:8000 --access-logfile - "app.app:create_app()"
CMD flask run
