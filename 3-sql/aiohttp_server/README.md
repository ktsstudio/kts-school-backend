# Aiohttp Server

## Prerequisites
1) Run `python3 -m venv venv`
2) Run `source venv/bin/activate`
3) Run `pip install -r requrements.txt`
4) Create PostgreSQL database
5) Create telegram bot by BotFather and copy token
5) Place `config.yaml` similar to `heroku_config.yaml` to `config/` folder and adjust 
values
6) Run `export PYTHONPATH=.` because sometimes alembic can not find `app` 
7) Run `alembic upgrade head`

## Run
1) Run `python3 main.py`

## Swagger
1) Raw documentation `127.0.0.1:8080/swagger.json`
2) SwaggerUI `127.0.0.1:8080/swagger`

## Deploy
1) Create account on Heroku
2) Install Heroku CLI: 
2) Run `git init`
3) Run `git add . && git commit -m 'initial commit''`
4) Run `heroku create`
5) Login to Heroku registry `heroku container:login`
6) Push container `heroku container:push web`
6) Add PostgreSQL-addon `heroku addons:create heroku-postgresql:hobby-dev`
7) Release last build `heroku container:release web`
8) Open in browser `heroku open`