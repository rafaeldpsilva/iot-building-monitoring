FROM python:3.12-slim

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

CMD ["python", "api/main.py"]