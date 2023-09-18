# Getting Started

```
docker compose --build
docker compose up -d
docker compose exec demo-app poetry run python -m api.migrate_db
```

# How to test

```
docker compose exec demo-app poetry run pytest -s -p no:warnings -v
```

