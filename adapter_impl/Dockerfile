FROM python:3.9
WORKDIR /app

COPY ./adapter_impl/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./adapter_impl/adapter.py ./adapter_impl/db_func.py .

CMD ["python", "adapter.py"]
