# Purplle Tech Challenge 2026

## Offline Store Analytics using CCTV + POS Data

Transforming in-store CCTV footage and POS transactions into structured customer behavior events, actionable retail analytics, and business intelligence dashboards.

---

# Problem Statement

Physical retail stores generate large amounts of customer activity data through CCTV systems and Point-of-Sale (POS) transactions. However, this information is often disconnected, making it difficult to understand customer journeys, store performance, conversion rates, and operational bottlenecks.

This project proposes an event-driven analytics platform that converts raw CCTV footage and POS data into a unified stream of customer behavior events that can be queried, analyzed, and visualized.

The solution enables Purplle to measure customer engagement, conversion, queue behavior, and zone performance while maintaining privacy by avoiding facial recognition.

---

# North Star Metric

## Offline Store Conversion Rate

```text
Offline Conversion Rate =
Converted Unique Visitors / Total Unique Visitors
```

A visitor is considered converted when:

```text
A non-staff visitor is observed inside the billing zone
within five minutes prior to a POS transaction.
```

---

# Demo

### Live Demo

```text
https://purplle-tech-challenge-mu.vercel.app
```

### Local Dashboard

```text
demo/dashboard.html
```

---

# Features

### Customer Analytics

* Unique visitor tracking
* Entry and exit detection
* Zone-wise customer movement
* Dwell time analysis
* Re-entry handling
* Queue participation tracking
* Billing completion tracking
* Queue abandonment detection

### Store Analytics

* Offline conversion rate
* Zone engagement metrics
* Customer flow analysis
* Visitor heatmap generation
* Peak-hour identification
* Queue efficiency measurement

### Business Intelligence

* POS attribution
* Revenue summaries
* Order analytics
* Customer-to-purchase conversion
* Event quality monitoring

### Engineering Features

* Event-first architecture
* JSONL event logging
* Schema validation
* Unit testing
* Configurable pipeline
* Docker-ready deployment
* Structured logging

---

# Architecture Overview

```text
CCTV Footage
      │
      ▼
YOLOv8 Person Detection
      │
      ▼
ByteTrack Multi-Object Tracking
      │
      ▼
Visitor Association & Re-ID
      │
      ▼
Zone Mapping
      │
      ▼
Behavior Event Generation
      │
      ▼
JSONL Event Log
      │
      ▼
POS Attribution Engine
      │
      ▼
Analytics APIs & Dashboard
```

The platform treats validated behavioral events as the single source of truth for all downstream analytics.

---

# Technology Stack

| Layer                 | Technology                             |
| --------------------- | -------------------------------------- |
| Backend API           | FastAPI                                |
| Database              | SQLite (Demo), PostgreSQL (Production) |
| Object Detection      | YOLOv8                                 |
| Multi-Object Tracking | ByteTrack                              |
| Re-Identification     | OSNet Appearance Embeddings            |
| Video Processing      | OpenCV                                 |
| Dashboard             | Streamlit Concept + Static HTML        |
| Validation            | Python JSONL Validator                 |
| Testing               | unittest / Pytest                      |
| Deployment            | Vercel                                 |
| Containerization      | Docker Compose                         |
| Logging               | Structured JSON Logs                   |

---

# Why These Choices?

## YOLOv8

Chosen for:

* High detection accuracy
* Fast inference
* Industry adoption
* Easy deployment

---

## ByteTrack

Chosen because it:

* Handles temporary occlusions
* Maintains stable identities
* Works well with crowded retail environments
* Outperforms simple centroid tracking

---

## OSNet Appearance Embeddings

Since faces are blurred, visitor matching relies on:

* Clothing appearance
* Body shape
* Motion consistency

OSNet provides lightweight and effective person re-identification.

---

## Event-First Architecture

Raw detections are noisy and difficult to audit.

Event-based systems provide:

* Explainability
* Traceability
* Easier testing
* Reliable analytics

Every business metric can be traced back to one or more validated events.

---

# Event Types

The system generates the following behavioral events:

```text
visitor_entered
visitor_exited

zone_entered
zone_exited

zone_dwell

queue_joined
queue_completed
queue_abandoned

billing_zone_entered

conversion_attributed

staff_detected
staff_excluded
```

---

# Conversion Attribution Logic

