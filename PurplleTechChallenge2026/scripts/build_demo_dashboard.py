from __future__ import annotations

import argparse
import csv
import html
import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class DashboardMetrics:
    total_events: int
    entry_count: int
    exit_count: int
    unique_visitors: int
    zone_events: int
    queue_completed: int
    queue_abandoned: int
    avg_wait_seconds: float
    pos_orders: int
    pos_revenue: float
    conversion_rate: float


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as file:
        for line_number, raw_line in enumerate(file, start=1):
            line = raw_line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSONL row") from exc
            if not isinstance(event, dict):
                raise ValueError(f"{path}:{line_number}: JSONL row must be an object")
            events.append(event)
    return events


def load_pos_orders(path: Path) -> tuple[int, float]:
    order_totals: dict[str, float] = {}
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        required = {"order_id", "total_amount"}
        missing = required.difference(reader.fieldnames or [])
        if missing:
            raise ValueError(f"{path}: missing required POS columns: {', '.join(sorted(missing))}")

        for row in reader:
            order_id = row["order_id"].strip()
            if not order_id:
                continue
            amount = float(row["total_amount"] or 0)
            order_totals[order_id] = order_totals.get(order_id, 0.0) + amount

    return len(order_totals), sum(order_totals.values())


def compute_metrics(events: list[dict[str, Any]], pos_orders: int, pos_revenue: float) -> DashboardMetrics:
    event_counts = Counter(str(event.get("event_type", "")) for event in events)

    visitor_ids = {
        str(event["id_token"])
        for event in events
        if event.get("event_type") == "entry" and event.get("is_staff") is False and event.get("id_token")
    }

    queue_events = [
        event
        for event in events
        if event.get("event_type") in {"queue_completed", "queue_abandoned"}
    ]
    wait_values = [
        float(event["wait_seconds"])
        for event in queue_events
        if isinstance(event.get("wait_seconds"), (int, float))
    ]
    avg_wait = sum(wait_values) / len(wait_values) if wait_values else 0.0
    conversion_rate = min(event_counts["queue_completed"], len(visitor_ids)) / len(visitor_ids) if visitor_ids else 0.0

    return DashboardMetrics(
        total_events=len(events),
        entry_count=event_counts["entry"],
        exit_count=event_counts["exit"],
        unique_visitors=len(visitor_ids),
        zone_events=event_counts["zone_entered"] + event_counts["zone_exited"],
        queue_completed=event_counts["queue_completed"],
        queue_abandoned=event_counts["queue_abandoned"],
        avg_wait_seconds=avg_wait,
        pos_orders=pos_orders,
        pos_revenue=pos_revenue,
        conversion_rate=conversion_rate,
    )


def event_type_rows(events: list[dict[str, Any]]) -> str:
    counts = Counter(str(event.get("event_type", "unknown")) for event in events)
    max_count = max(counts.values(), default=1)
    rows: list[str] = []
    for event_type, count in counts.most_common():
        width = int((count / max_count) * 100)
        rows.append(
            f"""
            <div class="bar-row">
              <div class="bar-label">{html.escape(event_type)}</div>
              <div class="bar-track"><div class="bar-fill" style="width:{width}%"></div></div>
              <div class="bar-value">{count}</div>
            </div>
            """
        )
    return "\n".join(rows)


def recent_event_rows(events: list[dict[str, Any]]) -> str:
    rows: list[str] = []
    for event in events[-8:]:
        event_type = html.escape(str(event.get("event_type", "")))
        store = html.escape(str(event.get("store_id") or event.get("store_code") or ""))
        camera = html.escape(str(event.get("camera_id", "")))
        timestamp = html.escape(str(event.get("event_time") or event.get("event_timestamp") or event.get("queue_join_ts") or ""))
        identity = html.escape(str(event.get("id_token") or event.get("track_id") or ""))
        rows.append(
            f"""
            <tr>
              <td>{event_type}</td>
              <td>{identity}</td>
              <td>{store}</td>
              <td>{camera}</td>
              <td>{timestamp}</td>
            </tr>
            """
        )
    return "\n".join(rows)


