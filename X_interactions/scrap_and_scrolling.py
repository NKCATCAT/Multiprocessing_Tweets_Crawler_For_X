# Packages
import time
import logging
import random
import pandas as pd
from itertools import cycle
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

# Modules
from Dingtalkbot.send_ding_message import send_ding_message_5
from X_interactions.login import login_and_check_account
from X_interactions.query import advanced_search_1_24
from X_interactions.showmore import filter_show_more, find_show_more_buttons
from Database.storage import get_dataframe, save_to_database
from X_accounts_management.ratelimits_availability import set_rate_limited_account, select_not_rate_limited_accounts, set_availability_account
# Scrap and Scrolling
def get_twitter_page(bot,twitter_account_database, query_database_to_use,queries, all_accounts, i,tab,sql_connector,database_tosave,start_date, end_date, likes_straint, replies_straint, reposts_straint, post_counter, counter_lock, error_counter, error_counter_lock,connectionerror_counter, connectionerror_lock, pause_event, proxy_username = None, proxy_passwords = None, proxy_ip = None, proxy_port = None):
    page_sources_1 = [] #用来存储不包含show_more的源代码
    page_sources_2 = [] #用来存储包含show_more的源代码
    counts_for_queries = 0
    driver = None
    for query in queries:
        if pause_event.is_set():
            pause_event.wait()
            send_ding_message_5(bot)
        accounts = select_not_rate_limited_accounts(sql_connector, twitter_account_database, bot)
        accounts = [item for item in accounts if item in all_accounts]
        if len(accounts) == 0:
            accounts = select_not_rate_limited_accounts(sql_connector, twitter_account_database, bot)
            random.shuffle(accounts)
        accounts = cycle(accounts)
        if query_database_to_use == "kol_query_database":
            query_kol = query
            query_wordstring = None 
        elif query_database_to_use == "wordstring_query_database":
            query_kol = None
            query_wordstring = query
        else:
            query_wordstring, query_kol = query
        if counts_for_queries % i == 0 and counts_for_queries != 0: 
            account = next(accounts)
            driver = login_and_check_account(sql_connector,account, error_counter, error_counter_lock,connectionerror_counter, connectionerror_lock)
            while driver is None:
                account = next(accounts)
                driver = login_and_check_account(sql_connector, account, error_counter, error_counter_lock,connectionerror_counter, connectionerror_lock)
        driver = advanced_search_1_24(driver,query_wordstring, query_kol,likes_straint, replies_straint, reposts_straint, tab, start_date, end_date, error_counter, error_counter_lock)
        while driver is None:
            while driver is None:
                account = next(accounts)
                driver = login_and_check_account(sql_connector, account, error_counter, error_counter_lock,connectionerror_counter, connectionerror_lock)
            driver = advanced_search_1_24(driver,query_wordstring, query_kol,likes_straint, replies_straint, reposts_straint, tab, start_date, end_date, error_counter, error_counter_lock)
        time.sleep(10)

        account_suspended_expr = (
        "//span[contains(text(), 'Your account is suspended and is not permitted to perform this action.')] | "
        "//span[contains(text(), 'Your account is suspended')]"
        )
        account_suspended_element = None
        retry = 0
        max_retry = 1
        while retry <= max_retry:
            try:
                account_suspended_element = driver.find_element(By.XPATH, account_suspended_expr)
                break
            except NoSuchElementException:
                retry += 1
                time.sleep(5)
        if account_suspended_element:
            logging.critical(f"This {account} is suspended")
            set_availability_account(sql_connector, account)
            try:
                driver.quit()
            except:
                pass
            driver = None
            while driver is None:
                account = next(accounts)
                driver = login_and_check_account(sql_connector, account, error_counter, error_counter_lock,connectionerror_counter, connectionerror_lock)
            counts_for_queries = 1
            continue

        something_went_wrong_expr = (
        "//span[contains(text(), 'Something went wrong, try')]"
        )
        something_went_wrong_element = None
        retry = 0
        max_retry = 0
        while retry <= max_retry:
            try:
                something_went_wrong_element = driver.find_element(By.XPATH, something_went_wrong_expr)
                break
            except NoSuchElementException:
                retry += 1
                time.sleep(3)
        if something_went_wrong_element:
            logging.critical(f"This {account} shows something went wrong")
            try:
                driver.quit()
            except:
                pass
            driver = None
            while driver is None:
                account = next(accounts)
                driver = login_and_check_account(sql_connector, account, error_counter, error_counter_lock,connectionerror_counter, connectionerror_lock)
            counts_for_queries = 1
            continue

        no_search_results_expr = (
        "//span[contains(text(), 'Try searching for something else')] | "
        "//span[contains(text(), 'No results for')] | "
        "//span[contains(text(), 'check your Search settings to see if they’re protecting you from potentially sensitive content')]"
        )
        no_search_results_element = None
        retry = 0
        max_retry = 1
        while retry <= max_retry:
            try:
                no_search_results_element = driver.find_element(By.XPATH, no_search_results_expr)
                logging.info("No search results for this query")
                break
            except NoSuchElementException:
                time.sleep(5)
                retry += 1
        if no_search_results_element:
            logging.info(f"Query: ({query_wordstring}, {query_kol}) is conducted")
            continue
        else:
            rate_limit_expr = (
            "//span[contains(text(), 'you are rate limited')]"
            )
            rate_limit_results_element = None
            try:
                rate_limit_results_element = driver.find_element(By.XPATH, rate_limit_expr)
            except NoSuchElementException:
                pass
            if rate_limit_results_element:
                logging.info(f"This twitter account {account} is rate limited")
                set_rate_limited_account(sql_connector, account)
                try:
                    driver.quit()
                except:
                    pass
                driver = None
                while driver is None:
                    account = next(accounts)
                    driver = login_and_check_account(sql_connector, account, error_counter, error_counter_lock,connectionerror_counter, connectionerror_lock)
                counts_for_queries = 1
                continue
            else:
                time.sleep(10)
                cellinnerdivs = None
                try:
                    cellinnerdivs = driver.find_elements(By.CSS_SELECTOR, "[data-testid='cellInnerDiv']")
                except NoSuchElementException:
                    pass
                if cellinnerdivs:
                    logging.info("Search results found and not rate limited")
                    counts_for_queries += 1
                    html_1 = driver.page_source
                    filtered_html = filter_show_more(html_1)
                    page_sources_1.append(filtered_html)
                    
                    driver, page_sources_2 = find_show_more_buttons(driver, page_sources_2)
                    scroll_count = 0
                    while True:
                        actions = ActionChains(driver)
                        actions.send_keys(Keys.PAGE_DOWN)
                        actions.perform()
                        actions.send_keys(Keys.PAGE_DOWN)
                        actions.perform()
                        
                        time.sleep(5)

                        rate_limit_results_element = None
                        try:
                            rate_limit_results_element = driver.find_element(By.XPATH, rate_limit_expr)
                            logging.info(f"This twitter account {account} is rate limited")
                            set_rate_limited_account(sql_connector, account)
                            try:
                                driver.quit()
                            except:
                                pass
                            driver = None
                            while driver is None:
                                account = next(accounts)
                                driver = login_and_check_account(sql_connector, account, error_counter, error_counter_lock,connectionerror_counter, connectionerror_lock)
                            counts_for_queries = 1
                            continue
                        except NoSuchElementException:
                            pass
                        if rate_limit_results_element is None:
                            scroll_to_bottom = False
                            cellinnerdivs = None
                            try:
                                cellinnerdivs = driver.find_elements(By.CSS_SELECTOR, "[data-testid='cellInnerDiv']")
                            except NoSuchElementException:
                                pass
                            if cellinnerdivs:
                                for cellinnerdiv in cellinnerdivs:
                                    try:
                                        cellinnerdiv.find_element(By.CSS_SELECTOR, "[data-testid='tweet']")
                                    except NoSuchElementException:
                                        scroll_to_bottom = True
                                        logging.info("Scrolled to bottom")

                            if scroll_to_bottom:
                                # 停止滑动
                                break
                            
                            scroll_count += 1
                            if scroll_count >= 500: 
                                break
                        
                            html_1 = driver.page_source
                            filtered_html = filter_show_more(html_1)
                            page_sources_1.append(filtered_html)
                            driver, page_sources_2 = find_show_more_buttons(driver, page_sources_2)
                    time.sleep(5)
                    tweets_df = get_dataframe(page_sources_1, page_sources_2,query_wordstring, query_kol)
                    if tweets_df is not None:
                        try:
                            save_to_database(sql_connector, tweets_df, database_tosave, post_counter, counter_lock)
                            page_sources_1 = [] 
                            page_sources_2 = []
                        except:
                            pass 
                    logging.info(f"Query: ({query_wordstring}, {query_kol}) is conducted")
                else:
                    logging.info("No tweets can be found or the page is waiting too long.")
                    counts_for_queries += 1