#!/usr/bin/python3
# Packages
import time
import threading
from datetime import datetime, timedelta
from sqlalchemy import create_engine
import pandas as pd
import multiprocessing
from multiprocessing import Value, Lock
import random
from dingtalkchatbot.chatbot import DingtalkChatbot
import logging
import argparse

# Modules
from Dingtalkbot.send_ding_message import send_ding_message_1, reset_and_send_hourly_count, hourly_monitor, connection_monitor
from X_interactions.query import get_search_queries
from X_interactions.scrap_and_scrolling import get_twitter_page

logging.basicConfig(
    filename='twitter_scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

parser = argparse.ArgumentParser(description='Twitter Data Collection')
parser.add_argument('--db', type=str, help='Query database to use', choices=['kol_query_database', 'wordstring_query_database', 'wordstring_kol_query_database'])
parser.add_argument('--start_date', type=str, help='Start date for crawling tweets, format YYYY-MM-DD')
parser.add_argument('--end_date', type=str, help='End date for crawling tweets, format YYYY-MM-DD')
parser.add_argument('--days_per_call', type=int, default=1, help="How many days' contents per query")    
parser.add_argument('--likes_straint', type=int, default=0, help="Leave out posts with likes below (likes_straint)")     
parser.add_argument('--replies_straint', type=int, default=0, help="Leave out posts with replies below (replies_straint)")
parser.add_argument('--reposts_straint', type=int, default=0, help="Leave out posts with reposts below (reposts_straint)")
parser.add_argument('--num_queries_per_account', type=int, default=2, help="Number of queries per account")
parser.add_argument('--tab', type=str, default="Latest", choices=['Latest', 'Top'])
parser.add_argument('--twitter_account_db', type=str, default="", help='Database for Twitter accounts')
parser.add_argument('--kol_query_db', type=str, default="", help='Database for KOL queries')
parser.add_argument('--wordstring_query_db', type=str, default="", help='Database for wordstring queries')
parser.add_argument('--wordstring_kol_query_db', type=str, default="", help='Database for combined wordstring and KOL queries')
parser.add_argument('--database_tosave', type=str, default="", help='Database to save collected posts')
parser.add_argument('--sql_connector', type=str, default="", help='SQL connection string')
parser.add_argument('--num_processes', type=int, default=1, help='Number of processes for multiprocessing')
parser.add_argument('--dingtalkbot_webhook', type=str, default="", help="X Crawler Dingtalk Bot")
parser.add_argument('--dingtalkbot_secret', type=str, default="")
parser.add_argument('--dingtalkbot_webhook_warning', type=str, default="", help="X Crawler Dingtalk Warning Bot")
''' Define Const'''

# arg
args = parser.parse_args()
query_database_to_use = args.db
start_date = datetime.strptime(args.start_date, "%Y-%m-%d") if args.start_date else datetime.now() - timedelta(days=4)
end_date = datetime.strptime(args.end_date, "%Y-%m-%d") if args.end_date else datetime.now() + timedelta(days=1)
days_per_call = args.days_per_call
likes_straint = args.likes_straint     
replies_straint = args.replies_straint
reposts_straint = args.reposts_straint
i = args.num_queries_per_account
tab = args.tab
twitter_account_database = args.twitter_account_db
kol_query_database = args.kol_query_db
wordstring_query_database = args.wordstring_query_db
wordstring_kol_query_database = args.wordstring_kol_query_db
database_tosave = args.database_tosave
sql_connector = args.sql_connector
num_processes = args.num_processes
dingtalkbot_webhook = args.dingtalkbot_webhook
dingtalkbot_secret = args.dingtalkbot_secret 
dingtalkwarningbot_webhook = args.dingtalkbot_webhook_warning

log_message = (
    f"Configuration Parameters:\n"
    f"  Query Database Used: {query_database_to_use}\n"
    f"  Start Date: {start_date.strftime('%Y-%m-%d')}\n"
    f"  End Date: {end_date.strftime('%Y-%m-%d')}\n"
    f"  Days per Call: {days_per_call}\n"
    f"  Likes Constraint: {likes_straint}\n"
    f"  Replies Constraint: {replies_straint}\n"
    f"  Reposts Constraint: {reposts_straint}\n"
    f"  Number of Queries Conducted per X Account: {i}\n"
    f"  Tab Selected: {tab}\n"
    f"  Database for Storing X Accounts: {twitter_account_database}\n"
    f"  Database for Storing KOLs Query: {kol_query_database}\n"
    f"  Database for Storing Keywords Query: {wordstring_query_database}\n"
    f"  Database for Storing KOLs & Keywords Query: {wordstring_kol_query_database}\n"
    f"  Database for Storing Posts Collected: {database_tosave}\n"
    f"  SQL Connection String: {sql_connector}\n"
    f"  Number of Processes for Multiprocessing: {num_processes}\n"
    f"  Dingtalk Bot Webhook: {dingtalkbot_webhook}\n"
    f"  Dingtalk Bot Secret: {dingtalkbot_secret}\n"
    f"  Dingtalk Warning Bot Webhook: {dingtalkwarningbot_webhook}"
)
logging.info(log_message)

if query_database_to_use == "kol_query_database":
    message_part = "****KOLs Only Query Crawler****\n\n"
elif query_database_to_use == "wordstring_query_database":
    message_part = "****Wordstrings Only Query Crawler****\n\n"
elif query_database_to_use == "wordstring_kol_query_database":
    message_part = "****KOLs & Wordstrings Query Crawler****\n\n"
start_message = (
        message_part +
        "***Crawler Process Started***\n\n"
        "**Configuration Parameters:**\n\n"
        f"- Query Database Used: `{query_database_to_use}`\n"
        f"- Start Date: `{start_date.strftime('%Y-%m-%d')}`\n"
        f"- End Date: `{end_date.strftime('%Y-%m-%d')}`\n"
        f"- Days per Call: `{days_per_call}`\n"
        f"- Likes Constraint: `{likes_straint}`\n"
        f"- Replies Constraint: `{replies_straint}`\n"
        f"- Reposts Constraint: `{reposts_straint}`\n"
        f"- Number of Queries per X Account: `{i}`\n"
        f"- Tab Selected: `{tab}`\n"
        f"- Database for Posts Storage: `{database_tosave}`\n"
        f"- SQL Connection String: `{sql_connector}`\n"
        f"- Number of Processes: `{num_processes}`"
)
post_counter = Value('i', 0)
counter_lock = Lock()
error_counter = Value('i', 0)
error_counter_lock = Lock()
connectionerror_counter = Value('i', 0)
connectionerror_lock = Lock()

pause_event = threading.Event()


bot = DingtalkChatbot(dingtalkbot_webhook, dingtalkbot_secret)
bot_warning = DingtalkChatbot(dingtalkwarningbot_webhook)
first_call = [True,]
send_ding_message_1(bot, start_message)
reset_and_send_hourly_count(bot, post_counter, counter_lock,first_call)
hourly_monitor(bot_warning, error_counter, error_counter_lock)
connection_monitor(bot_warning, connectionerror_counter, connectionerror_lock, pause_event)

'''Load Data'''
# Load Queries
if query_database_to_use == "kol_query_database" or query_database_to_use == "wordstring_query_database":
    query = "queries"
    queries = get_search_queries(sql_connector, query_database_to_use, query)
elif query_database_to_use == "wordstring_kol_query_database":
    query = "wordstring, kol"
    queries = get_search_queries(sql_connector, query_database_to_use, query)

# Load Twitter Accounts
def get_twitter_accounts(sql_connector, twitter_account_database):
    engine = create_engine(sql_connector)
    accounts = pd.read_sql(f"SELECT email_, username, password, email_password, two_fa_link FROM {twitter_account_database} WHERE availability = 1", engine)
    all_accounts = [tuple(row) for row in accounts.itertuples(index = False)]
    return all_accounts
all_accounts = get_twitter_accounts(sql_connector, twitter_account_database)


'''Shuffle and Split queries and accounts into chunks for multi-processing.'''
# Shuffle the lists
random.shuffle(all_accounts)
random.shuffle(queries)

# Split data into chunks
num_processes = num_processes  # Set the number of processes as needed
chunk_size_1 = len(all_accounts) // num_processes
chunk_size_2 = len(queries) // num_processes
account_chunks = [all_accounts[i:i + chunk_size_1] for i in range(0, len(all_accounts), chunk_size_1)]
queries_chunks = [queries[i:i + chunk_size_2] for i in range(0, len(queries), chunk_size_2)]

current_start_date = start_date
while current_start_date < end_date:
    current_end_date = current_start_date + timedelta(days = days_per_call)
    # Create and start processes
    processes = []
    for accounts_chunk, queries_chunk in zip(account_chunks, queries_chunks):
        process = multiprocessing.Process(target=get_twitter_page, args=(bot,twitter_account_database, query_database_to_use,queries_chunk, accounts_chunk, i, tab, sql_connector, database_tosave, current_start_date, current_end_date,likes_straint, replies_straint, reposts_straint, post_counter, counter_lock, error_counter, error_counter_lock,connectionerror_counter, connectionerror_lock, pause_event))
        processes.append(process)
        process.start()
    # Wait for all processes to finish
    for process in processes:
        process.join()
    logging.info(f"Queries between {current_start_date} and {current_end_date} is conducted.")
    current_start_date = current_end_date + timedelta(days = 1)
    time.sleep(10)