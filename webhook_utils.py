import requests

def send_notification(message, use_webhook=False):
    if use_webhook:
        webhook_url = "https://hooks.slack.com/services/..."  # Replace with your actual webhook URL
        payload = {"text": message}
        try:
            requests.post(webhook_url, json=payload, timeout=5)
        except Exception:
            pass  # Silently ignore if fails in demo mode
    # If not enabled, simply do nothing (no-op)
