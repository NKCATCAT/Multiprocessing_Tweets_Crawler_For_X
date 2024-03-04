# Packages
import time
import logging
import pandas as pd
from urllib.parse import quote
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from sqlalchemy import create_engine

# Set Crawler Time Scope
def time_scope(start_date, end_date):
    return str(start_date.month), str(start_date.day), str(start_date.year), str(end_date.month), str(end_date.day), str(end_date.year)


# Tab = "Top" or "Latest"
def top_or_latest(driver, tab):
    retry = 0
    max_retry = 5
    tab_field = None
    while retry <= max_retry:
        try:
            tab_field = driver.find_element(By.XPATH,f"//span[text()='{tab}']")
            break
        except NoSuchElementException:
            retry += 1
            time.sleep(5)
    if tab_field:
        try:
            tab_field.click()
        except:
            logging.error("Error: Cannot click the tab button \nState: The tab button detected \nPage: The query page")
            try:
                driver.quit()
            except:
                pass
            return None
    else:
        logging.error("Error: The tab button not found \nState: Query proceeded \nPage: The query page")
        try:
            driver.quit()
        except:
            pass
        return None
    time.sleep(5)
    logging.info(f"Tab {tab} selected.")
    return driver


# Search specific user's or specific words posts between specific dates 
def advanced_search(query_wordstring, query_kol, likes_straint, replies_straint, reposts_straint, driver, f_m, f_d, f_y, t_m, t_d, t_y):
    # search query
    if query_wordstring and query_kol:
        query_string = f"({query_wordstring}) (from:{query_kol}) min_faves:{likes_straint} min_replies:{replies_straint} min_retweets:{reposts_straint} until:{t_y}-{t_m}-{t_d} since:{f_y}-{f_m}-{f_d}"
    elif not query_wordstring:
        query_string = f"(from:{query_kol}) min_faves:{likes_straint} min_replies:{replies_straint} min_retweets:{reposts_straint} until:{t_y}-{t_m}-{t_d} since:{f_y}-{f_m}-{f_d}"
    else:
        query_string = f"({query_wordstring}) min_faves:{likes_straint} min_replies:{replies_straint} min_retweets:{reposts_straint} until:{t_y}-{t_m}-{t_d} since:{f_y}-{f_m}-{f_d}"
    logging.info(f"Query String:{query_string}")
    search_input_field_css = '[data-testid="SearchBox_Search_Input"]'
    retry = 0
    max_retry = 3
    search_input_field = None
    while retry <= max_retry:
        try:
            search_input_field = driver.find_element(By.CSS_SELECTOR, search_input_field_css)
            break
        except NoSuchElementException:
            retry += 1
            time.sleep(5)
    if search_input_field: 
        try:
            search_input_field.send_keys(query_string)
            time.sleep(1.5)
            search_input_field.send_keys(Keys.ENTER)
            time.sleep(5)
        except:
            logging.error("Error: Cannot send keys to the search inputbox \nState: The search inputbox detected \nPage: The explore page")
            try:
                driver.quit()
            except:
                pass
            return None
    else:
        logging.error("Error: The search inputbox not found \nState: Logged in \nPage: The explore page")
        try:
            driver.quit()
        except:
            pass
        return None
    time.sleep(5)
    return driver

