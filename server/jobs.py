__author__ = 'rcj1492'
__created__ = '2017.04'
__license__ = '©2017 Collective Acuity'

# add configs to namespace
from labpack.records.settings import load_settings
telegram_config = load_settings('../cred/telegram.yaml')
catapi_config = load_settings('../cred/catapi.yaml')
bluemix_config = load_settings('../cred/bluemix.yaml')

from time import time

job_list = [
    {
        'id': 'telegram.monitor.%s' % str(time()),
        'function': 'telegram:monitor_telegram',
        'kwargs': { 'telegram_config': telegram_config },
        'interval': 2
    },
    {
        'id': 'monitors.running.%s' % str(time()),
        'function': 'init:app.logger.debug',
        'kwargs': { 'msg': 'Monitors are running...' },
        'interval': 60 * 2
    },
    {
        'id': 'monitors.started.%s' % str(time()),
        'function': 'init:app.logger.debug',
        'kwargs': { 'msg': 'Monitors are started.' }
    }
]