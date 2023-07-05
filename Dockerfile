FROM nickgryg/alpine-pandas:latest
RUN apk update
RUN apk add py-pip
RUN apk add build-base
RUN apk add --no-cache python3-dev 
RUN pip install --upgrade pip
WORKDIR /app
COPY . /app
RUN pip install -r reqs.txt
RUN apk del build-base
CMD ["python3", "api/main.py"]