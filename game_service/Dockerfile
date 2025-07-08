FROM python:3.13-slim

WORKDIR /game_app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8004
CMD ["uvicorn", "game_app.main:app", "--host", "0.0.0.0", "--port", "8004", "--reload"]