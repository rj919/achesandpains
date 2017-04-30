__author__ = 'rcj1492'
__created__ = '2017.04'
__license__ = 'MIT'

text_2_speech = 'https://stream.watsonplatform.net/text-to-speech/api'

def bluemix_token(bluemix_username, bluemix_password):

    import requests
    from labpack.handlers.requests import handle_requests

# construct request
    request_kwargs = {
        'url': 'https://stream.watsonplatform.net/authorization/api/v1/token',
        'params': {
            'url': 'https://stream.watsonplatform.net/speech-to-text/api'
        },
        'auth': (bluemix_username, bluemix_password)
    }

# send request
    try:
        response = requests.get(**request_kwargs)
    except:
        request_kwargs['method'] = 'GET'
        request_object = requests.Request(**request_kwargs)
        return handle_requests(request_object)

# construct default response details
    details = {
        'method': response.request.method,
        'code': response.status_code,
        'url': response.url,
        'error': '',
        'json': None,
        'headers': response.headers
    }

# handle different codes
    if details['code'] == 200:
        details['json'] = { 'token': response.text }
    else:
        details['error'] = response.content.decode()

    return details

def bluemix_speech2text(byte_data, file_name, auth_token):

    import requests
    from labpack.handlers.requests import handle_requests

    request_kwargs = {
        'url': 'https://stream.watsonplatform.net/speech-to-text/api/v1/recognize',
        'headers': {
            'Content-Type': 'audio/ogg;codecs=opus',
            'X-Watson-Authorization-Token': auth_token,
            'X-Watson-Learning-Opt-Out': 'true'
        },
        'files': {
            'file': (file_name, byte_data)
        }
    }

# send request
    try:
        response = requests.post(**request_kwargs)
    except:
        request_kwargs['method'] = 'POST'
        request_object = requests.Request(**request_kwargs)
        return handle_requests(request_object)

# construct default response details
    details = {
        'method': response.request.method,
        'code': response.status_code,
        'url': response.url,
        'error': '',
        'json': None,
        'headers': response.headers
    }

# handle different codes
    if details['code'] == 200:
        details['json'] = response.json()
    else:
        details['error'] = response.content.decode()

    return details

if __name__ == '__main__':

    from labpack.records.settings import load_settings
    bluemix_config = load_settings('../cred/bluemix.yaml')
    username = bluemix_config['bluemix_speech2text_username']
    password = bluemix_config['bluemix_speech2text_password']

    token_details = bluemix_token(username, password)
    auth_token = token_details['json']['token']

    file_name = 'watson_test'
    file_path = '../data/%s.ogg' % file_name
    file_data = open(file_path, 'rb')
    transcribed_text = bluemix_speech2text(file_data, file_path, auth_token)
    print(transcribed_text)
