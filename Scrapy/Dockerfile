#Image de base python pour le Dockerfile\
FROM python:3.9-slim

WORKDIR /Scrapy

COPY . .

RUN pip install -r requirements.txt 


CMD ["scrapy", "crawl", "nintendo_spider"]