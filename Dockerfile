FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN python -m pip install --upgrade pip && \
    python -m pip install "pymongo[srv]==3.12" && \
    pip install -r requirements.txt
    pip install certifi

COPY . .

CMD ["python3", "main.py"]
