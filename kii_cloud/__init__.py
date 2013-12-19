# -*- coding: utf-8 -*-
# vim:set sts=4 sw=4 tw=0 et:

import httplib2
import json

APP_ID = None
APP_KEY = None
BASE_URL = None
TOKEN = None

def init(app_id, app_key, region):
    global APP_ID, APP_KEY, BASE_URL
    APP_ID = app_id
    APP_KEY = app_key
    if region == u'jp':
        BASE_URL = u'https://api-jp.kii.com/api'
    else:
        BASE_URL = u'https://api.kii.com/api'

def delete_bucket(bucket_name):
    global APP_ID, APP_KEY, BASE_URL

    if not _has_token(u'kii_migrator', u'12345678'):
        return False

    uri_array = [BASE_URL, u'apps', APP_ID, u'buckets', bucket_name]
    uri = u'/'.join(uri_array)
    headers = {
            u'Authorization': u'Bearer ' + TOKEN,
            u'x-kii-appid': APP_ID,
            u'x-kii-appkey': APP_KEY,
            }
    (resp, content) = json_request(uri, 'DELETE', None, headers)
    return resp.status == 204

def json_request(uri, method, data, headers):
    h = httplib2.Http()
    if data != None:
        data = json.dumps(data).encode('UTF-8')
    (resp_headers, resp_body) = h.request(uri, method, data, headers)
    try:
        resp_json = json.loads(resp_body) if resp_body != None else None
        return (resp_headers, resp_json)
    except ValueError:
        return (resp_headers, {})

def create_user(data):
    global APP_ID, APP_KEY, BASE_URL
    uri_array = [BASE_URL, u'apps', APP_ID, u'users']
    uri = u'/'.join(uri_array)
    headers = {
            u'content-type': u'application/vnd.kii.RegistrationRequest+json',
            u'x-kii-appid': APP_ID,
            u'x-kii-appkey': APP_KEY,
            }
    (resp, content) = json_request(uri, 'POST', data, headers)
    return (resp.status == 201 or resp.status == 409)

def _has_token(username, password):
    global TOKEN
    if TOKEN:
        return True
    elif not create_user({ u'loginName': username, u'password': password }):
        return False
    uri = u'/'.join([BASE_URL, u'oauth2', u'token'])
    data = {
            u'username': username,
            u'password': password
            }
    headers = {
            'content-type': 'application/json',
            'x-kii-appid': APP_ID,
            'x-kii-appkey': APP_KEY,
            }
    (resp, resp_json) = json_request(uri, 'POST', data, headers)
    if resp.status != 200:
        return False
    if resp_json['access_token'] == None:
        return False
    else:
        TOKEN = str(resp_json['access_token'])
        return True

def create_object(bucket, data, obj_id=None):
    if not _has_token(u'kii_migrator', u'12345678'):
        return False
    uri_array = [BASE_URL, u'apps', APP_ID, u'buckets', bucket, u'objects']
    if obj_id:
        uri_array.append(obj_id)
    uri = u'/'.join(uri_array)
    headers = {
            'Authorization': u'Bearer ' + TOKEN,
            'content-type': 'application/json',
            'x-kii-appid': APP_ID,
            'x-kii-appkey': APP_KEY,
            }
    (resp, resp_json) = json_request(uri, 'PUT', data, headers)
    return (resp.status == 201 or resp.status == 200)