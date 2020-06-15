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
$ pipenv run python mange.py db init
$ pipenv run python mange.py db migrate
$ pipenv run python mange.py db upgrade
```
- run the app
```bash
$ pipenv run flask run
```
- or
```bash
$ pipenv run flask run --cert=adhoc
```
