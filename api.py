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

# 获取Koyeb的活动信息
def get_last_login_dates():
    url = f"{BASE_URL}/activities?limit=10"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        activities = response.json().get('activities', [])
        login_dates = []
        
        # 遍历活动记录，查找与登录相关的活动
        for activity in activities:
            # 检查活动是否与登录相关（判断 'console' 作为活动对象名称）
            if activity.get('object', {}).get('name') == "console":
                created_at = activity.get('created_at')
                login_dates.append(created_at)
                
            if len(login_dates) >= 2:  # 只需要最近两次登录记录
                break
        
        if len(login_dates) >= 2:
            current_login = login_dates[0]  # 最近一次登录
            last_login = login_dates[1]     # 上一次登录
            return current_login, last_login
        elif len(login_dates) == 1:
            return login_dates[0], None
        else:
            return None, None
    else:
        print(f"Failed to fetch activities. Status code: {response.status_code}, Response: {response.text}")
        return None, None

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

# 获取活动并提取登录日期，发送到Telegram
def report_login_dates():
    current_login, last_login = get_last_login_dates()
    
    if current_login and last_login:
        message = f"Koyeb当前登录日期: `{current_login}`\nKoyeb上次登录日期: `{last_login}`"
    elif current_login:
        message = f"Koyeb当前登录日期: `{current_login}`\nKoyeb上次登录日期: 无法获取"
    else:
        message = "Koyeb无法获取登录日期"
    
    result = send_telegram_message(message)
    if result:
        print("消息已发送到Telegram:", result)

if __name__ == "__main__":
    # 获取登录日期并发送到Telegram
    report_login_dates()
