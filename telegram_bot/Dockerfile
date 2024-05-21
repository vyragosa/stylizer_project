
FROM python:3.8-slim

WORKDIR /app


COPY . /app


RUN pip install -r requirements.txt


EXPOSE 8443

ENV TELEGRAM_BOT_TOKEN='6639128192:AAEV_HHQKuIW_CZ-cA8Gie3pC6nidhb8xzA'


CMD ["python", "bot.py"]