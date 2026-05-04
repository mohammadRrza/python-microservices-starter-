# Python Microservices Starter

A clean microservices starter project built with FastAPI, Docker, and Docker Compose.

## Services
- gateway-service
- user-service
- product-service
- order-service
- postgres

## Tech Stack
- Python
- FastAPI
- Docker
- Docker Compose
- PostgreSQL

## 🧱 Architecture

This project consists of the following services:

- **gateway-service** → API Gateway (routes requests)
- **user-service** → Manages users (connected to PostgreSQL)
- **product-service** → Manages products
- **order-service** → Manages orders
- **payment-service** → Manages payments
- **postgres** → Database

---

## Notes

- Each service runs independently
- Gateway acts as a single entry point
- Services communicate over Docker network
- Payment Service is implemented using tactical DDD patterns to model payment lifecycle, business invariants, and domain events.
---

## Run the project

```bash
cd infrastructure
docker compose up --build