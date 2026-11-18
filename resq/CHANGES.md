# Change log: SMS / alert system removed

The whole alert system (SMS via Twilio and the Gmail email fallback) was removed.

## Backend (`backend/`)
| File | Change |
|---|---|
| `app/alerts.py` | **Deleted.** It held `send_alert()` (Twilio SMS, SMTP email, 5-minute cooldown). |
| `app/main.py` | Removed `AlertReq`, the `ALERTS` list and the routes `POST /api/alerts/send`, `GET /api/alerts`, `POST /api/alerts/test`. Imports updated. |
| `app/explain.py` | **Renamed** to `app/explainability.py` (no code change). |
| `app/clustering.py` | **Renamed** to `app/incident_clustering.py` (no code change). |
| `requirements.txt` | Removed `twilio`. |

## Frontend (`frontend/index.html`)
- Removed the "Alert Center" section and its nav link.
- Removed the SEND SMS ALERT button (result stage) and the SEND SMS button on each feed item.
- Removed the alert-mode / recipient chips, the "Alert ready" checklist item, the pop-up toast, the auto-send logic and the auto demo.
- Removed the `sendSms`, `toastIf`, `alertToast` and `demoTick` functions and the related CSS.
- The backend URL is now fixed at `http://localhost:8000` inside `index.html` (`base()`), since its input box lived in Alert Center.

## What still works
Report analysis, urgency levels, explainable AI, incident clustering, live feed, command center and model comparison.
