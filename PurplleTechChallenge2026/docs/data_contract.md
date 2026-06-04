# Data Contract

## Event Schema

Every generated event must conform to this schema:

```json
{
  "event_id": "evt_001",
  "store_id": "store_001",
  "camera_id": "entry_cam_001",
  "visitor_id": "visitor_001",
  "event_type": "ENTRY",
  "timestamp": "2026-01-01T10:00:00Z",
  "zone_id": "entry_zone",
  "dwell_ms": null,
  "is_staff": false,
  "confidence": 0.92,
  "metadata": {}
}
```

## Event Types

```text
ENTRY
EXIT
ZONE_ENTER
ZONE_EXIT
ZONE_DWELL
BILLING_QUEUE_JOIN
BILLING_QUEUE_ABANDON
REENTRY
```

## Store Layout

`store_layout.json` defines:

- `store_id`
- open hours
- camera coverage
- zone polygons
- zone types

Zone membership should use the bottom-center point of the detected person bounding box.

## POS Transactions

Canonical internal columns:

```text
store_id
transaction_id
timestamp
basket_value_inr
```

The provided POS source file uses product-line order rows:

```text
order_id
order_date
order_time
store_id
product_id
brand_name
total_amount
```

The importer should normalize source rows into canonical transactions by grouping on `order_id` and summing `total_amount`.

## Conversion Rule

A transaction is attributed to a visitor if:

- same `store_id`
- visitor is not staff
- visitor was in billing zone
- visitor was observed within five minutes before transaction timestamp

When multiple candidates exist, choose the highest scoring candidate and store attribution confidence.

## Database Schema

```mermaid
erDiagram
    stores ||--o{ cameras : has
    stores ||--o{ zones : has
    stores ||--o{ visitors : has
    stores ||--o{ events : has
    stores ||--o{ transactions : has
    visitors ||--o{ tracks : has
    visitors ||--o{ events : produces
    cameras ||--o{ tracks : observes
    zones ||--o{ events : relates_to
    transactions ||--o| conversion_attributions : attributed_by
    visitors ||--o{ conversion_attributions : matched_to

    stores {
        string store_id PK
        string name
        time open_time
        time close_time
        json metadata
    }

    cameras {
        string camera_id PK
        string store_id FK
        string camera_type
        json coverage
        json metadata
    }

    zones {
        string zone_id PK
        string store_id FK
        string zone_type
        json polygon
        json metadata
    }

    visitors {
        string visitor_id PK
        string store_id FK
        timestamp first_seen_at
        timestamp last_seen_at
        boolean is_staff
        float confidence
        json metadata
    }

    tracks {
        string track_id PK
        string visitor_id FK
        string camera_id FK
        timestamp start_time
        timestamp end_time
        float avg_confidence
        json metadata
    }

    events {
        string event_id PK
        string store_id FK
        string camera_id FK
        string visitor_id FK
        string event_type
        timestamp timestamp
        string zone_id FK
        integer dwell_ms
        boolean is_staff
        float confidence
        json metadata
    }

    transactions {
        string transaction_id PK
        string store_id FK
        timestamp timestamp
        float basket_value_inr
    }

    conversion_attributions {
        string attribution_id PK
        string transaction_id FK
        string visitor_id FK
        timestamp attributed_at
        float confidence
        string attribution_method
        json metadata
    }
```
