FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR  /opt/cerebro/

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./data/arcface_r100_v1.zip /root/.insightface/models/arcface_r100_v1.zip

CMD ["python", "/opt/cerebro/src/flask_api.py"]
