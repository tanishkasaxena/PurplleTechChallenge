# API Contract

The intelligence API uses FastAPI and returns typed JSON responses.

## Health

```http
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

## Stores

```http
GET /stores
GET /stores/{store_id}
```

## Events

```http
GET /stores/{store_id}/events
```

Query parameters:

- `start_time`
- `end_time`
- `event_type`
- `visitor_id`
- `zone_id`
- `include_staff`

## Visitors

```http
GET /stores/{store_id}/visitors
```

Query parameters:

- `start_time`
- `end_time`
- `include_staff`

## Transactions

```http
GET /stores/{store_id}/transactions
```

## Conversion Metric

```http
GET /stores/{store_id}/metrics/conversion
```

Response:

```json
{
  "store_id": "store_001",
  "start_time": "2026-01-01T10:00:00Z",
  "end_time": "2026-01-01T22:00:00Z",
  "unique_visitors": 120,
  "converted_visitors": 36,
  "conversion_rate": 0.3,
  "attributed_transactions": 36,
  "unattributed_transactions": 4,
  "confidence": 0.84
}
```

## Dwell Metrics

```http
GET /stores/{store_id}/metrics/dwell
```

Returns average and percentile dwell time by zone.

## Heatmap Metrics

```http
GET /stores/{store_id}/metrics/heatmap
```

Returns zone-level density and dwell aggregates for dashboard heatmaps.

## Queue Metrics

```http
GET /stores/{store_id}/metrics/queue
```

Returns:

- queue joins
- queue abandons
- average queue depth
- peak queue depth
- estimated wait time

## Summary Metrics

```http
GET /stores/{store_id}/metrics/summary
```

Returns top-level KPIs for dashboard cards.

