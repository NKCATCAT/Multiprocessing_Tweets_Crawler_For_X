#%%
# Packages
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import re
import imaplib
import email
import logging

# Modules
from X_accounts_management.ratelimits_availability import set_availability_account
from X_interactions.two_fa_code_request import get_2fa_code

# avoid error
def login_and_check_account(sql_connector,account,error_counter, error_counter_lock, connectionerror_counter, connectionerror_lock):
    try:
        email_, username, password, email_password,two_fa_link = account
    except:
        two_fa_link = None
        email_, username, password, email_password = account
    try:
        driver = twitter_login(sql_connector, email_, username, password, email_password, two_fa_link,error_counter, error_counter_lock, None, None, None, None)
        if driver:
            driver.maximize_window()
            time.sleep(6)
    except Exception as e:
        if "net::ERR_CONNECTION_CLOSED" in str(e):
            with connectionerror_lock:
                connectionerror_counter.value += 1
            logging.error("Error: Connection Error \nState: Log in Procedure \nPage: Log in Page")
        else:
            with error_counter_lock:
                error_counter.value += 1
            logging.error("Error: Log in error \n %s \nState: Log in Procedure \nPage: Log in Page", str(e))
        try:
            driver.quit()
        except:
            pass
        return None
    return driver


def get_server_address(username):
    server = re.search(r'@(hotmail\.com|outlook\.com)$', username)
    if server:
        server_address = "imap-mail.outlook.com"
    else:
        server = re.search(r'(@gmail\.com)$', username)
        if server:
            server_address = "imap.gmail.com"
        else:
            server = re.search(r'(@yahoo\.com)$', username)
            if server:
                server_address = "imap.mail.yahoo.com"
            else:
                server = re.search(r'(@autorambler.ru)$', username)
                if server:
                    server_address = "imap.rambler.ru"
    return server_address

# Deal mail inspection if encountered
def get_mail_verified(username, password):
    server_address = get_server_address(username)   
    mail = imaplib.IMAP4_SSL(server_address)
    code = None
    try:
        mail.login(username, password)
        mail.select("inbox")
        # Search Mails
        result, data = mail.uid('search', None, "ALL")
        # Fetch the Mail List
        email_list = data[0].split()
        if email_list:
            # Fetch the latest mail
            latest = email_list[-1]
            # Fetch the body of the latest mail
            result, email_data = mail.uid('fetch', latest, '(BODY.PEEK[TEXT])')
            raw_email = email_data[0][1].decode("utf-8")
            # Parse raw mail
            email_message = email.message_from_string(raw_email)
        
            # Get Verification Code
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    html_content = part.get_payload(decode=True)
                    soup = BeautifulSoup(html_content, "html.parser")
                    text = soup.get_text()
                    clean_text = re.sub(r'\s+', ' ', text)
                    verified_code = re.search(r'single-use code. (\w+)', clean_text)
                    if verified_code:
                        code = verified_code.group(1)
    except Exception as e:
        logging.error("Error: Email verified error \n%s \nState: Extra checks detected \nPage: Extra checks page", str(e))
        code = None
    return code