# Conduct specific query
def get_query(driver,query_wordstring, query_kol, likes_straint, replies_straint, reposts_straint, tab, start_date, end_date, error_counter, error_counter_lock):
    retry = 0
    max_retry = 3
    explore_element = None
    explore_element_expr = "//a[@href='/explore']"
    while retry <= max_retry:
        try:
            explore_element = driver.find_element(By.XPATH, explore_element_expr)
            break
        except NoSuchElementException:
            retry += 1
            if retry == max_retry:
                logging.error("Error: Cannot find the explore page through XPATH error \nState: Logged In \nPage: Home Page")
    if explore_element:
        explore_element.click()
        logging.info("Clicked for the Explore Page")
        time.sleep(5)
        f_m, f_d, f_y, t_m, t_d, t_y = time_scope(start_date, end_date)
        driver = advanced_search(query_wordstring, query_kol, likes_straint, replies_straint, reposts_straint, driver, f_m, f_d, f_y, t_m, t_d, t_y)
        time.sleep(5)
        if driver:
            driver = top_or_latest(driver, tab)
            if driver is None:
                with error_counter_lock:
                    error_counter.value += 1
                logging.error("Error: Error happens during selecting tabs \nState: Query proceeded \nPage: Query page")
                try:
                    driver.quit()
                except:
                    pass
                return None
        else:
            with error_counter_lock:
                error_counter.value += 1
            logging.error("Error: Error happens during advanced search \nState: Explore page proceeded \nPage: The explore page")
            try:
                driver.quit()
            except:
                pass
            return None
    else:
        try:
            driver.get("https://twitter.com/explore")
        except Exception as e:
            with error_counter_lock:
                error_counter.value += 1
            logging.error("Error: Connot get to the explore page \n%s\nState: Logged in \nPage: X Home Page", str(e))
            try:
                driver.quit()
            except:
                pass
            return None
        time.sleep(5)
        f_m, f_d, f_y, t_m, t_d, t_y = time_scope(start_date, end_date)
        driver = advanced_search(query_wordstring, query_kol, likes_straint, replies_straint, reposts_straint, driver, f_m, f_d, f_y, t_m, t_d, t_y)
        time.sleep(5)
        if driver:
            driver = top_or_latest(driver, tab)
            if driver is None:
                with error_counter_lock:
                    error_counter.value += 1
                logging.error("Error: Error happens during selecting tabs \nState: Query proceeded \nPage: Query page")
                try:
                    driver.quit()
                except:
                    pass
                return None
    time.sleep(10)
    return driver

def advanced_search_1_24(driver,query_wordstring, query_kol, likes_straint, replies_straint, reposts_straint, tab ,start_date, end_date, error_counter, error_counter_lock):
    if tab == "Latest":
        tab_part = "&f=live"
    elif tab == "Top":
        tab_part = ""

    logging.info(f"Tab {tab} selected.")

    f_m, f_d, f_y, t_m, t_d, t_y = time_scope(start_date, end_date)

    if query_wordstring and query_kol:
        query_type = f"({query_wordstring}) (from:{query_kol})"
    elif query_wordstring is not None:
        query_type = f"({query_wordstring})"
    else:
        query_type = f"(from:{query_kol})"
    query_parts = [query_type,
        f"min_faves:{likes_straint}",
        f"min_replies:{replies_straint}",
        f"min_retweets:{reposts_straint}",
        f"until:{t_y}-{t_m}-{t_d}",
        f"since:{f_y}-{f_m}-{f_d}"
    ]
    query_string = " ".join(filter(None, query_parts))
    logging.info(f"Query String:{query_string}")
    encoded_query_string = quote(query_string)
    query_string = f"search?q={encoded_query_string}&src=typed_query"+tab_part
    try:
        driver.get("https://twitter.com/"+query_string)
    except Exception as e:
        with error_counter_lock:
            error_counter.value += 1
        logging.error("Error: Cannot get the query page \n%s \nState: Successful Logged In \nPage: X Home Page", str(e))
        try:
            driver.quit()
        except:
            pass
        return None
    time.sleep(10)
    return driver
                
# Get Search Query
def get_search_queries(sql_connector,query_database_to_use, query):
    engine = create_engine(sql_connector)
    queries = pd.read_sql(f"SELECT {query} FROM {query_database_to_use}", engine)
    if query_database_to_use != "wordstring_kol_query_database":
        queries = queries['queries'].tolist()
        engine.dispose()
    else:
        queries = [tuple(row) for row in queries['wordstring', 'kol'].itertuples(index = False)]
        engine.dispose()
    return queries
