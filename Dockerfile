FROM python:3.8
LABEL MAINTAINER="Muhammad Nahid"
LABEL "Maintainer email"="mdnahid22@gmail.com"
LABEL version="1.0"

# set env var
ENV INSTALL_PATH /flask_app
# create app directory
RUN mkdir -p $INSTALL_PATH
# set the app directory as Work Directory
WORKDIR $INSTALL_PATH

# copy the requirements.txt
COPY requirements.txt requirements.txt
#  install dependencies
RUN pip install -r requirements.txt

# copy project files <src> to WORKDIR <dest>
COPY . .

# run app
CMD gunicorn -b 0.0.0.0:8000 --access-logfile - "app:create_app()"

