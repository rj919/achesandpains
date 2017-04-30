__author__ = 'rcj1492'
__created__ = '2017.04'
__license__ = 'MIT'

def get_kitten(api_key=''):

    ''' a method to get a random kitten image '''

    # http://thecatapi.com/

# import dependencies
    import re
    import requests
    from labpack.handlers.requests import handle_requests

# construct request
    request_kwargs = {
        'url': 'http://thecatapi.com/api/images/get',
        'params': {
            'format': 'xml'
        }
    }
    if api_key:
        request_kwargs['params']['api_key'] = api_key

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
        xml_text = response.text
        url_pattern = re.compile('<url>(.*?)</url>')
        url_search = url_pattern.findall(xml_text)
        if url_search:
            details['json'] = { 'src': url_search[0] }
    else:
        details['error'] = response.content.decode()

    return details

def get_puppy():


    return True

if __name__ == '__main__':

    print(get_kitten())