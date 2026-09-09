FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir .
CMD ["sh","-c","exec gunicorn --bind :${PORT:-8080} --workers 1 --threads 8 --timeout 900 main:app"]
