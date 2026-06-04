# Source Data Inventory

This document records the real files provided for the Purplle Tech Challenge and the implementation implications discovered from inspection.

## Local Raw Files

The provided files were copied into:

```text
purplle-tech-challenge-2026/data/raw/
```

Normalized local names:

```text
pos_transactions.csv
sample_events.jsonl
store_1.zip
store_2.zip
```

The video archives are intentionally ignored by git because they are large local challenge assets.

## POS File

Source file:

```text
POS - sample transactionsb1e826f.csv
```

Observed row count:

```text
100 data rows + 1 header row
```

Observed columns:

```text
order_id
order_date
order_time
store_id
product_id
brand_name
total_amount
```

Observed store:

```text
ST1008
```

Important implication:

The real POS schema differs from the original prompt schema.

The prompt expected:

```text
store_id
transaction_id
timestamp
basket_value_inr
```

Implementation should normalize the real POS data into the internal transaction contract:

```text
transaction_id = order_id
timestamp = parsed order_date + order_time
store_id = store_id
basket_value_inr = sum(total_amount) grouped by order_id
```

Why grouping matters:

The provided POS file appears to contain product-level order rows. Conversion attribution should happen at the order level, not the product-line level, otherwise a multi-product basket could be counted as multiple purchases.

## Sample Events File

Source file:

```text
sample_eventsbe42122.jsonl
```

Observed row count:

```text
13 JSONL events
```

Observed fields include:

```text
event_type
id_token
store_code
camera_id
event_timestamp
is_staff
gender_pred
age_pred
age_bucket
is_face_hidden
group_id
group_size
zone_id
dwell_time_sec
queue_id
queue_duration_sec
```

Observed event types:

```text
entry
exit
zone_entered
zone_exited
queue_completed
queue_abandoned
```

Important implication:

The sample event schema differs from the canonical schema in the prompt. Implementation should support a source-event adapter that maps provided sample event names and fields to the internal canonical event schema.

Suggested mappings:

| Source event type | Internal event type |
|---|---|
| `entry` | `ENTRY` |
| `exit` | `EXIT` |
| `zone_entered` | `ZONE_ENTER` |
| `zone_exited` | `ZONE_EXIT` |
| `queue_completed` | `BILLING_QUEUE_JOIN` plus purchase-attribution signal |
| `queue_abandoned` | `BILLING_QUEUE_ABANDON` |

Suggested field mappings:

| Source field | Internal field |
|---|---|
| `id_token` | `visitor_id` |
| `store_code` | `store_id` |
| `event_timestamp` | `timestamp` |
| `dwell_time_sec` | `dwell_ms` |
| `queue_duration_sec` | `dwell_ms` for queue events |
| demographic fields | `metadata` |

## Store 1 Video Archive

Source file:

```text
Store 1-20260602T101818Z-3-001ec38db8.zip
```

Normalized local file:

```text
data/raw/store_1.zip
```

Archive contents:

```text
Store 1/Store 1 - layout.png
Store 1/CAM 5 - billing.mp4
Store 1/CAM 3 - entry.mp4
Store 1/CAM 2 - zone.mp4
Store 1/CAM 1 - zone.mp4
```

Important implication:

Store 1 has one billing camera, one entry camera, and two zone cameras. The layout is an image, not a JSON file.

## Store 2 Video Archive

Source file:

```text
Store 2-20260602T101819Z-3-001099f208.zip
```

Normalized local file:

```text
data/raw/store_2.zip
```

Archive contents:

```text
Store 2/store 2 - layout.png
Store 2/entry 2.mp4
Store 2/entry 1.mp4
Store 2/billing_area.mp4
Store 2/zone.mp4
```

Important implication:

Store 2 has two entry cameras, one billing camera, and one zone camera. The layout is an image, not a JSON file.

## Store Layout Implication

The original prompt mentioned `store_layout.json`, but the real source data currently contains layout PNGs inside the store archives.

Recommended implementation decision:

1. Extract layout images locally.
2. Create a manual calibration file per store:

```text
configs/store_layouts/store_1.layout.json
configs/store_layouts/store_2.layout.json
```

3. Store polygon zones in JSON after visually calibrating against the layout image and camera views.

Why:

- This preserves the expected zone-based architecture.
- It is explainable and practical for a challenge dataset.
- It avoids pretending the source provided polygons when it did not.

## Revised Implementation Priority

Because real layouts are images, the next build step should be:

1. Implement POS normalization.
2. Implement source sample-event adapter.
3. Extract layout PNGs.
4. Create calibrated store layout JSON files.
5. Validate canonical events against the challenge schema.
6. Then proceed to CV detection and tracking.

