import requests

def test_ntfy_urls(ntfy_alert, ntfy_monitor):
    requests.post(ntfy_alert, data=f"This is a test from Cecil. You're ntfy server connection is working! 😀".encode(encoding='utf-8'))
    requests.post(ntfy_monitor, data=f"This is a test from Cecil. You're ntfy server connection is working! 😀".encode(encoding='utf-8'))
