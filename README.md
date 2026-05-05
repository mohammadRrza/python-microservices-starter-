# Python Microservices Architecture

A production-style microservices architecture built with FastAPI, PostgreSQL, Kafka, Docker, SQLAlchemy, Alembic, Pytest, and Domain-Driven Design (DDD).

This project demonstrates scalable backend architecture patterns including:

- Microservices architecture
- Event-driven communication
- Kafka messaging
- Outbox Pattern
- Dockerized infrastructure
- Database-per-service pattern
- Alembic migrations
- Integration & unit testing
- DDD structure
- CI/CD-ready setup

---

# Tech Stack

## Backend

- Python 3.11+
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pydantic

## Messaging

- Apache Kafka
- Zookeeper

## DevOps

- Docker
- Docker Compose
- Makefile
- Jenkinsfile

## Testing

- Pytest
- Unit Tests
- Integration Tests

---

# Architecture

## Services

| Service | Description |
|---|---|
| user-service | User management |
| product-service | Product catalog |
| order-service | Order management |
| payment-service | Payment processing |
| notification-service | Notification handling |
| gateway-service | API Gateway |

---

# Architectural Patterns

## Domain-Driven Design (DDD)

The project follows DDD principles, especially inside the `payment-service`.

Typical structure:

```text
app/
├── application/
├── domain/
├── infrastructure/
├── presentation/
└── tests/
```

### Layers

#### Domain Layer
Contains:

- Entities
- Value Objects
- Repository interfaces
- Domain logic

#### Application Layer
Contains:

- Use cases
- DTOs
- Business orchestration

#### Infrastructure Layer
Contains:

- SQLAlchemy repositories
- Kafka producer/consumer
- Database implementation
- External integrations

#### Presentation Layer
Contains:

- FastAPI routers
- API schemas
- Controllers

---

# Event-Driven Architecture

Services communicate asynchronously using Kafka.

Example flow:

```text
payment-service
    ↓
Kafka Event
    ↓
notification-service
```

Benefits:

- Loose coupling
- Scalability
- Async communication
- Reliability
- Better fault isolation

---

# Outbox Pattern

Implemented in:

- `payment-service`

Purpose:

To guarantee reliable event publishing without losing messages.

---

## Outbox Table

```sql
payment_outbox_events
```

Columns:

| Column | Description |
|---|---|
| id | Event ID |
| aggregate_type | Aggregate name |
| aggregate_id | Aggregate identifier |
| event_type | Domain event type |
| topic | Kafka topic |
| payload | Event payload |
| published | Publish status |
| created_at | Creation timestamp |

---

## Outbox Flow

### Inside Use Case

`AuthorizePaymentUseCase`

Steps:

1. Save payment
2. Save outbox event
3. Commit transaction

Example:

```python
payment_repository.save(payment)
outbox_repository.save(event)
db.commit()
```

---

## Outbox Publisher

Background worker:

```python
publish_outbox_events()
```

Responsibilities:

- Query unpublished events
- Publish events to Kafka
- Mark events as published
- Commit transaction

---

## Kafka Producer Startup

The Kafka producer must start before the outbox publisher worker.

Implemented in:

```python
main.py
```

Example:

```python
@app.on_event("startup")
async def startup_event():
    await start_producer()
    asyncio.create_task(publish_outbox_events())
```

Correct startup order:

```text
1. Start Kafka producer
2. Start outbox publisher worker
```

Otherwise:

```text
RuntimeError: Kafka producer is not started
```

---

# Database Architecture

Each service uses its own PostgreSQL database.

This follows the:

```text
Database per Service
```

pattern.

---

# Docker Infrastructure

The entire system is containerized.

Infrastructure includes:

- PostgreSQL
- Kafka
- Zookeeper
- Services
- API Gateway

---

# Docker Compose

Main compose file:

```text
infrastructure/docker-compose.yml
```

---

# Running the Project

## Clone Repository

```bash
git clone https://github.com/mohammadRrza/event-driven-backend-platform.git
cd python-microservices-project
```

---

## Start Infrastructure

```bash
make up
```

---

## Stop Infrastructure

```bash
make down
```

---

## Rebuild Containers

```bash
make build
```

---

# Database Migrations

Alembic is used for schema migrations.

Each service manages its own migrations.

---

## Run Migrations

Migrations are automatically executed using:

```text
entrypoint.sh
```

during container startup.

---

# Seed Data

Development seed data:

```text
infrastructure/seed_dev_data.sql
```

---

# Testing

The project contains both unit and integration tests.

## Test Structure

```text
tests/
├── unit/
└── integration/
```

---

## Unit Tests

Unit tests isolate business logic.

Example:

- Use cases
- Domain services
- Validation logic

---

## Integration Tests

Integration tests run against a real PostgreSQL database.

Used for:

- Repository testing
- API testing
- Database transaction testing
- End-to-end flows

---

## Run Tests

```bash
pytest
```

---

## Run Unit Tests

```bash
pytest tests/unit
```

---

## Run Integration Tests

```bash
pytest tests/integration
```

---

# Kafka Topics

Example topics:

```text
payment.authorized
payment.failed
order.created
notification.send
```

---

# API Documentation

FastAPI Swagger UI:

```text
http://localhost:<port>/docs
```

ReDoc:

```text
http://localhost:<port>/redoc
```

---

# CI/CD

A Jenkins pipeline is included.

File:

```text
Jenkinsfile
```

Potential stages:

- Build
- Test
- Docker build
- Deploy

---

# Reliability Features

Implemented:

- Outbox Pattern
- Transactional event publishing
- Async messaging
- Docker health management
- Automatic migrations

Planned improvements:

- Retry mechanism
- Dead Letter Queue (DLQ)
- Idempotent consumers
- Distributed tracing
- OpenTelemetry
- Centralized logging
- Metrics monitoring
- Circuit breakers

---

# Project Structure

```text
python-microservices-project/
├── infrastructure/
├── deploy/
├── services/
│   ├── user-service/
│   ├── product-service/
│   ├── order-service/
│   ├── payment-service/
│   ├── notification-service/
│   └── gateway-service/
├── Jenkinsfile
└── README.md
```

---

# Example Payment Flow

```text
Client
  ↓
payment-service
  ↓
Save Payment
  ↓
Save Outbox Event
  ↓
Commit Transaction
  ↓
Outbox Publisher
  ↓
Kafka
  ↓
notification-service
```

---

# Production Considerations

Recommended next steps:

- Kubernetes deployment
- Redis caching
- API rate limiting
- Saga pattern
- Centralized authentication
- Observability stack
- Distributed tracing
- Horizontal scaling
- Service mesh

---

# Author

Built for learning and demonstrating modern Python microservices architecture patterns using FastAPI and Kafka.

---

# License

MIT License
