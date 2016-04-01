import time
import log
import requests
import json

log = log.log('log.txt', 'DEBUG')

CLIENT_ID = '0ff6b819-6eb1-4881-918a-11b7485224d1'
SECRET_KEY = '0hjDS3PRMqC2yiFHKGvd2PBgzmChxklO6NxZz0vHYIw='
REDIRECT_URI = 'https://login.live.com/oauth20_desktop.srf'
AUTH_ENDPOINT = 'https://login.microsoftonline.com/common'
TOKEN_ENDPOINT = 'https://login.microsoftonline.com/common/oauth2/token'
RESOURCE_URI = 'https://analysis.windows.net/powerbi/api'
API_ROOT = 'https://api.powerbi.com/v1.0/myorg/'

seed_token = ''
refresh_token = 'AAABAAAAiL9Kn2Z27UubvWFPbm0gLQe2AeyczBgGHq66SNxZs_UdVcJadWH1yyOESslkN67k9ww7Qdyt0ivK5PGLHHY4f4w717jGqOCDscZI-AMCyLG9MIRic6KIJeA2LjVhTZ_m5VdC3CGUBJ9FKLoDbyDxepK5Nmfwqs0rFFB4LHThWVvyGvjkjmbrXQ8haDMpeQSSkp6TC0H9h_gzpswTHgjd29ofEzyF6j7CLh3gx-3kHCzaqpPH9uCAI8n0bRc3Dj-2QEmqkqYb2yp4fX7gz159k62n5ocdQsRyRpLCuldcd_kBLy7zOnxTKQfk6FmFukALdkdmjewdk_eD7iacVn4yyo0c6PTHP-9gJvSiFU7AFq66Yc5yhFuvp5QfRd5ATQmi6gxD4cUg2G01vizUPAdRQrfPBrbyGZUi2MUsKF3ud3hxLTMLYzBXPHaDetgprEQRcgvOWNGTsueJOd0Iw08DbrdSN8GHWQ3R_d7a5Pue1lhrNk6kgNdHPNc8hIrcRh-fDyzlLuR9bWjJ65ahbU5qcE-a3iO5Zx3mOqfJ_xbeXHNYd91cvRyb2Fi3a_nhjzGi5QnNhykR2s7C5HixaCxtM5tMJ15VN70rdORgbxqkLqBy-6_boYzGvr5Oyr8Y1VBvlhrqS8PuAosyHMwYDhb2krfBLeYdCd8GCwO_MFjlbwMczsArxNsmao7EWMKH7QRmhrQW8mrzhWPnxk_BClBLEHkiD6KBYhca93-FpTsDvFmUB4_9YNimx0NoOKIeyC9fw0nYIet4E_LdioK-Tm1Fmaus1O9FKf4BWz2Fg7Y-V3LAsVBFpxom-oD5Q2crfVKMFR2dBdJncWwmNvVNDUp-08g4uGi5JmVlQIy9k5UL_uxOnAidLH8y0WpMykFj7mCsgvfvNMfhtupW6QtlG87uUr10V7lA3bQXZfaa3iksTD8534Q6XvGsbtalv3UV64P3IAA'

class PBI:
    def __init__(self, seed, refresh):
        self.token = seed
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
        if self.expires - time.time() < 60:
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
        log.info('%s - %s' %(r, r.json()))
        return r.json()
        
        
    def get(self, suburl):
        return self.call(requests.get, suburl)
        
    def post(self, suburl, body, headers={}):
        return self.call(requests.post, suburl, body=body, headers=headers)

        
ds = '''{
  "name": "Test2",
  "tables": 
  [
    {
      "name": "Test2a", "columns": 
        [
          { "name": "StatusDate", "dataType": "DateTime"},
          { "name": "OpenCount", "dataType": "Int64"},
          { "name": "CloseCount", "dataType": "Int64"},
          { "name": "CSAT", "dataType": "Int64"}
        ]
     }
   ]
}'''

#ds = json.loads(ds)
        
pbi = PBI(seed_token, refresh_token)
print pbi.get('groups')
print pbi.get('datasets')
print pbi.post('datasets', ds, headers={'Content-Type':'application/json'})
print pbi.get('datasets')