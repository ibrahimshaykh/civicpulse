# CivicPulse

Municipal complaint triage platform.

![CI](https://github.com/ibrahimshaykh/civicpulse/actions/workflows/ci.yml/badge.svg)
![CD](https://github.com/ibrahimshaykh/civicpulse/actions/workflows/cd.yml/badge.svg)

## Quickstart
```bash
make up
```
Open `http://localhost:8080`.

## API
| Method | Path | Behaviour |
|---|---|---|
| POST | /api/complaints | Create complaint |
| GET | /api/complaints | List complaints |
| PATCH | /api/complaints/{id}/status | Update status |
| GET | /api/stats | View stats |
| GET | /api/meta/providers | Providers info |
| GET | /health | Liveness |
| GET | /ready | Readiness |
| GET | /metrics | Prometheus |

## Architecture
```mermaid
flowchart TB
    user([Citizen / Operator])
    fe[frontend]
    be[backend]
    db[(postgres)]
    cache[(redis)]
    user --> fe
    fe --> be
    be --> db
    be --> cache
```
