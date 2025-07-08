FROM python:3.13-slim

WORKDIR /user_app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8003
CMD ["uvicorn", "user_app.main:app", "--host", "0.0.0.0", "--port", "8003", "--reload"]