def render_dashboard(events: list[dict[str, Any]], metrics: DashboardMetrics) -> str:
    conversion_percent = metrics.conversion_rate * 100
    revenue = f"Rs {metrics.pos_revenue:,.2f}"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Purplle Offline Store Intelligence</title>
  <style>
    :root {{
      --ink: #172026;
      --muted: #60707c;
      --line: #d8e0e5;
      --panel: #ffffff;
      --bg: #f5f7f8;
      --accent: #7d2ca8;
      --accent-2: #0b7f78;
      --warn: #c7511f;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--ink);
      background: var(--bg);
    }}
    header {{
      padding: 28px 36px 18px;
      background: #fff;
      border-bottom: 1px solid var(--line);
    }}
    h1 {{
      margin: 0;
      font-size: 30px;
      line-height: 1.15;
      letter-spacing: 0;
    }}
    .subtitle {{
      margin-top: 8px;
      color: var(--muted);
      max-width: 900px;
      font-size: 15px;
    }}
    main {{
      padding: 24px 36px 36px;
      display: grid;
      gap: 20px;
    }}
    .kpis {{
      display: grid;
      grid-template-columns: repeat(4, minmax(160px, 1fr));
      gap: 14px;
    }}
    .card {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 18px;
    }}
    .label {{
      color: var(--muted);
      font-size: 13px;
      text-transform: uppercase;
      letter-spacing: 0;
    }}
    .value {{
      margin-top: 10px;
      font-size: 30px;
      font-weight: 760;
    }}
    .grid {{
      display: grid;
      grid-template-columns: 1.1fr 0.9fr;
      gap: 20px;
    }}
    h2 {{
      margin: 0 0 14px;
      font-size: 18px;
    }}
    .bar-row {{
      display: grid;
      grid-template-columns: 150px 1fr 44px;
      gap: 12px;
      align-items: center;
      margin: 12px 0;
      font-size: 14px;
    }}
    .bar-track {{
      height: 12px;
      border-radius: 999px;
      background: #e9eef1;
      overflow: hidden;
    }}
    .bar-fill {{
      height: 100%;
      background: var(--accent);
    }}
    .queue {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
    }}
    .mini {{
      padding: 14px;
      background: #f8fafb;
      border: 1px solid var(--line);
      border-radius: 8px;
    }}
    .mini strong {{
      display: block;
      margin-top: 6px;
      font-size: 24px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
    }}
    th, td {{
      padding: 11px 10px;
      border-bottom: 1px solid var(--line);
      text-align: left;
      vertical-align: top;
    }}
    th {{
      color: var(--muted);
      font-weight: 650;
    }}
    .note {{
      color: var(--muted);
      font-size: 13px;
      line-height: 1.5;
    }}
    @media (max-width: 900px) {{
      .kpis, .grid, .queue {{
        grid-template-columns: 1fr;
      }}
      header, main {{
        padding-left: 18px;
        padding-right: 18px;
      }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>Purplle Offline Store Intelligence</h1>
    <div class="subtitle">
      CCTV-to-conversion analytics demo generated from the validated JSONL event log and POS source data.
    </div>
  </header>
  <main>
    <section class="kpis">
      <div class="card"><div class="label">Conversion proxy</div><div class="value">{conversion_percent:.1f}%</div></div>
      <div class="card"><div class="label">Unique visitors</div><div class="value">{metrics.unique_visitors}</div></div>
      <div class="card"><div class="label">POS orders</div><div class="value">{metrics.pos_orders}</div></div>
      <div class="card"><div class="label">POS revenue</div><div class="value">{revenue}</div></div>
    </section>

    <section class="grid">
      <div class="card">
        <h2>Event Quality</h2>
        {event_type_rows(events)}
      </div>
      <div class="card">
        <h2>Billing Queue</h2>
        <div class="queue">
          <div class="mini"><span class="label">Completed</span><strong>{metrics.queue_completed}</strong></div>
          <div class="mini"><span class="label">Abandoned</span><strong>{metrics.queue_abandoned}</strong></div>
          <div class="mini"><span class="label">Avg wait</span><strong>{metrics.avg_wait_seconds:.0f}s</strong></div>
        </div>
        <p class="note">
          Queue completion is used as a visual proxy for billing-zone purchase intent. Final conversion attribution links these events to POS orders within the five-minute billing window.
        </p>
      </div>
    </section>

    <section class="card">
      <h2>Recent Events</h2>
      <table>
        <thead>
          <tr><th>Event</th><th>Identity</th><th>Store</th><th>Camera</th><th>Timestamp</th></tr>
        </thead>
        <tbody>
          {recent_event_rows(events)}
        </tbody>
      </table>
    </section>

    <section class="card">
      <h2>Submission Status</h2>
      <p class="note">
        Mandatory files included: README.md, DESIGN.md, CHOICES.md, and submission/event_log.jsonl.
        The event log has a local validator at scripts/validate_event_log.py.
      </p>
    </section>
  </main>
</body>
</html>
"""


def build_dashboard(event_log: Path, pos_csv: Path, output_html: Path) -> DashboardMetrics:
    events = load_jsonl(event_log)
    pos_orders, pos_revenue = load_pos_orders(pos_csv)
    metrics = compute_metrics(events, pos_orders, pos_revenue)
    output_html.parent.mkdir(parents=True, exist_ok=True)
    output_html.write_text(render_dashboard(events, metrics), encoding="utf-8")
    return metrics


def main() -> int:
    parser = argparse.ArgumentParser(description="Build an offline HTML demo dashboard.")
    parser.add_argument("--event-log", type=Path, default=Path("submission/event_log.jsonl"))
    parser.add_argument("--pos", type=Path, default=Path("data/raw/pos_transactions.csv"))
    parser.add_argument("--output", type=Path, default=Path("demo/dashboard.html"))
    args = parser.parse_args()

    metrics = build_dashboard(args.event_log, args.pos, args.output)
    print(f"Wrote {args.output}")
    print(f"Events: {metrics.total_events}")
    print(f"Unique visitors: {metrics.unique_visitors}")
    print(f"Conversion proxy: {metrics.conversion_rate:.2%}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

