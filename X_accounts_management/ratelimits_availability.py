# Packages
import sys
import logging
import argparse
import pandas as pd
from itertools import cycle
from sqlalchemy import create_engine
from dingtalkchatbot.chatbot import DingtalkChatbot
sys.path.append("..")
# Modules
from Dingtalkbot.send_ding_message import send_ding_message_3, send_ding_message_4
parser = argparse.ArgumentParser(description='Rate Limited Accounts Daily Clear Up')
parser.add_argument('--dingtalkbot_webhook', type=str, default="", help="X Crawler Dingtalk Bot")
parser.add_argument('--dingtalkbot_secret', type=str, default="")

def set_rate_limited_account(sql_connector, account):
    email = account[0]
    engine = create_engine(sql_connector)
    sql_cmd = '''
    UPDATE twitter_account_database
    SET is_rate_limited_now = 1
    WHERE email_ = %s
    '''
    with engine.connect() as conn:
        conn.execute(sql_cmd, (email,))

def set_availability_account(sql_connector, account):
    if not isinstance(account, tuple):
        email = account
    else:
        email = account[0]
    engine = create_engine(sql_connector)
    sql_cmd = '''
    UPDATE twitter_account_database
    SET availability = 0
    WHERE email_ = %s
    '''
    with engine.connect() as conn:
        conn.execute(sql_cmd, (email,))

def select_not_rate_limited_accounts(sql_connector, twitter_account_database, bot):
    engine = create_engine(sql_connector)
    accounts = pd.read_sql(f"SELECT email_, username, password, email_password, two_fa_link FROM {twitter_account_database} WHERE is_rate_limited_now = 0 AND availability = 1", engine)
    accounts = [tuple(row) for row in accounts.itertuples(index = False)]
    if len(accounts) > 0:
        engine.dispose()
        return accounts
    else:
        logging.critical("!!!All accounts are rate limited.")
        send_ding_message_3(bot)
        return None
    
def daily_clear_up(sql_connector, twitter_account_database):
    engine = create_engine(sql_connector)
    sql_cmd = f'''
    UPDATE {twitter_account_database}
    SET is_rate_limited_now = 0
    '''
    with engine.connect() as conn:
        conn.execute(sql_cmd) 
    logging.info("Rate Limited Daily Clear Up")

if __name__ == "__main__":
    args = parser.parse_args()
    bot = DingtalkChatbot(args.dingtalkbot_webhook, args.dingtalkbot_secret)
    send_ding_message_4(bot)