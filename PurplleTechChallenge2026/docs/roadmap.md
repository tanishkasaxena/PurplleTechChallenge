# Development Roadmap

## Phase 1: Contracts and Validation

Deliver:

- Event schema
- Store layout schema
- POS transaction schema
- Sample event validation
- Unit tests

Why:

- Prevents inconsistent downstream analytics.

## Phase 2: Database Layer

Deliver:

- SQLAlchemy models
- SQLite local database
- PostgreSQL-compatible configuration
- Repository tests

Why:

- Makes API and analytics deterministic.

## Phase 3: Layout and Zone Logic

Deliver:

- Polygon zone loader
- Point-in-zone mapper
- Track-to-zone transitions
- Boundary tests

Why:

- Zone correctness drives dwell, heatmap, and billing attribution.

## Phase 4: Event Generator

Deliver:

- ENTRY and EXIT events
- ZONE_ENTER and ZONE_EXIT events
- ZONE_DWELL events
- BILLING_QUEUE_JOIN and BILLING_QUEUE_ABANDON events
- REENTRY events

Why:

- Required event generation is the backbone of the challenge.

## Phase 5: Conversion Attribution

Deliver:

- POS importer
- Candidate visitor selection
- Attribution ranking
- Confidence scoring
- Attribution tests

Why:

- Directly supports the North Star metric.

## Phase 6: API

Deliver:

- FastAPI app
- Health endpoint
- Event, visitor, transaction, and metrics endpoints
- OpenAPI documentation
- API tests

Why:

- Converts event data into usable intelligence.

## Phase 7: Dashboard

Deliver:

- Streamlit overview
- Store and date filters
- Conversion card
- Dwell charts
- Heatmap
- Queue chart
- Event explorer

Why:

- Demonstrates business actionability.

## Phase 8: CV Pipeline

Deliver:

- Video reader
- Frame sampler
- YOLOv8 detector adapter
- ByteTrack tracker adapter
- Track persistence
- Empty-frame handling

Why:

- Connects raw CCTV to the event layer.

## Phase 9: Identity and Edge Cases

Deliver:

- Global visitor association
- Re-entry detection
- Staff exclusion
- Camera overlap suppression
- Occlusion confidence degradation

Why:

- Reduces double counting and improves conversion accuracy.

## Phase 10: Production Readiness

Deliver:

- Docker Compose
- Structured JSON logs
- Configurable thresholds
- README
- Testing guide
- Known limitations

Why:

- Makes the submission easy to run, evaluate, and defend.

