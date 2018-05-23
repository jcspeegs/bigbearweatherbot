from time import sleep
import bigbearweatherbot
import config

token = config.token

ben = bigbearweatherbot.Bbw(token)


def main():
    confirmed_offset = -1

    while True:

        sleep(0.5)
        updates = ben.get_updates_json(offset=confirmed_offset + 1)
        if len(updates['result']) > 0:
            ud = updates['result'][-1]
            chat_id = ud['message']['chat']['id']
            if 'text' in ud['message'] \
                    and ud['message']['text'].lower().find('/help') == -1:
                if ud['message']['text'].lower().find('/bb') != -1:
                    reply = bigbearweatherbot.scrape_bens()
                    ben.send_msg(chat_id, text=reply, parse='HTML')
                    ben.send_photo(chat_id)
            else:
                reply = "Hello {}, I am the Big Bear Weather Bot.  " \
                        "I can give you the Ben's weather forecast for " \
                        "Big Bear if you ask with: /bb".format(ud['message']['from']['username'])
                ben.send_msg(chat_id, reply)

            confirmed_offset = max(confirmed_offset, ud['update_id'])


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
