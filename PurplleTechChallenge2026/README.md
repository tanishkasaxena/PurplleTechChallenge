# Purplle Tech Challenge 2026 - Offline Store Analytics

Submission package for transforming in-store CCTV and POS data into structured customer behavior events, APIs, and dashboards.

## North Star Metric

Offline Store Conversion Rate:

```text
converted_unique_visitors / total_unique_visitors
```

Where a converted visitor is a non-staff visitor observed in the billing zone within five minutes before a POS transaction.

## What This Submission Contains

- A concise submission summary
- Mandatory HackerEarth deliverables:
  - `submission/event_log.jsonl`
  - `README.md`
  - `DESIGN.md`
  - `CHOICES.md`
- End-to-end architecture and system design
- Detection, tracking, re-identification, and event lifecycle design
- Database schema for events, tracks, visitors, zones, transactions, and attribution
- API contract for intelligence endpoints
- Dashboard design for business users
- Production readiness plan with testing, logging, Docker, and MLOps considerations
- Incremental implementation roadmap

## Current Stage

This is the design-approved submission scaffold. It is intentionally documentation-first because implementation should begin only after architecture, data contracts, event semantics, and scoring strategy are approved.

## Proposed Stack

| Layer | Choice |
|---|---|
| API | FastAPI |
| Database | SQLite for local demo, PostgreSQL for production |
| Detection | YOLOv8 person detector |
| Tracking | ByteTrack |
| Re-ID | OSNet or lightweight appearance embeddings |
| Dashboard | Streamlit |
| Testing | Pytest |
| Packaging | Docker Compose |
| Logging | Structured JSON logs |

## Directory Guide

```text
purplle-tech-challenge-2026/
  README.md
  DESIGN.md
  CHOICES.md
  SUBMISSION.md
  pyproject.toml
  docker-compose.yml
  .env.example
  submission/
    event_log.jsonl
  scripts/
    validate_event_log.py
  docs/
    architecture.md
    api_contract.md
    data_contract.md
    event_lifecycle.md
    roadmap.md
    risks_and_scoring.md
    source_data_inventory.md
  docker/
    README.md
  configs/
    default.yaml
  data/
    examples/
      store_layout.example.json
      pos_transactions.example.csv
      sample_events.example.jsonl
    raw/
      pos_transactions.csv
      sample_events.jsonl
      store_1.zip
      store_2.zip
  app/
    README.md
  tests/
    README.md
```

## Recommended Build Order

1. Source data adapters for the provided POS and sample event files
2. Event schemas and validation
3. Database models and repositories
4. Layout calibration from provided layout PNGs
5. Layout and zone mapper
6. Track-based event generator
7. POS conversion attribution
8. FastAPI intelligence endpoints
9. Streamlit dashboard
10. YOLOv8 and ByteTrack video pipeline
11. Re-ID, staff exclusion, overlap suppression
12. Docker, tests, logging, and final documentation

## Submission Narrative

The system treats validated behavioral events as the source of truth. This makes conversion measurement explainable, testable, and resilient to CCTV edge cases such as group entry, staff movement, re-entry, camera overlap, billing queues, occlusion, and empty periods.

## Validate Mandatory Event Log

Run:

```text
python3 scripts/validate_event_log.py submission/event_log.jsonl
```

Expected result:

```text
OK: submission/event_log.jsonl is valid JSONL for the provided sample schema
```

## Create Snapshot and Video Demo

Build the offline dashboard:

```text
python3 scripts/build_demo_dashboard.py
```

Open the generated file in a browser:

```text
demo/dashboard.html
```

Use that page for screenshots or screen recording.

Run local tests:

```text
python3 -m unittest discover -s tests/unit
```
