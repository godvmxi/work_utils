#coding=gbk
import httplib
header = {'oauth_nonce': '80155333', 'oauth_timestamp': 1382509888, 'oauth_consumer_key': '2a72a9cd6e870ed5d28ea00335908230', 'oauth_signature_method': 'PLAINTEXT', 'oauth_version': '1.0', 'oauth_signature': '4d6f9cafdfb3910a5d5bd96090cfd852%20&', 'oauth_callback': 'http://sandbox.note.youdao.com/oauth'}
conn = httplib.HTTPConnection("sandbox.note.youdao.com")
conn.request('get', '/oauth/oauth/request_token',str ( header ))
print conn.getresponse().read()
conn.close()