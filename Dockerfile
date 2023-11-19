FROM python:3.10.6-slim

WORKDIR /opt/app
COPY req.txt .
RUN pip install -r req.txt

COPY bot.py .

ENTRYPOINT [ "python", "bot.py" ]