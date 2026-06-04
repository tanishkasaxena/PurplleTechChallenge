# CHOICES.md

## Model Selection Decisions

### Person Detection: YOLOv8

Why chosen:

- Reliable person-detection baseline.
- Mature ecosystem and straightforward inference.
- Practical for 1080p CCTV footage.

Alternatives considered:

- YOLOv5
- Detectron2 Faster R-CNN
- RT-DETR

Tradeoffs:

- YOLOv8 is fast and simple, but crowded queues can still create missed detections.

Scoring impact:

- Strong detection quality without over-engineering.

### Tracking: ByteTrack

Why chosen:

- Handles low-confidence detections better than SORT.
- Works well for pedestrian tracking.
- Good fit for billing queues and temporary occlusion.

Alternatives considered:

- SORT
- DeepSORT
- FairMOT

Tradeoffs:

- Track switches can still occur under long occlusion.

Scoring impact:

- Improves event stability and group-entry handling.

### Re-Identification: OSNet or Lightweight Appearance Embeddings

Why chosen:

- Face data is blurred, so body/clothing appearance is the best available identity signal.
- Useful for re-entry and cross-camera association.

Alternatives considered:

- Face recognition
- No cross-camera re-ID
- Manual identity labels

Tradeoffs:

- Appearance embeddings can fail when clothing is similar or lighting changes.

Scoring impact:

- Helps reduce double counting and improves conversion accuracy.

## Schema Design Decisions

### Internal Canonical Schema

The internal system uses a normalized schema:

```text
event_id
store_id
camera_id
visitor_id
event_type
timestamp
zone_id
dwell_ms
is_staff
confidence
metadata
```

Why chosen:

- Consistent across event types.
- Easier for APIs, databases, and analytics.

Alternative:

- Use the sample JSONL schema internally.

Tradeoff:

- Requires adapter logic for submission output.

Scoring impact:

- Improves analytics correctness and production readiness.

### Submission Event Schema

The final event log follows the provided `sample_events.jsonl` style.

Why chosen:

- HackerEarth explicitly calls this a critical deliverable.

Alternative:

- Submit only canonical events.

Tradeoff:

- More fields vary by event type.

Scoring impact:

- Reduces mandatory-deliverable risk.

### POS Schema Normalization

The provided POS file is grouped by product line. The system normalizes it into order-level transactions.

Mapping:

```text
transaction_id = order_id
timestamp = order_date + order_time
store_id = store_id
basket_value_inr = sum(total_amount)
```

Why chosen:

- Conversion is customer/order-level, not product-line-level.

Alternative:

- Treat each row as one transaction.

Tradeoff:

- Requires grouped aggregation.

Scoring impact:

- Prevents inflated conversion attribution.

## API Architecture Decisions

### FastAPI

Why chosen:

- Typed request and response models.
- Built-in OpenAPI docs.
- Easy testing with pytest.

Alternatives considered:

- Flask
- Django REST Framework

Tradeoffs:

- FastAPI requires explicit schema discipline, which is useful here.

Scoring impact:

- Strong API correctness and documentation.

### Repository and Service Layers

Why chosen:

- Separates database access from business analytics logic.
- Makes conversion attribution testable.

Alternatives considered:

- Put all queries directly in route handlers.

Tradeoffs:

- More files, but clearer ownership.

Scoring impact:

- Improves production readiness.

### SQLite First, PostgreSQL Compatible

Why chosen:

- SQLite makes local evaluation simple.
- SQLAlchemy keeps PostgreSQL migration practical.

Alternatives considered:

- PostgreSQL only
- DuckDB

Tradeoffs:

- SQLite is not ideal for high-concurrency production workloads.

Scoring impact:

- Balances demo simplicity and production credibility.

### Streamlit Dashboard

Why chosen:

- Fast to build useful business dashboards.
- Good for conversion cards, dwell charts, heatmaps, and event tables.

Alternatives considered:

- React dashboard
- Dash

Tradeoffs:

- Less customizable than a full frontend.

Scoring impact:

- Maximizes dashboard value within challenge time.

