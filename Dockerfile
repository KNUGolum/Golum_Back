FROM python:3.11-slim

WORKDIR /app

# 시스템 의존성 설치 (PostgreSQL 연결용)
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 실행 명령은 docker-compose에서 제어하므로 비워두거나 기본값 설정
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]