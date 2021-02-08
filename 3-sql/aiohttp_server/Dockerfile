FROM python:3.7
# gettext-base нужен для того, чтобы установить envsubst
RUN apt update && apt -y install gettext-base
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
# подставляем переменные из окружения в подготовленный конфиг
RUN cat config/heroku_config.yaml | envsubst > config/config.yaml
CMD ["./run.sh"]
