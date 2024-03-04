# Packages
import threading
import logging
import time
import subprocess
from datetime import datetime, timedelta

def send_ding_message_1(bot, message):
    # Format the current time
    time_now = datetime.now() + timedelta(hours=8)
    timestamp = time_now.strftime("[%Y-%m-%d %H:%M:%S]")
    # Construct the formatted message using Markdown
    formatted_message = (
        f"**🕒 时间戳**: {timestamp}\n\n") + message
    
    # Send the message via DingTalk bot
    response = bot.send_markdown("爬虫环境",formatted_message)
    if response['errcode'] != 0:
        logging.info('DingTalk message failed, error code: {response["errcode"]}, error message: {response["errmsg"]}, message: {formatted_message}')

def send_ding_message_2(bot, post_counter):
    time_now = datetime.now() + timedelta(hours=8)
    timestamp = time_now.strftime("[%Y-%m-%d %H:%M:%S]")
    count = post_counter.value
    formatted_message = (
        f"**🕒 时间戳**: {timestamp}\n\n"  
        "----\n\n"  
        f"**📊 本小时收集的 Posts 数量**: {count}\n\n" 
    )
    response = bot.send_markdown("每小时帖子爬取情况",formatted_message)
    if response['errcode'] != 0:
        logging.info(f'DingTalk message failed, error code: {response["errcode"]}, error message: {response["errmsg"]}, message: {formatted_message}')

def reset_and_send_hourly_count(bot, post_counter, counter_lock, first_call):
    with counter_lock:
        if not first_call[0]:
            send_ding_message_2(bot, post_counter)
            post_counter.value = 0
        else:
            first_call[0] = False
    threading.Timer(3600, reset_and_send_hourly_count, [bot, post_counter, counter_lock, first_call]).start()

def send_ding_warning(bot_warning, error_counter):
    time_now = datetime.now() + timedelta(hours=8)
    timestamp = time_now.strftime("[%Y-%m-%d %H:%M:%S]")
    count = error_counter.value
    formatted_message = (
        f"**🕒 时间戳**: {timestamp}\n\n"  
        "----\n\n"  
        "**important WARNING**\n\n" 
        f"-- 本小时检测到的 errors: {count}\n\n" 
        f"-- X爬虫已停止，请进行日志审查以识别和分析详细的错误信息。"
    )
    response = bot_warning.send_markdown("WARNING",formatted_message)
    if response['errcode'] != 0:
        logging.info(f'DingTalk message failed, error code: {response["errcode"]}, error message: {response["errmsg"]}, message: {formatted_message}')

def hourly_monitor(bot_warning, error_counter, error_counter_lock):
    with error_counter_lock:
        if error_counter.value >= 500:
            send_ding_warning(bot_warning, error_counter)
            error_counter.value = 0
            ## 停止
            try:
                subprocess.run(['pkill', '-f', '/home/tangshuo/my_cron_venv/bin/python3 ./main.py'])
                subprocess.run(['pkill', 'chrome'])
            except Exception as e:
                logging.error("Error: Cannot shut down the process \n%s", str(e))
                pass
        else:
            pass
    threading.Timer(3600, hourly_monitor,[bot_warning, error_counter, error_counter_lock]).start()

def send_ding_message_3(bot):
    time_now = datetime.now() + timedelta(hours=8)
    timestamp = time_now.strftime("[%Y-%m-%d %H:%M:%S]")
    formatted_message = (
        f"**🕒 时间戳**: {timestamp}\n\n"
        f"**Important Info**\n\n"
        "所有可用X账户均已达到阅读限制。本次数据抓取已停止。"
    )
    response = bot.send_markdown("Rate Limited",formatted_message)
    if response['errcode'] != 0:
        logging.info(f'DingTalk message failed, error code: {response["errcode"]}, error message: {response["errmsg"]}, message: {formatted_message}')
    try:
        subprocess.run(['pkill', '-f', '/home/tangshuo/my_cron_venv/bin/python3 ./main.py'])
        subprocess.run(['pkill', 'chrome'])
    except Exception as e:
        logging.error("Error: Cannot shutdown the process \n%s", str(e))
        pass

def send_ding_message_4(bot):
    time_now = datetime.now() + timedelta(hours=8)
    timestamp = time_now.strftime("[%Y-%m-%d %H:%M:%S]")
    formatted_message = (
        f"**🕒 时间戳**: {timestamp}\n\n"
        f"**Regular Info**\n\n"
        "每日可用X账号阅读限制清零"
    )
    response = bot.send_markdown("Rate Limited Daily Clear Up",formatted_message)
    if response['errcode'] != 0:
        logging.info(f'DingTalk message failed, error code: {response["errcode"]}, error message: {response["errmsg"]}, message: {formatted_message}')

def send_ding_warning_1(bot):
    time_now = datetime.now() + timedelta(hours=8)
    timestamp = time_now.strftime("[%Y-%m-%d %H:%M:%S]")
    formatted_message = (
        f"**🕒 时间戳**: {timestamp}\n\n"
        f"**important WARNING**\n\n"
        "网络连接异常，请检查VPN。X爬虫已经暂时停止。\n\n"
        "一小时后重试"
    )
    response = bot.send_markdown("Error Connection",formatted_message)
    if response['errcode'] != 0:
        logging.info(f'DingTalk message failed, error code: {response["errcode"]}, error message: {response["errmsg"]}, message: {formatted_message}')

def connection_monitor(bot_warning, connectionerror_counter, connectionerror_lock, pause_event):
    with connectionerror_lock:
        if connectionerror_counter.value >= 150:
            send_ding_warning_1(bot_warning)
            connectionerror_counter.value = 0
            pause_event.set()
            time.sleep(3600)
            pause_event.clear()
        else:
            pass
    threading.Timer(600, connection_monitor,[bot_warning,connectionerror_counter, connectionerror_lock, pause_event]).start()

def send_ding_message_5(bot):
    time_now = datetime.now() + timedelta(hours=8)
    timestamp = time_now.strftime("[%Y-%m-%d %H:%M:%S]")
    formatted_message = (
        f"**🕒 时间戳**: {timestamp}\n\n"
        f"**Important Info**\n\n"
        "X爬虫重新启动"
    )
    response = bot.send_markdown("X Crawler Resumes",formatted_message)
    if response['errcode'] != 0:
        logging.info(f'DingTalk message failed, error code: {response["errcode"]}, error message: {response["errmsg"]}, message: {formatted_message}')
