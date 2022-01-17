import os


class Config():
    ENV_AWS_DEFAULT_REGION = 'AWS_DEFAULT_REGION'
    ENV_NGROK_BASE_AGENT_URL = 'NGROK_BASE_AGENT_URL'
    ENV_SSM_PREFIX = 'SSM_PREFIX'

    defaults = {
        ENV_AWS_DEFAULT_REGION: 'us-east-2',
        ENV_NGROK_BASE_AGENT_URL: 'http://localhost:4040/api',
        ENV_SSM_PREFIX: '/ngrok_domains',
    }

    def __init__(self):
        self.cache = {
            self.ENV_AWS_DEFAULT_REGION: os.environ.get(self.ENV_AWS_DEFAULT_REGION),
            self.ENV_NGROK_BASE_AGENT_URL: os.environ.get(self.ENV_NGROK_BASE_AGENT_URL),
            self.ENV_SSM_PREFIX:  os.environ.get(self.ENV_SSM_PREFIX)
        }
        for key, value in self.cache.items():
            if (value == None or value == '') and key in self.defaults:
                self.cache[key] = self.defaults[key]

        if self.cache[self.ENV_SSM_PREFIX].endswith('/'):
            self.cache[self.ENV_SSM_PREFIX] = self.cache[self.ENV_SSM_PREFIX][:-1]

    def get(self, keyName):
        if not keyName in self.cache:
            return None
        return self.cache[keyName]
