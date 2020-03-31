FROM python:3.7

RUN apt-get update && \
    apt-get install -y gcc make apt-transport-https ca-certificates build-essential

WORKDIR  /opt/cerebro

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /opt/cerebro

CMD ["python3", "/opt/cerebro/src/face_reco_api.py"]