# Log in
def twitter_login(sql_connector, email, username, password, email_password, two_fa_link ,error_counter, error_counter_lock,proxy_username, proxy_password, proxy_ip, proxy_port):

    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--lang=en")
    chrome_options.add_argument('accept-language=en')
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
    chrome_options.add_argument("--headless=new")

    ''' Web Driver '''
    webdriver_service = Service('./chromedriver-linux64/chromedriver')
    webdriver_service.log_path = './chromedriver.log'  # 设置日志路径
    driver = webdriver.Chrome(service = webdriver_service, options=chrome_options)
    driver.maximize_window()
    driver.delete_all_cookies()
    #webdriver_service = Service(ChromeDriverManager().install())
    #driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

    try:
        ''' Direct to the login page '''
        driver.get('https://twitter.com/i/flow/login')
        time.sleep(7.5)


        ''' Buttons '''
        # Next button
        next_expr = (
        "//span[text()='下一步'] | "
        "//span[text()='Next']"
        )

        # Login button
        login_button_expr = (
            "//span[text()='Log in'] | "
            "//span[text()='登录']"
        )


        ''' Network Errors '''
        xpath_expr_1 = (
        "//span[text()='出错了，但别担心，这不是你的错'] | "
        "//span[text()='Something went wrong, but don’t fret — let’s give it another shot.'] | "
        "//span[text()='出错了，请重试'] | "
        "//span[text()='Something went wrong. Try reloading.']"
        )
        try:
            login_error = driver.find_element(By.XPATH, xpath_expr_1)
            if login_error:
                login_error.click()
                time.sleep(3)
        except NoSuchElementException:
            pass
        time.sleep(3)

        ''' Login Procedures '''
        # Login email
        retry = 0
        max_retry = 5
        email_field = None
        while retry <= max_retry:
            try:
                email_field = driver.find_element(By.NAME, "text")
                break
            except NoSuchElementException:
                retry += 1
                time.sleep(3)
        if email_field:
            email_field.send_keys(email)
            try:
                next_button = driver.find_element(By.XPATH, next_expr)
            except NoSuchElementException as e:
                with error_counter_lock:
                    error_counter.value += 1
                logging.error("Error: the 'Next' button not found with error: \n%s \nState: Email input box detected \nPage: The email page",str(e))
                try:
                    driver.quit()
                except:
                    pass
                return None

            if next_button:
                try:
                    next_button.click()
                except Exception as e:
                    with error_counter_lock:
                        error_counter.value += 1
                    logging.error("Error: the 'Next' button cannot be clicked with error: \n%s \nState: Email entered \nPage: The email page",str(e))
        else:
            with error_counter_lock:
                error_counter.value += 1
            logging.error("Error: the email inputbox not found \nState: Unknown \nPage: The email page")
            try:
                driver.quit()
            except:
                pass
            return None
        time.sleep(10)

        # Unusual Activity Check
        xpath_expr_2 = (
        "//span[contains(text(),'Enter your phone number or username')] | "
        "//span[contains(text(),'unusual login activity')] | "
        "//span[contains(text(),'输入你的手机号码或用户名')]"
        )
        retry = 0
        max_retry = 1
        unusual_activity_check = None
        while retry <= max_retry:
            try:
                unusual_activity_check = driver.find_element(By.XPATH, xpath_expr_2) 
                break
            except NoSuchElementException:
                retry += 1
                time.sleep(5)
        if unusual_activity_check:
            username_inputbox = driver.find_element(By.NAME, 'text')
            username_inputbox.send_keys(username)
            try:
                next_button = driver.find_element(By.XPATH, next_expr)
            except NoSuchElementException as e:
                with error_counter_lock:
                    error_counter.value += 1
                logging.error("Info: The 'Next' button not found with error: \n %s \nState: unusual activity check inputbox detected \nPage: The unusual activity check page", str(e))
                try:
                    driver.quit()
                except:
                    pass
                return None
            if next_button:
                try:
                    next_button.click()
                except Exception as e:
                    with error_counter_lock:
                        error_counter.value += 1
                    logging.error("Error: the 'Next' button cannot be clicked with error: \n %s \nState: Email entered \nPage: The email page", str(e))
        else:
            logging.info("Info: the unusual check inputbox not detected \nState: Unknown \nPage: The password page or the unusual activity check page")
        time.sleep(10)

        # Login password
        retry = 0
        max_retry = 5
        password_field = None
        while retry <= max_retry:
            try:
                password_field = driver.find_element(By.NAME, "password")
                break
            except:
                retry += 1
                time.sleep(5)
        if password_field:
            password_field.send_keys(password)
            try:
                login_button = driver.find_element(By.XPATH, login_button_expr)
            except NoSuchElementException as e:
                with error_counter_lock:
                    error_counter.value += 1
                logging.error("Error: the 'Log in' button not found with error: \n %s \nState: Password inputbox detected \nPage: The password page", str(e))
                try:
                    driver.quit()
                except:
                    pass
                return None
            if login_button:
                try:
                    login_button.click()
                except Exception as e:
                    with error_counter_lock:
                        error_counter.value += 1
                    logging.error("Error: Cannot click the login button \n%s \nState: Password entered \nPage: The password page", str(e))
        else:
            with error_counter_lock:
                error_counter.value += 1
            logging.error("Error: Password inputbox not found. \nState: Unknown. \nPage: Unknown")
            try:
                driver.quit()
            except:
                pass
            return None
        time.sleep(10)
        
        ''' Extra Checks '''
        # If email is inspected
        xpath_expr_3 = (
        "//span[text()='检查你的邮箱'] | "
        "//span[text()='Confirm your email address'] | "
        "//span[text()='Check your email'] | "
        "//span[contains(text(),'a confirmation code')]"
        )
        retry = 0
        max_retry = 0
        extra_checks = None
        while retry <= max_retry:
            try:
                extra_checks = driver.find_element(By.XPATH, xpath_expr_3)
                break
            except NoSuchElementException:
                retry += 1
                time.sleep(3)
        if extra_checks:
            try:
                verified_code_field = driver.find_element(By.NAME, 'text')
            except NoSuchElementException as e:
                logging.error("Error: The verified code inputbox not found with error: \n %s \nState: Extra checks detected \nPage: The extra checks page", str(e))
                try:
                    driver.quit()
                except:
                    pass
                return None
            if verified_code_field:
                verified_code = get_mail_verified(email, email_password)
                if verified_code is None:
                    set_availability_account(sql_connector, email)
                    logging.error("Error: The verified code from eamil not fetched  \nState: Extra checks inputbox detected \nPage: The extra checks page \nEmail: %s \nEmail Password: %s", email, email_password)
                    logging.info("Info: The status of X account: %s  has been set unvailable.", email)
                    try:
                        driver.quit()
                    except:
                        pass
                    return None
                else:
                    verified_code_field.send_keys(verified_code)
                    try:
                        next_button = driver.find_element(By.XPATH, next_expr)
                    except NoSuchElementException as e:
                        with error_counter_lock:
                            error_counter.value += 1
                        logging.error("Info: The 'Next' button not found \n \nState: Password proceeded \nPage: The extra checks page", str(e))
                        pass
                    if next_button:
                        next_button.click()
        else:
            logging.info("Info: The extra checks not found \nState: The password page proceeded \nPage: Unknown")
        time.sleep(5)


        ''' 2FA Authentication '''
        xpath_expr_4 = (
        "//span[contains(text(), 'Enter your verification code')] | "
        "//span[text()='Use your code generator app to generate a code and enter it below.']"
        )
        retry = 0
        max_retry = 1
        twofa_authentication = None
        while retry <= max_retry:
            try:
                twofa_authentication= driver.find_element(By.XPATH, xpath_expr_4)
                break
            except NoSuchElementException:
                retry += 1
                time.sleep(3)
        if twofa_authentication and two_fa_link:
            logging.info("Info: The 2FA authentication is found \nState: 2FA Authenication  \nPage: 2FA authentication page ")
            twofa_code = get_2fa_code(two_fa_link)
            if twofa_code:
                logging.info("Info: The 2FA code is found Code: %s \nState: 2FA Page Proceeded \nPage: 2FA authentication page", twofa_code)
                twofa_code_field = None
                try:
                    twofa_code_field = driver.find_element(By.NAME, 'text')
                except NoSuchElementException as e:
                    with error_counter_lock:
                        error_counter.value += 1
                    logging.error("Error: The 2FA code inputbox not found with error: \n %s \nState: 2FA authentication is found \nPage: 2FA Authentication page", str(e))
                    try:
                        driver.quit()
                    except:
                        pass
                    return None
                if twofa_code_field:
                    twofa_code_field.send_keys(twofa_code)
                    next_button = None
                    try:
                        next_button = driver.find_element(By.XPATH, next_expr)
                    except NoSuchElementException as e:
                        logging.error("Info: The 'Next' button not found with error: \n %s \nState: 2FA authentication inputbox detected \nPage: 2FA Authentication page", str(e))
                        try:
                            driver.quit()
                        except:
                            pass
                        return None
                    if next_button:
                        try:
                            next_button.click()
                        except Exception as e:
                            with error_counter_lock:
                                error_counter.value += 1
                            logging.error("Error: Cannot click the 'Next' button \n%s \nState:")
            else:
                logging.error("Error: Cannot get the 2FA code \nState: 2FA Authentication is found \nPage: 2FA authentication page")
                with error_counter_lock:
                    error_counter.value += 1
                try:
                    driver.quit()
                except:
                    pass
                return None
        elif twofa_authentication and two_fa_link is None:
            logging.error("Error: 2FA Authentication founded but no two fa link provided \nState: 2FA Authentication found \nPage:2FA authentication page")
            try:
                driver.quit()
            except:
                pass
            return None
        else:
            logging.info("Info: No 2FA Authentication detected \nState: Password proceeded \nPage: Unknown")
        time.sleep(5)

        ''' Authentication '''
        # If Authentication is needed, try next account
        authentication_expr = (
        "//span[contains(text(),'Authenticate your account')]"
        )
        retry = 0
        max_retry = 0
        authentication = None
        while retry <= max_retry:
            try:
                authentication = driver.find_element(By.XPATH, authentication_expr)
                break
            except NoSuchElementException:
                retry += 1
                time.sleep(5)
            if authentication:
                with error_counter_lock:
                    error_counter.value += 1
                set_availability_account(email)
                logging.error("Error: Authentication is found \nState: The password page proceeded \nPage: Unknown \nEmail: %s; Username: %s", email, username)
                logging.info("Info: The status of X account: %s  has been set unvailable.", email)
                try:
                    driver.quit()
                except:
                    pass
                return None
            else:
                logging.info("Info: No authentication detected \nState: successful logged in \nPage: X Home Page")
    except TimeoutException:
        with error_counter_lock:
            error_counter.value += 1
        logging.info("Info: Time out for loading pages \nState: Unknown \nPage: Unknown")
        try:
            driver.quit()
        except:
            pass
        return None
    time.sleep(5)
    return driver