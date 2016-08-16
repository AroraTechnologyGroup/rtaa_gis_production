import requests
from requests_oauthlib import OAuth2, OAuth2Session

# my constants
CONSTANTS = {
    'CLIENT_ID': '5d33386c-50a1-4584-8437-ef27004a3093',
    'CLIENT_KEY': 'zZXdY4KLpQRY7F2WpG6KeagttzV5VSn3SxAiF84EcUA=',
    'OAUTH2_TOKEN_ENDPOINT': 'https://login.microsoftonline.com/1b626f6f-0703-43f4-a7a6-7668239c6091/oauth2/token',
    'OAUTH2_AUTH_ENDPOINT': 'https://login.microsoftonline.com/1b626f6f-0703-43f4-a7a6-7668239c6091/oauth2/authorize',
    'REDIRECT_URI': 'https://gisapps.aroraengineers.com.com:8004',
    'RESOURCE_URI': 'https://management.core.windows.net/',
    'GET_SUBSCRIPTIONS_URL': 'https://management.core.windows.net/subscriptions',
    'MS_API_VERSION_HEADER': 'x-ms-version',
    'MS_API_VERSION_HEADER_VALUE': '2013-08-01',
    'SIGN_IN_TEMPLATE': 'aad/index.html'
}


class oauth_code:
    def __init__(self):
        self.url = ''
        self.status_code = ''
        self.history = ''
        self.authorization_response = ''
        self.client_id = CONSTANTS['CLIENT_ID']
        self.client_key = CONSTANTS['CLIENT_KEY']
        self.authorization_base_url = CONSTANTS['OAUTH2_AUTH_ENDPOINT']
        self.token_url = CONSTANTS['OAUTH2_TOKEN_ENDPOINT']
        self.get_subscriptions_url = CONSTANTS['GET_SUBSCRIPTIONS_URL']
        self.x_ms_version = CONSTANTS['MS_API_VERSION_HEADER_VALUE']
        self.redirect_uri = CONSTANTS['REDIRECT_URI']

        self.azure_session = OAuth2Session(self.client_id, redirect_uri=self.redirect_uri,
                                           scope=[self.get_subscriptions_url])

    def do_common(self):
        # get the authorization url from the base url + creds
        authorization_url, state = self.azure_session.authorization_url(self.authorization_base_url)
        resp = requests.get(authorization_url)

        self.authorization_response = resp.url
        self.status_code = resp.status_code
        self.history = resp.history

    def get_subscriptions(self, token):
        header_dict = {'Authorization': 'Bearer ' + token}
        return requests.request('GET', self.get_subscriptions_url, headers=header_dict)

    def fetch_token(self, aad_code, auth_resp):
        print ('call fetch_token')
        token_dict = self.azure_session.fetch_token(self.token_url, client_secret=self.client_key, code=aad_code,
                                                    authorization_response=auth_resp)
        print ('finished fetch_token')
        print (token_dict)
        return token_dict
