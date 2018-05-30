import collections
from urllib import parse

import requests
from bs4 import BeautifulSoup


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

    def send_msg(self, chat_id, text, parse=False, loc=False):
        method = 'sendMessage'
        params = {'chat_id': chat_id, 'text': text}
        if parse:
            params['parse_mode'] = parse
        if loc:
            params['request_location'] = True
        resp = requests.post(self.api_url + method, params)
        
        return resp

    def send_photo(self, chat_id, photo):
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

def scrape_aa( uday= '%25', ucity= '%25', utype= '%25', uzip= '%25'):
    web_url = 'http://oc-aa.org/directory/meetings.asp?day={}&city={}&type={}&zip={}'.format(uday, ucity, utype, uzip)
    r = requests.get(web_url)

    soup = BeautifulSoup(r.text, 'html.parser')
    result_table = soup.find_all('table')[2]

    head = result_table.find('tr')
    header = ' '.join([h.text.replace(' ', '_') for h in head.find_all('th')]).lower()
    meeting = collections.namedtuple('meeting', header)
    print(header)
    meetings = []
    for tr in result_table.find_all('tr')[1:]:
        # print(tr)
        vals = [d.text.strip() for d in tr.find_all('td')]
        meetings.append(meeting._make(vals))

    display = ''
    for m in meetings:
        params = parse.urlencode({'destination': m.address})
        map_url = 'https://www.google.com/maps/dir/?api=1&{}'\
            .format(params)
        display += '{:>8} {:<40} {:>10}\n'\
            .format(m.time, '<a href={}>{}</a>'.format(map_url, m.meeting_name), m.day)

    print(display)
    return display

scrape_aa(uzip=92646)