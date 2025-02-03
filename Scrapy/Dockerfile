#Image de base python pour le Dockerfile\
FROM python:3.9-slim

WORKDIR /app/Scrapy

COPY requirements.txt . 

RUN pip install -r requirements.txt 

COPY . . 

CMD ["scrapy", "crawl", "nintendo_games"]