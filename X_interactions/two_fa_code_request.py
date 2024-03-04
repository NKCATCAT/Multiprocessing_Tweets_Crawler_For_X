import requests
import json
import re
def get_2fa_code(two_fa_link):
    two_fa = two_fa_link.replace('henduohao.com/2fa/', '')
    url = 'https://www.henduohao.com/tools/twofaGet'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': '_ga=GA1.1.1785124203.1706003806; PHPSESSID=tb5rsp5b8sj2ibdfa5tvv05cvf; _ga_DV9JNDK8NY=GS1.1.1706211482.7.1.1706211678.60.0.0',
        'Origin': 'https://www.henduohao.com',
        'Referer': 'https://www.henduohao.com/2fa/'+two_fa,
        'Sec-Ch-Ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Linux"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    data = {
        'twoFaCode': two_fa
    }

    response = requests.post(url, headers=headers, data = data)
    response_text = str(response.text)
    response_text = re.sub(r'[^\x20-\x7E]+', '', response_text)
    response_data = json.loads(response_text)
    if response_data["code"] == 0:
        two_fa_code = response_data["data"]
        return two_fa_code
    else:
        return None