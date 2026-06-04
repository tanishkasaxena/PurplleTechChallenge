# Test Plan

Planned test groups:

```text
tests/
  unit/
    test_event_schema.py
    test_zone_mapper.py
    test_conversion_attribution.py
    test_queue_events.py
    test_reentry.py
  integration/
    test_api_metrics.py
    test_pipeline_sample_video.py
  fixtures/
    store_layout.json
    pos_transactions.csv
    sample_events.jsonl
```

Testing priorities:

- Event schema validation
- Zone boundary behavior
- Dwell threshold behavior
- Queue join and abandon behavior
- Re-entry detection
- Staff exclusion
- POS attribution ambiguity
- Empty input handling

