FROM python:3.13-slim

WORKDIR /auth_app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8001
CMD ["uvicorn", "auth_app.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]