import os
import requests

# Koyeb API的基础URL
BASE_URL = "https://app.koyeb.com/v1"

# 你的API Token
koyeb_token = os.environ.get('KOYEB_API_TOKEN')
# 设置请求头，包含API Token
headers = {
    "Authorization": f"Bearer {koyeb_token}",
    "Content-Type": "application/json"
}

# 获取Koyeb的服务信息
def get_services():
    url = f"{BASE_URL}/services"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print("Services info:", response.json())
    else:
        print(f"Failed to fetch services. Status code: {response.status_code}, Response: {response.text}")

# 发送Telegram消息
def send_telegram_message(message):
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    
    if not bot_token or not chat_id:
        print("Telegram bot token or chat ID is missing!")
        return None

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")
        return None

if __name__ == "__main__":
    # 获取服务信息并发送到Telegram
    get_services()
    message = "服务信息已获取"
    result = send_telegram_message(message)
    if result:
        print("消息已发送到Telegram:", result)
