import requests

def test_ntfy_urls(ntfy_alert, ntfy_monitor):
    requests.post(ntfy_alert, data=f"This is a test from Cecil. You're ntfy server connection is working! 😀".encode(encoding='utf-8'))
    requests.post(ntfy_monitor, data=f"This is a test from Cecil. You're ntfy server connection is working! 😀".encode(encoding='utf-8'))

def send_monitor_notification(ntfy_monitor, message):
    requests.post(ntfy_monitor, data=message.encode(encoding='utf-8'))
    
def send_alert_notification(ntfy_alert, message):
    requests.post(ntfy_alert, data=message.encode(encoding='utf-8'))