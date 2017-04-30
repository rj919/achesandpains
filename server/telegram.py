__author__ = 'rcj1492'
__created__ = '2017.04'
__license__ = 'MIT'

def analyze_message(update_details, user_id, telegram_bot_client):

    from os import environ
    from server.feedback import get_kitten
    from labpack.storage.appdata import appdataClient
    telegram_data_client = appdataClient('Telegram', prod_name='achesBot')
    user_key = 'users/telegram_%s.yaml' % user_id
    user_record = telegram_data_client.read(user_key)

# parse message
    message_string = ''
    if 'voice' in update_details['message'].keys():
        voice_id = update_details['message']['voice']['file_id']
        details = telegram_bot_client.get_route(voice_id)
        file_route = details['json']['result']['file_path']
        file_buffer = telegram_bot_client.get_file(file_route, file_name='voice_telegram_%s' % user_id)
        file_data = file_buffer.getvalue()
        file_name = file_buffer.name

        from server.bluemix import bluemix_speech2text, bluemix_token
        bluemix_username = environ['bluemix_speech2text_username'.upper()]
        bluemix_password = environ['bluemix_speech2text_password'.upper()]
        token_details = bluemix_token(bluemix_username, bluemix_password)
        if token_details['json']:
            auth_token = token_details['json']['token']
            speech_details = bluemix_speech2text(file_data, file_name, auth_token)
            if speech_details['json']:
                if 'results' in speech_details['json'].keys():
                    transcript_results = speech_details['json']['results']
                    if transcript_results:
                        alternative_list = transcript_results[0]['alternatives']
                        sorted_results = sorted(alternative_list, key=lambda k: k['confidence'])
                        message_string = sorted_results[0]['transcript']

    elif 'text' in update_details['message'].keys():
        if update_details['message']['text']:
            message_string = update_details['message']['text']

# define default response
    print(message_string)
    response_details = {
        'function': 'send_message',
        'kwargs': {
            'user_id': user_id,
            'message_text': 'Thanks. Your symptoms have been recorded.'
        }
    }

# handle navigation
    if message_string.lower() in ('start', '/start', 'help', '/help', 'about', '/about'):
        response_details['kwargs']['message_text'] = 'Aches & Pains bot is your personal health journal. To create an entry, simply type or speak into the app about how you feel. Your entry will be logged, coded and added to your medical records. \n\nYou can also type the following commands:\n\t__/help__ : for this message\n\t__/feedback__ : for selection of feedback options\n\t__/history__ : for last three entries'
        response_details['kwargs']['message_style'] = 'markdown'

# update feedback types
    elif message_string.lower() == 'kittens':
        user_details = { 'feedback_type': 'kittens' }
        telegram_data_client.create(user_key, user_details, overwrite=True)
        response_details['kwargs']['message_text'] = 'Sweet! Your feedback type has been updated to cute kittens.'
    elif message_string.lower() == 'text':
        user_details = {'feedback_type': 'text'}
        telegram_data_client.create(user_key, user_details, overwrite=True)
        response_details['kwargs']['message_text'] = 'Sweet! Your feedback type has been updated to normal text.'
    elif message_string.lower() in ('feedback', '/feedback'):
        response_details['kwargs']['message_text'] = 'Select a type of feedback:'
        response_details['kwargs']['button_list'] = [ 'Text', 'Kittens' ]

# retrieve history
    elif message_string.lower() in ('history', '/history'):
        from server.nlp.nlp_engine import nlp_engine, engine
        # Check to see that database file is written if needed
        # assert os.path.isfile(nlp.database_file)
        n1 = nlp_engine()
        report_string = n1.extract('janedoe')
        import re
        entry_pattern = re.compile('\n\s\s\s\sSun,.*')
        entry_search = entry_pattern.findall(report_string)
        message_text = 'Your last three entries:\n'
        for i in [ -3, -2, -1 ]:
            message_text += '\n%s' % entry_search[i]
        response_details['kwargs']['message_text'] = message_text
    elif message_string == '.':
        response_details['function'] = 'pass'

# add entry to record
    else:
        if not message_string and 'voice' in update_details['message'].keys():
            response_details['kwargs']['message_text'] = 'Transcription failed. Can you type that out instead?'
        else:
            from server.nlp.nlp_engine import nlp_engine, engine
            # Check to see that database file is written if needed
            # assert os.path.isfile(nlp.database_file)
            n1 = nlp_engine()
            token_list = []
            sentences_list = message_string.split('.')
            for sentence in sentences_list:
                word_list = sentence.split(' ')
                token_list.append(word_list)
            # n1.slurp("janedoe", [["My", "leg", "hurts"], ["I", "took", "an", "aspirin"]])
            n1.slurp('janedoe', token_list)
            if user_record['feedback_type'] == 'kittens':
                api_key = environ['CATAPI_API_KEY']
                kitten_details = get_kitten(api_key)
                if kitten_details['json']:
                    if 'src' in kitten_details['json'].keys():
                        response_details = {
                            'function': 'send_photo',
                            'kwargs': {
                                'user_id': user_id,
                                'photo_url': kitten_details['json']['src']
                            }
                        }
            print(n1.extract('janedoe'))

    return response_details

def monitor_telegram(telegram_config):

    from time import time
    from labpack.storage.appdata import appdataClient
    telegram_data_client = appdataClient('Telegram', prod_name='achesBot')
    from labpack.messaging.telegram import telegramBotClient
    init_kwargs = {
        'access_token': telegram_config['telegram_access_token'],
        'bot_id': telegram_config['telegram_bot_id']
    }
    admin_id = 'telegram_%s' % telegram_config['telegram_admin_id']
    telegram_bot_client = telegramBotClient(**init_kwargs)
    update_key = 'last-update.yaml'
    update_record = telegram_data_client.read(update_key)
    last_update = update_record['last_update']
    updates_details = telegram_bot_client.get_updates(last_update)
    update_list = []
    if updates_details['json']['result']:
        update_list = sorted(updates_details['json']['result'], key=lambda k: k['update_id'])
        offset_details = { 'last_update': update_list[-1]['update_id']}
        telegram_data_client.create(update_key, offset_details)
    for update in update_list:
        user_id = update['message']['from']['id']
        contact_id = 'telegram_%s' % user_id
        record_key = 'incoming/%s/%s.json' % (contact_id, str(time()))
        telegram_data_client.create(record_key, update)

    # analyze message
        response_details = analyze_message(update, user_id, telegram_bot_client)
        if response_details['function'] == 'send_message':
            telegram_bot_client.send_message(**response_details['kwargs'])
        elif response_details['function'] == 'send_photo':
            telegram_bot_client.send_photo(**response_details['kwargs'])

    # save response
        record_key = 'outgoing/%s/%s.json' % (contact_id, str(time()))
        telegram_data_client.create(record_key, response_details)

    return True

if __name__ == '__main__':
    from labpack.records.settings import load_settings
    telegram_config = load_settings('../cred/telegram.yaml')
    monitor_telegram(telegram_config)
