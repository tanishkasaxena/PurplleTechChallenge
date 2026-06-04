from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.build_demo_dashboard import build_dashboard, compute_metrics


class DemoDashboardTests(unittest.TestCase):
    def test_compute_metrics_counts_visitors_and_queue_events(self) -> None:
        events = [
            {"event_type": "entry", "id_token": "ID_1", "is_staff": False},
            {"event_type": "entry", "id_token": "ID_2", "is_staff": True},
            {"event_type": "queue_completed", "wait_seconds": 10},
            {"event_type": "queue_abandoned", "wait_seconds": 20},
        ]

        metrics = compute_metrics(events, pos_orders=1, pos_revenue=100.0)

        self.assertEqual(metrics.unique_visitors, 1)
        self.assertEqual(metrics.queue_completed, 1)
        self.assertEqual(metrics.queue_abandoned, 1)
        self.assertEqual(metrics.avg_wait_seconds, 15)
        self.assertEqual(metrics.conversion_rate, 1)

    def test_build_dashboard_writes_html(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            event_log = root / "events.jsonl"
            pos = root / "pos.csv"
            output = root / "dashboard.html"

            event_log.write_text(
                '{"event_type":"entry","id_token":"ID_1","store_code":"store","camera_id":"cam1",'
                '"event_timestamp":"2026-01-01T10:00:00","is_staff":false}\n',
                encoding="utf-8",
            )
            pos.write_text(
                "order_id,order_date,order_time,store_id,product_id,brand_name,total_amount\n"
                "1,10-04-2026,12:15:05,ST1008,399945,Faces Canada,302.33\n",
                encoding="utf-8",
            )

            metrics = build_dashboard(event_log, pos, output)

            self.assertEqual(metrics.pos_orders, 1)
            self.assertTrue(output.exists())
            self.assertIn("Purplle Offline Store Intelligence", output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

