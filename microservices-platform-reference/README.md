# Microservices Platform Reference

**Reference architecture for enterprise microservices: API gateway, event-driven messaging, Kubernetes deployment, and observability.**

This repository demonstrates patterns used in large-scale, regulated environments: Spring Boot microservices, Spring Cloud Gateway, Apache Kafka for events, Kubernetes manifests, and an observability stack (Prometheus + Grafana).

## Features

- **Spring Boot microservices** — Two domain services (orders, users) with REST APIs
- **API Gateway** — Spring Cloud Gateway with routing and simple auth
- **Kafka messaging** — Event publishing and consumption between services
- **Kubernetes deployment** — Manifests for all components
- **Observability** — Prometheus metrics, Grafana dashboard placeholders

## Tech Stack

- Java 17, Spring Boot 3.x
- Spring Cloud Gateway
- Apache Kafka
- Docker & Kubernetes
- Prometheus, Grafana

## Quick Start

### With Docker Compose (local)

```bash
# Start Kafka and supporting services
docker-compose up -d

# Build and run (from repo root)
./mvnw -pl gateway,order-service,user-service spring-boot:run
# Or run each service in a separate terminal with the appropriate profile.
```

### With Kubernetes (minikube / kind)

```bash
kubectl apply -f k8s/
# Then access gateway (NodePort or port-forward).
```

## Project Structure

```
microservices-platform-reference/
├── gateway/              # Spring Cloud Gateway
├── order-service/        # Order domain microservice
├── user-service/         # User domain microservice
├── k8s/                  # Kubernetes manifests
├── docker-compose.yml
└── README.md
```

## License

MIT

## Author

Sumit Bhatnagar — [LinkedIn](https://linkedin.com/in/sumitbhatnagar1411) 