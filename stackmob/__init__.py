#import oauth.oauth as oauth
import oauth.oauth as oauth
import httplib
import json
import sys

SM_URL = "api.stackmob.com"
SM_CONNECTION = None
SM_CONSUMER = None

def init(key, secret):
    global SM_URL, SM_CONNECTION, SM_CONSUMER
    SM_CONNECTION = httplib.HTTPConnection(SM_URL)
    SM_CONSUMER = oauth.OAuthConsumer(key, secret)
        
def _execute(httpmethod, path, body):
    global SM_URL, SM_CONNECTION, SM_CONSUMER

    request = oauth.OAuthRequest.from_consumer_and_token(SM_CONSUMER, http_method=httpmethod, http_url="http://" + SM_URL + "/" + path)
    request.sign_request(oauth.OAuthSignatureMethod_HMAC_SHA1(), SM_CONSUMER, None)
    headers = request.to_header()
    headers["Content-Type"] = "application/json"
    headers["Accept"] = "application/vnd.stackmob+json; version=0"
    # SM_CONNECTION.set_debuglevel(1)
    bodyString = ""
    if(body != None):
        bodyString = json.dumps(body)
    
    SM_CONNECTION.request(request.http_method, "/"+path, body=bodyString, headers=headers)
    return SM_CONNECTION.getresponse()

def get(path):
        return _execute("GET", path, None)