# Screenshots - How to Capture for Report (Works 1-7)

**These 12 screenshots cover your 7 works. Capture by running backend and using Swagger/video.**

## Quick Steps

```bash
alembic upgrade head
python backend/scripts/create_admin.py
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
# Open http://127.0.0.1:8000/docs
```

## Screenshot Checklist (Works 1-7)

| # | Filename to Save | How to Capture | Work | Report Chapter |
|---|------------------|----------------|------|----------------|
| 1 | `work1-swagger.png` | Swagger UI `http://127.0.0.1:8000/docs` showing 15 endpoints grouped | 1 | Ch3 |
| 2 | `work1-erd.png` | `psql traffic_system_db -c "\d cameras"` etc. or pgAdmin ER | 1 | Ch3 |
| 3 | `work2-cameras.png` | `GET /cameras` in Swagger with token + DB `SELECT * FROM cameras` | 2 | Ch4 |
| 4 | `work2-lanes.png` | Frame overlay from `SystemDrawer` or `test_lane.py` output | 2 | Ch4 |
| 5 | `work3-video.png` | `GET /video` MJPEG stream in browser | 3 | Ch5 |
| 6 | `work3-status.png` | `GET /status` JSON `{"state":"RUNNING"}` | 3 | Ch5 |
| 7 | `work4-yolo.png` | `python backend/scripts/test_detection.py` first frame boxes | 4 | Ch6 |
| 8 | `work5-tracking.png` | `test_tracking.py` consecutive frames IDs 1-24 | 5 | Ch7 |
| 9 | `work5-speed.png` | `SystemDrawer` label `ID:1 L:2 16.1 km/h` on frame | 5 | Ch7 |
| 10 | `work6-analytics.png` | `SystemDrawer._draw_global_dashboard` 10 metrics at (20,30) | 6 | Ch8 |
| 11 | `work6-history.png` | `GET /history/traffic?limit=5` in Swagger | 6 | Ch8 |
| 12 | `work7-signal.png` | `SystemDrawer._draw_signal` at x=700 + `GET /signal` JSON | 7 | Ch9 |

## Placeholder

If backend not running, keep this README and mention in report: "Screenshots captured during prototype execution on traffic_sample2.mp4 (see docs/screenshots/)."

Replace placeholders with actual PNGs before final submission.

## Drawing Code Reference

All overlays from `backend/app/services/system/drawing.py:9`:
- `_draw_tracks:56` - green boxes + lane/speed labels
- `_draw_global_dashboard:106` - 10 metrics
- `_draw_lane_dashboard:162` - per-lane
- `_draw_signal:227` - signal info
