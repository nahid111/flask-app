# Flask App


## installation
- install pipenv
```bash
$ sudo -H pip3 install -U pipenv
```
- clone the repo & cd into it
- install dependencies
```bash
$ pipenv install
```
- Copy & rename .env.example file to .env
- Set the database credentials inside .env
- Make DB Migrations - 
```bash
$ pipenv run python manage.py db init
$ pipenv run python manage.py db migrate
$ pipenv run python manage.py db upgrade
```
- run the app
```bash
$ pipenv run flask run
```
- or
```bash
$ pipenv run flask run --cert=adhoc
```
- or
```bash
$ pipenv run gunicorn -b 0.0.0.0:5000 --access-logfile - --reload "app:create_app()"
```


## in case
- generate requirements.txt
```bash
$ pipenv lock -r > requirements.txt
```

## Run with Docker
- Make sure [Docker](https://docs.docker.com/install/ "Docker") & [Docker-Compose](https://docs.docker.com/compose/install/ "Docker-Compose") are installed
- run
```bash
$ docker-compose up -d
```
- exec into the app container and make DB migrations
```bash
$ docker exec -it CONTAINER_ID bash
```
- see app logs
```bash
$ docker logs -f CONTAINER_ID
```
- clean up
```bash
$ docker-compose down -v
```