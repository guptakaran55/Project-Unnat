# docker-compose.yml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - REDIS_URL=redis://redis:6379
      - DATABASE_URL=postgresql://user:pass@db:5432/buildingdb
    depends_on:
      - redis
      - db

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"


  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=buildingdb
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/ssl
    depends_on:
      - web

  celery:
    build: .
    command: celery -A app.celery worker --loglevel=info
    environment:
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis

volumes:
  postgres_data: