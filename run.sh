#!/bin/bash
PYTHON_SCRIPT="./main.py"
/your/path/to/python $PYTHON_SCRIPT \
    --db "kol_query_database" \
    --start_date "2023-12-07" \
    --end_date "2024-01-24" \
    --days_per_call 5 \
    --likes_straint 0 \
    --replies_straint 0 \
    --reposts_straint 0 \
    --num_queries_per_account 5 \
    --tab "Latest" \
    --twitter_account_db "" \
    --kol_query_db "" \
    --wordstring_query_db "" \
    --wordstring_kol_query_db "" \
    --database_tosave "" \
    --sql_connector "" \
    --num_processes 12 \
    --dingtalkbot_webhook "" \
    --dingtalkbot_secret "" \
    --dingtalkbot_webhook_warning ""
