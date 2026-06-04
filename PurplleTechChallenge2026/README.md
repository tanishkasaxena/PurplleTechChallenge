```markdown
# Purplle Tech Challenge 2026 - Offline Store Analytics

Submission package for transforming in-store CCTV and POS data into structured customer behavior events, analytics APIs, and dashboard insights.

## North Star Metric

Offline Store Conversion Rate:

```text
converted_unique_visitors / total_unique_visitors
```

A converted visitor is inferred when a non-staff visitor is observed in the billing zone within five minutes before a POS transaction.

## Demo

Deployed demo:

```text
https://purplle-tech-challenge-mu.vercel.app
```

Local dashboard:

```text
demo/dashboard.html
```

## Mandatory Deliverables

This submission includes:

```text
README.md
DESIGN.md
CHOICES.md
submission/event_log.jsonl
```

The event log follows the schema style demonstrated in the provided `sample_events.jsonl`.

## Tech Stack

| Layer | Choice |
|---|---|
| API | FastAPI |
| Database | SQLite for local demo, PostgreSQL for production |
| Detection | YOLOv8 |
| Tracking | ByteTrack |
| Re-ID | OSNet / lightweight appearance embeddings |
| Video Processing | OpenCV |
| Dashboard | Streamlit concept + static Vercel demo |
| Validation | Python JSONL validator |
| Testing | unittest / Pytest-compatible structure |
| Packaging | Docker Compose plan |
| Deployment | Vercel static demo |
| Logging | Structured JSON logs design |

## Project Structure

```text
PurplleTechChallenge2026/
  README.md
  DESIGN.md
  CHOICES.md
  SUBMISSION.md
  pyproject.toml
  package.json
  vercel.json
  docker-compose.yml
  .env.example

  submission/
    event_log.jsonl
    Purplle_Offline_Store_Analytics_Deck.pptx

  demo/
    dashboard.html

  scripts/
    validate_event_log.py
    build_demo_dashboard.py

  docs/
    architecture.md
    api_contract.md
    data_contract.md
    event_lifecycle.md
    roadmap.md
    risks_and_scoring.md
    source_data_inventory.md

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

  tests/
    unit/
      test_demo_dashboard.py
    README.md

  docker/
    README.md

  app/
    README.md
```

## How To Run Locally

1. Open the project folder:

```bash
cd PurplleTechChallenge2026
```

2. Validate the mandatory event log:

```bash
python3 scripts/validate_event_log.py submission/event_log.jsonl
```

Expected output:

```text
OK: submission/event_log.jsonl is valid JSONL for the provided sample schema
```

3. Run tests:

```bash
python3 -m unittest discover -s tests/unit
```

Expected output:

```text
Ran 2 tests
OK
```

4. Generate the offline dashboard:

```bash
python3 scripts/build_demo_dashboard.py
```

5. Open the dashboard:

```text
demo/dashboard.html
```

## What The System Does

The proposed system converts CCTV footage into structured retail behavior events:

- customer entry and exit
- zone entry and exit
- zone dwell
- billing queue completion
- billing queue abandonment
- staff exclusion
- re-entry handling
- conversion attribution using POS transactions

The analytics layer computes:

- offline conversion rate
- unique visitors
- queue completion and abandonment
- dwell behavior
- event quality
- POS order and revenue summaries

## Architecture Summary

The system is designed around validated behavioral events as the source of truth.

```text
CCTV footage
  -> YOLOv8 person detection
  -> ByteTrack tracking
  -> visitor association / Re-ID
  -> zone mapping
  -> event generation
  -> JSONL event log
  -> POS attribution
  -> APIs and dashboard
```

This design makes every business metric traceable back to a specific event.

## Key Design Choices

### YOLOv8 for detection

Chosen because it is accurate, practical, widely supported, and easy to explain.

### ByteTrack for tracking

Chosen because it handles temporary occlusion and low-confidence detections better than simple centroid tracking.

### OSNet / appearance embeddings for Re-ID

Chosen because faces are blurred, so cross-camera matching must rely on body and clothing appearance.

### Event-first architecture

Chosen because raw detections are noisy, while validated events are easier to test, audit, and serve through APIs.

### POS normalization

The provided POS file contains product-line rows. The system normalizes these into order-level transactions before conversion attribution.

## Edge Cases Covered

- Multiple people entering together
- Staff movement
- Re-entry
- Partial occlusion
- Billing queues
- Queue abandonment
- Empty store periods
- Camera overlap
- POS attribution ambiguity

## Production Readiness

The submission includes:

- JSONL schema validation
- unit tests
- configuration file
- Docker Compose plan
- structured logging design
- API contract
- database schema
- Vercel demo deployment setup
- documentation for architecture and engineering decisions

## Deployment

The static demo is deployed on Vercel:

```text
https://purplle-tech-challenge-mu.vercel.app
```

For Vercel deployment from source:

```text
Framework Preset: Other
Root Directory: PurplleTechChallenge2026
Build Command: npm run build
Output Directory: public
Install Command: leave empty
```

## Submission Notes

The current submission focuses on correctness of architecture, event schema, validation, analytics design, and demo readiness. The event log is validated against the provided sample schema, and the dashboard demonstrates how the event stream becomes business intelligence.

```
