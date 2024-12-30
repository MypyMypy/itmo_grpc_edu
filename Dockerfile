FROM python:3

WORKDIR /app

COPY ./app ./app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN python -m grpc_tools.protoc -I./app --python_out=./app --grpc_python_out=./app ./app/glossary.proto

CMD ["python", "main.py"]
