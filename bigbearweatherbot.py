import requests
from bs4 import BeautifulSoup
from time import time


class Bbw:

    def __init__(self, token):
        self.token = token
        self.api_url = 'https://api.telegram.org/bot{}/'.format(token)

    def get_updates_json(self, offset: int = None, timeout: int = 60) -> object:
        """Get updates after <offset> in last <timeout> seconds"""

        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp_json = requests.get(self.api_url + method, params).json()
        return resp_json

    def send_msg(self, chat_id, text, parse=False):
        method = 'sendMessage'
        params = {'chat_id': chat_id, 'text': text}
        if parse:
            params['parse_mode'] = parse
        resp = requests.post(self.api_url + method, params)
        return resp

    def send_photo(self, chat_id,
                   photo='https://media-mammothresorts-com.s3-us-west-2.amazonaws.com/bbmr/snowsummit/cams/summitktla.jpg?={}'
                   .format(time())):
        method = 'sendPhoto'
        params = {'chat_id': chat_id, 'photo': photo}
        resp = requests.post(self.api_url + method, params)
        return resp


def scrape_bens(web_url='http://bensweather.com'):
    def extract(styleno):
        return soup.find(class_='style{}'.format(styleno)).text.strip()

    r = requests.get(web_url)
    soup = BeautifulSoup(r.text, 'html.parser')

    timestamp = soup.find(class_='style108').find_next('u').text.strip()

    condition = '{}: {} {} {}'.format(extract(205), extract(45), extract(43), extract(211))

    long_report = extract(209)

    weather_report = '<b>{}</b>\n\n{}\n\n{}\n\n{}' \
        .format(timestamp, condition, long_report, web_url)

    # print(weather_report)
    return weather_report
