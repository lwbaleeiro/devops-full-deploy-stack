FROM python:3.11-slim

WORKDIR /app

# O buffer do python precisa ser desativado para os logs aparecerem instantaneamente no docker logs
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

CMD ["python", "main.py"]
