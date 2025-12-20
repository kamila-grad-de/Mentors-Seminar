## Сборка
```bash
docker build -t todo ./todo
docker run -d -p 8000:80 -v todo_data:/app/data todo
```

## Запуск
```bash
docker build -t shorturl ./shorturl
docker run -d -p 8001:80 -v shorturl_data:/app/data shorturl
```