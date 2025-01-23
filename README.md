py src/workers/sync_workers.py
http://127.0.0.1:8000/customers/
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
docker-compose -f docker/kafka-docker-compose.yml up -d

