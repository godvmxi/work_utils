#coding=gbk
import httplib
try:
    import json
except ImportError:
    import simplejson as json
import time
import urllib
import urllib2
import logging
#header = {'oauth_nonce': '80155333', 'oauth_timestamp': 1382509888, 'oauth_consumer_key': '2a72a9cd6e870ed5d28ea00335908230', 'oauth_signature_method': 'PLAINTEXT', 'oauth_version': '1.0', 'oauth_signature': '4d6f9cafdfb3910a5d5bd96090cfd852%20&', 'oauth_callback': 'http://sandbox.note.youdao.com/oauth'}
#conn = httplib.HTTPConnection("sandbox.note.youdao.com")
#conn.request('get', '/oauth/oauth/request_token',str ( header ))
#print conn.getresponse().read()
#conn.close()


class APIClient(object):
    '''
    API client using synchronized invocation.
    '''
    def __init__(self, app_key, app_secret, redirect_uri=None, response_type='code', domain='sandbox.note.yaodao.com', version='2'):
        self.client_id = app_key
        self.client_secret = app_secret
        self.redirect_uri = redirect_uri
        self.response_type = response_type

        self.request_token_url = self.auth_url+"request_token"   
        self.authorize_url = self.auth_url+"authorize"   
        self.access_token = self.auth_url+"access_token"
        self.expires = 0.0


    def set_access_token(self, access_token, expires_in):
        self.access_token = str(access_token)
        self.expires = float(expires_in)

    def get_authorize_url(self, redirect_uri=None, display='default'):
        '''
        return the authroize url that should be redirect.
        '''
        redirect = redirect_uri if redirect_uri else self.redirect_uri


    def request_access_token(self, code, redirect_uri=None):
        '''
        return access token as object: {"access_token":"your-access-token","expires_in":12345678}, expires_in is standard unix-epoch-time
        '''
        return True

    def is_expires(self):
        return not self.access_token or time.time() > self.expires

    def __getattr__(self, attr):
        return getattr(self.get, attr)
    def request_token(self):
        pass
    
