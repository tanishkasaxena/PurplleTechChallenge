# Submission Summary

## Problem

Specialty retail stores have CCTV footage and POS transactions but no reliable customer analytics. The system must convert physical-store behavior into structured events and calculate offline conversion rate.

## North Star Metric

```text
Offline Store Conversion Rate =
Visitors who completed a purchase / Total unique visitors
```

The system infers a completed purchase by matching a non-staff visitor in the billing zone within five minutes before a POS transaction.

## Proposed Solution

Build a modular offline analytics platform:

1. Detect people with YOLOv8.
2. Track individuals per camera with ByteTrack.
3. Associate camera-local tracks into global store-level visitors.
4. Map visitor positions into store zones using `store_layout.json`.
5. Emit validated behavioral events.
6. Attribute POS transactions to likely visitors.
7. Serve metrics through FastAPI.
8. Visualize insights in Streamlit.

## Why This Can Score Highly

- It optimizes for conversion accuracy, not just person counting.
- It handles real CCTV edge cases explicitly.
- It is explainable: every metric traces back to events.
- It is production-minded: typed APIs, database schema, tests, config, Docker plan, and structured logs.
- It is interviewable: each design choice has a clear reason and tradeoff.

## Key Differentiators

- Global `visitor_id` separated from camera-local `track_id`.
- Confidence scores on events and POS attribution.
- Staff exclusion strategy.
- Re-entry handling.
- Queue join and abandonment events.
- Camera overlap suppression.
- Empty-store and occlusion-safe behavior.

## Current Package Status

This package contains the approved design scaffold and implementation plan. Code should be generated incrementally after design approval, beginning with schemas, validation, database models, and tests.

