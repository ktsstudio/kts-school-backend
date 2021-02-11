cat config/heroku_config.yaml | envsubst > config/config.yaml
# необходимо для того, чтобы alembic смог найти наше приложение
export PYTHONPATH=.
alembic upgrade head
python main.py