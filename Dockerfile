FROM python:3.7

WORKDIR  /opt/cerebro/

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "/opt/cerebro/src/flask_api.py"]