A customer is marked as converted when:

```text
1. Visitor enters billing zone

AND

2. POS transaction occurs

AND

3. Transaction timestamp is within 5 minutes
   of the billing-zone observation

AND

4. Visitor is not classified as staff
```

---

# Edge Cases Covered

The design handles:

### Customer Behavior

* Group entries
* Family visits
* Multiple customers together
* Re-entry after exit

### Tracking Challenges

* Temporary occlusion
* Camera overlap
* Lost tracks
* Identity switching

### Store Operations

* Staff movement
* Queue abandonment
* Billing congestion
* Empty-store periods

### POS Challenges

* Delayed transactions
* Product-line POS records
* Transaction aggregation
* Attribution ambiguity

---

# Project Structure

```text
PurplleTechChallenge2026/
│
├── README.md
├── DESIGN.md
├── CHOICES.md
├── SUBMISSION.md
│
├── pyproject.toml
├── package.json
├── vercel.json
├── docker-compose.yml
├── .env.example
│
├── submission/
│   ├── event_log.jsonl
│   └── Purplle_Offline_Store_Analytics_Deck.pptx
│
├── demo/
│   └── dashboard.html
│
├── scripts/
│   ├── validate_event_log.py
│   └── build_demo_dashboard.py
│
├── docs/
│   ├── architecture.md
│   ├── api_contract.md
│   ├── data_contract.md
│   ├── event_lifecycle.md
│   ├── roadmap.md
│   ├── risks_and_scoring.md
│   └── source_data_inventory.md
│
├── configs/
│   └── default.yaml
│
├── data/
│   ├── examples/
│   │   ├── store_layout.example.json
│   │   ├── pos_transactions.example.csv
│   │   └── sample_events.example.jsonl
│   │
│   └── raw/
│       ├── pos_transactions.csv
│       └── sample_events.jsonl
│
├── tests/
│   ├── README.md
│   └── unit/
│       └── test_demo_dashboard.py
│
├── docker/
│   └── README.md
│
└── app/
    └── README.md
```

---

# Running Locally

## 1. Clone Repository

```bash
git clone <repository-url>
cd PurplleTechChallenge2026
```

---

## 2. Validate Event Log

```bash
python3 scripts/validate_event_log.py submission/event_log.jsonl
```

Expected Output:

```text
OK: submission/event_log.jsonl is valid JSONL for the provided schema
```

---

## 3. Run Unit Tests

```bash
python3 -m unittest discover -s tests/unit
```

Expected Output:

```text
Ran 2 tests

OK
```

---

## 4. Generate Dashboard

```bash
python3 scripts/build_demo_dashboard.py
```

---

## 5. Open Dashboard

```text
demo/dashboard.html
```

---

# Production Readiness

The proposed solution includes:

* Event schema validation
* Unit testing framework
* Configuration management
* Structured logging
* Docker deployment plan
* Database schema design
* API contracts
* Analytics documentation
* Deployment configuration

---

# Privacy & Compliance

The system is designed with privacy in mind.

### No Facial Recognition

Identity persistence relies on:

* Tracking IDs
* Appearance embeddings
* Motion consistency

### Face Blur Compatibility

The system remains operational even when faces are blurred.

### Event-Level Analytics

Analytics operate on behavioral events rather than personally identifiable information.

---

# Future Improvements

Potential enhancements include:

* Multi-camera synchronization
* Real-time dashboard streaming
* Heatmap generation
* Queue prediction models
* Product interaction analytics
* Shelf engagement tracking
* Customer path optimization
* Forecasting and anomaly detection

---

# Deliverables Included

✅ README.md

✅ DESIGN.md

✅ CHOICES.md

✅ event_log.jsonl

✅ Validation Script

✅ Dashboard Demo

✅ Documentation

✅ Deployment Configuration

✅ Unit Tests

---

# Conclusion

This solution demonstrates how retail CCTV footage and POS data can be transformed into reliable customer behavior analytics through an event-first architecture. By combining detection, tracking, re-identification, zone mapping, and transaction attribution, the platform provides measurable business insights while remaining explainable, scalable, and privacy-conscious.

The architecture prioritizes correctness, traceability, maintainability, and production readiness, making it suitable for deployment across large-scale offline retail environments.
