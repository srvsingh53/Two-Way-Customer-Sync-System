# Two-Way Customer Sync System

This project implements a two-way customer synchronization system using FastAPI, Kafka, PostgreSQL, and Stripe Webhooks. It allows for synchronization of customer data between an internal database and Stripe in both directions.

## Features

- 📡 **REST API** to create and manage customers.
- ⚙️ **Kafka Integration** for asynchronous processing.
- 🔄 **Two-Way Sync**:
  - **Outward Sync**: API sends data to Kafka for processing.
  - **Inward Sync**: Stripe webhooks update the internal database.
- 💄 **PostgreSQL** for customer data storage.
- 📊 **Logging** for debugging and monitoring.
- 🐥 **Docker** support for easy deployment.

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy
- **Database**: PostgreSQL
- **Messaging Queue**: Apache Kafka
- **Cloud Services**: Stripe API
- **Infrastructure**: Docker, Docker Compose
- **Other**: Pydantic, Ngrok (for testing webhooks)

## Project Structure

```bash
customer-sync/
│-- src/
│   ├── api/
│   │   ├── routes.py            # API endpoints for customer operations
│   │   ├── webhook.py           # Stripe webhook handling
│   ├── database/
│   │   ├── db.py                # Database connection setup
│   │   ├── models.py            # ORM models
│   ├── services/
│   │   ├── kafka_producer.py    # Kafka producer
│   │   ├── kafka_consumer.py    # Kafka consumer
│   ├── workers/
│   │   ├── sync_worker.py       # Worker for processing sync events
│   ├── config/
│   │   ├── settings.py          # Application configuration
│   ├── main.py                  # Entry point
│-- docker/
│   ├── kafka-docker-compose.yml # Kafka and PostgreSQL setup
│-- .env                         # Environment variables
│-- README.md                    # Project documentation
│-- requirements.txt             # Dependencies
│-- Dockerfile                   # Docker configuration
```

## Installation

### Prerequisites

- Python 3.8+
- Docker and Docker Compose
- Ngrok (for webhook testing)
- Stripe account

### Steps to Run the Project Locally

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/customer-sync.git
   cd customer-sync
   ```

2. **Create a virtual environment and install dependencies**:

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:

   Create a `.env` file and add the following:

   ```ini
   DATABASE_URL=postgresql://user:password@localhost:5432/customerdb
   STRIPE_SECRET_KEY=sk_test_xxxxxxxxxxxxx
   STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxx
   KAFKA_BROKER=localhost:9092
   KAFKA_TOPIC=customer-events
   ```

4. **Start services with Docker**:

   ```bash
   docker-compose -f docker/kafka-docker-compose.yml up -d
   ```

5. **Run the FastAPI application**:

   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
   ```

6. **Expose the local server for Stripe webhooks using Ngrok**:

   ```bash
   ngrok http 8000
   ```

7. **Update your Stripe dashboard webhook endpoint**:

   Go to **Stripe Dashboard > Webhooks > Add endpoint** and set it to:
   ```
   https://<your-ngrok-url>/stripe/webhook
   ```

## Usage

### API Endpoints

1. **Check API health**

   ```bash
   GET http://localhost:8000/checking
   ```
   **Response**:
   ```json
   {
     "message": "this endpoint is working"
   }
   ```

2. **Create a new customer**

   ```bash
   POST http://localhost:8000/customers/
   Content-Type: application/json

   {
     "name": "John Doe",
     "email": "john.doe@example.com"
   }
   ```
   **Response**:
   ```json
   {
     "message": "Customer added and queued for sync"
   }
   ```

### Stripe Webhook Setup

1. Log in to your Stripe Dashboard.
2. Go to **Developers > Webhooks > Add endpoint**.
3. Add the Ngrok URL as the webhook endpoint (e.g., `https://<your-ngrok-url>/stripe/webhook`).
4. Select events such as `customer.created` and `customer.updated`.
5. Save the endpoint and copy the **Webhook Secret Key**, then update it in `.env`.

To manually trigger a webhook using Stripe CLI:

```bash
stripe listen --forward-to localhost:8000/stripe/webhook
stripe trigger customer.created
```

## Testing

To run tests:

```bash
pytest tests/
```

Check customer data in the PostgreSQL container:

```bash
docker exec -it <postgres-container-id> psql -U user -d customerdb -c "SELECT * FROM customers;"
```

## Logging

Logging is enabled by default. Modify `src/utils/logger.py` to change the log level or format.

## Docker Usage

To run the application using Docker:

```bash
docker build -t customer-sync .
docker run -p 8000:8000 --env-file .env customer-sync
```

## Known Issues

- Ensure that the Kafka and PostgreSQL containers are running before starting the application.
- If webhooks fail, check the Ngrok tunnel URL and update it in the Stripe dashboard.

## Future Improvements

- Implement authentication and authorization.
- Enhance unit testing with more edge cases.
- Introduce monitoring and alerting.


