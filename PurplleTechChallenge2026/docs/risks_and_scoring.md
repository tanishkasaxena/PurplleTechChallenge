# Risks and Scoring Strategy

## Highest-Risk Areas

### Cross-Camera Identity

Risk:

- Same visitor may appear in multiple cameras and be double counted.

Mitigation:

- Use entry camera as primary visitor source.
- Associate global visitor IDs across cameras using time, zone transitions, and appearance embeddings.
- Store confidence for every association.

Scoring impact:

- Very high. Conversion accuracy depends on deduplicated visitors.

### Staff Exclusion

Risk:

- Staff movement inflates visitor counts and distorts dwell metrics.

Mitigation:

- Rule-based staff classifier using repeated appearances, long duration, staff-only zones, and behind-counter movement.
- Optional configured staff track labels for demos.

Scoring impact:

- Very high.

### POS Attribution Ambiguity

Risk:

- Multiple people may be in the billing area within five minutes of a transaction.

Mitigation:

- Rank candidates by time proximity, queue position, billing-zone presence, and track continuity.
- Store attribution confidence and metadata.

Scoring impact:

- Highest direct impact on the North Star metric.

### Group Entry

Risk:

- Multiple visitors entering together may merge into one count.

Mitigation:

- Person-level detection with YOLOv8.
- ByteTrack track continuity.
- ENTRY generated per individual track crossing.

Scoring impact:

- High.

### Occlusion

Risk:

- Track loss or ID switches in crowded areas.

Mitigation:

- ByteTrack low-confidence association.
- Short disappearance tolerance.
- Confidence degradation rather than silent failure.

Scoring impact:

- High.

### Empty Stores

Risk:

- No detections may crash naive pipelines.

Mitigation:

- Explicit empty-frame path.
- Emit no events and log empty intervals.

Scoring impact:

- Medium, but important for robustness.

## Scoring Strategy

| Area | Strategy | Impact |
|---|---|---|
| Conversion accuracy | Deduplicated visitors, staff exclusion, POS attribution confidence | Highest |
| Event correctness | Strict schema and deterministic lifecycle | Very high |
| Explainability | Trace every KPI back to events and metadata | Very high |
| Robustness | Handle occlusion, queues, overlap, empty stores | High |
| API quality | Typed FastAPI endpoints and OpenAPI docs | High |
| Dashboard | Business KPIs and operational insights | Medium-high |
| Production readiness | Docker, tests, config, structured logs | High |

## Winning Narrative

This system does not just count detections. It creates a validated event stream from CCTV, links it to POS activity with confidence, and exposes explainable store intelligence for conversion, dwell, queues, and heatmaps.

