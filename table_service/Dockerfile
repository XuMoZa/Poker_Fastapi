FROM python:3.13-slim

WORKDIR /table_app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8002
CMD ["uvicorn", "table_app.main:app", "--host", "0.0.0.0", "--port", "8002", "--reload"]