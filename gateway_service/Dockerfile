FROM python:3.13-slim

WORKDIR /gateway_app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
COPY . .
EXPOSE 8000
CMD ["uvicorn", "gateway_app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]