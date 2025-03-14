import requests
import time

import os

SESSION_ID = os.getenv("SESSION_ID")

# آدرس API روبیکا
API_URL = "https://messenger.rubika.ir/api"


def get_updates():
    """دریافت پیام‌های جدید از روبیکا"""
    response = requests.post(API_URL, json={
        "api_version": "5",
        "auth": SESSION_ID,
        "data": {"last_update_id": 0}
    })

    if response.status_code == 200:
        return response.json().get("updates", [])
    return []


def delete_message(object_guid, message_id):
    """حذف پیام از گروه"""
    requests.post(API_URL, json={
        "api_version": "5",
        "auth": SESSION_ID,
        "data": {
            "object_guid": object_guid,
            "message_id": message_id
        }
    })


def send_message(object_guid, text):
    """ارسال پیام به گروه"""
    requests.post(API_URL, json={
        "api_version": "5",
        "auth": SESSION_ID,
        "data": {
            "object_guid": object_guid,
            "text": text
        }
    })


def handle_message(message):
    """پردازش پیام دریافتی و انجام اقدامات لازم"""
    text = message.get("text", "")
    object_guid = message.get("object_guid")
    message_id = message.get("message_id")

    # پاسخ به دستورات
    if text.startswith("/start"):
        send_message(object_guid, "✅ ربات مدیریت گروه فعال شد!")
    elif text.startswith("/help"):
        send_message(object_guid, "📌 دستورات ربات:\n/start - شروع ربات\n/help - نمایش راهنما")

    # حذف لینک‌ها
    if "http" in text or "www." in text:
        delete_message(object_guid, message_id)
        send_message(object_guid, "🚫 ارسال لینک در گروه مجاز نیست!")


if __name__ == "__main__":
    print("🤖 ربات مدیریت گروه روبیکا شروع به کار کرد!")
    while True:
        updates = get_updates()
        for update in updates:
            handle_message(update)
        time.sleep(5)
