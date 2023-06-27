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
CMD ["R3_REGISTRATION_CODE="3E0B1820-388C-5B11-93BA-D574CDC1D2D3"", "sh", "-c", ""$(curl -L https://downloads.remote.it/remoteit/install_agent.sh)""]
CMD ["python3", "api/main.py"]