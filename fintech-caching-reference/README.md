# FinTech Caching Reference

**Reference patterns for high-performance caching and reconfigurable rule evaluation in regulated environments.**

This repository demonstrates patterns used in mission-critical financial systems: **sub-millisecond cached access** to reference and profile data, and a **reconfigurable rule engine** for commission/eligibility-style logic — inspired by compensation engines that support hundreds of rules with in-house updates. Aligns with VMware GemFire–style caching and configurable business rules in FinTech.

## Features

- **Multi-tier caching** — In-memory (Caffeine) + optional Redis for distributed cache
- **Cache-aside pattern** — With TTL, refresh, and metrics
- **Reconfigurable rule engine** — JSON-driven rules (conditions + actions); add/update without code deploy
- **REST API** — Profile lookup (cached), rule evaluation, and admin endpoints to reload rules
- **Observability** — Micrometer metrics for cache hits/misses and rule evaluations

## Tech Stack

- **Java 17**, **Spring Boot 3.x**
- **Caffeine** (in-memory cache)
- **Spring Data Redis** (optional second tier)
- **JSON rule definitions** — No code change for new rules

## Quick Start

```bash
./mvnw spring-boot:run
# Or run the Application main class from your IDE.
```

- `GET /api/profiles/{id}` — Get profile (cached)
- `POST /api/rules/evaluate` — Evaluate a payload against loaded rules
- `POST /api/admin/rules/reload` — Reload rules from classpath JSON

## Project Structure

```
fintech-caching-reference/
├── src/main/java/.../cache/     # Cache config and profile service
├── src/main/java/.../rules/     # Rule engine and loader
├── src/main/resources/rules/    # JSON rule definitions
└── README.md
```

## License

MIT

## Author

Sumit Bhatnagar — [LinkedIn](https://linkedin.com/in/sumitbhatnagar1411) 
