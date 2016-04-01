import time, json
import requests
import log

log = log.log('log.txt', 'DEBUG')

CLIENT_ID = '0ff6b819-6eb1-4881-918a-11b7485224d1'
SECRET_KEY = '0hjDS3PRMqC2yiFHKGvd2PBgzmChxklO6NxZz0vHYIw='
REDIRECT_URI = 'https://login.live.com/oauth20_desktop.srf'
AUTH_ENDPOINT = 'https://login.microsoftonline.com/common'
TOKEN_ENDPOINT = 'https://login.microsoftonline.com/common/oauth2/token'
RESOURCE_URI = 'https://analysis.windows.net/powerbi/api'
API_ROOT = 'https://api.powerbi.com/v1.0/myorg/'

def show(d):
    try:
        print json.dumps(d, sort_keys=True, indent=4)
    except:
        print d
    return 


class PBI:
    def __init__(self, refresh):
        self.token = None
        self.refresh_token = refresh
        self.api_root = API_ROOT
        self.token_endpoint = TOKEN_ENDPOINT
        self.client_id = CLIENT_ID
        self.secret = SECRET_KEY
        self.resource = RESOURCE_URI
        self.redirect = REDIRECT_URI
        self.expires = time.time()
        self.do_refresh_token()
    
    def do_refresh_token(self):
        log.info('Refreshing token...')
        body = {
            'grant_type' : 'refresh_token',
            'client_id': self.client_id,
            'resource' : self.resource,
            'redirect_uri' : self.redirect,
            'refresh_token' : self.refresh_token
        }
        r = requests.post(self.token_endpoint, data=body)
        j = r.json()
        log.debug(j)
        self.token = j['access_token']
        self.expires = int(j['expires_on'])
        log.info('Token refreshed')
        return
        
    def check_token(self):
        if self.token is None or self.expires - time.time() < 60:
            self.do_refresh_token()
        else:
            log.debug('Token still valid, reusing...')
        auth = {'Authorization' : 'Bearer %s' %self.token}
        return auth
        
    def call(self, method, suburl, body={}, headers={}):
        auth = self.check_token()
        headers.update(auth)
        url = '%s/%s' %(self.api_root, suburl)
        r = method(url, headers=headers, data=body)
        log.debug(url)
        log.debug(r)
        try:
            log.info('%s - %s' %(r, r.json()))
            return r.json()
        except:
            return r
        
        
    def get(self, suburl):
        return self.call(requests.get, suburl)
        
    def post(self, suburl, body, headers={'Content-Type':'application/json'}):
        return self.call(requests.post, suburl, body=body, headers=headers)

        
