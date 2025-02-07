#
FROM python:3.9-slim

#
WORKDIR /Api/dash_nintendo_app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt


CMD ["python", "app.py"]