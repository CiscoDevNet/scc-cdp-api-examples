#!/usr/bin/env python

import urllib.parse
import urllib.request
import json
import os
from pprint import pprint

# Authentication and API Requests

# This sample script demonstrates logging into the Smart+Connected Digital Platform and making an additional request
# Except for authentication, all Smart+Connected Digital Platform API requests require two access tokens that must be
#   passed in request headers.
# The main ideas in this sample are:
#   1) Logging in
#   2) Parsing the login response to get tokens needed for further API calls
#   3) Using the tokens to make another API request

# Base Smart+Connected Digital Platform API URL for all other requests
if 'SCC_BASE_URL' in os.environ:
    print('SCC_BASE_URL is set to {}'.format(os.environ['SCC_BASE_URL']))
else:
    print('SCC_BASE_URL has not been set.')
    exit()

baseUrl = os.environ['SCC_BASE_URL']

# Smart+Connected Digital Platform API URL for Login
loginUrl = baseUrl + '/login'

# specify default values so you don't have to type them in every time
# @Note: these are not valid, so you need to replace them with your actual username and password
if 'SCC_USER' in os.environ:
    print('SCC_USER is set to {}'.format(os.environ['SCC_USER']))
else:
    print('SCC_USER has not been set.')
    exit()

defaultUser = os.environ['SCC_USER']

if 'SCC_PASS' in os.environ:
    print('SCC_PASS is set to {}'.format('*****'))
else:
    print('SCC_PASS has not been set.')
    exit()

defaultPass = os.environ['SCC_PASS']

if 'SCC_CLIENT_ID' in os.environ:
    print('SCC_CLIENT_ID is set to {}'.format(os.environ['SCC_CLIENT_ID']))
else:
    print('SCC_CLIENT_ID has not been set.')
    exit()

client_id = os.environ['SCC_CLIENT_ID']

if 'SCC_CLIENT_SECRET' in os.environ:
    print('SCC_CLIENT_SECRET is set to {}'.format(os.environ['SCC_CLIENT_SECRET']))
else:
    print('SCC_CLIENT_SECRET has not been set.')
    exit()

client_secret = os.environ['SCC_CLIENT_SECRET']


# this dictionary contains the post body we will send to the /login API
# @Note: these are the DevNet sandbox client_id and client_secret values, so you will
#   need to replace them with yours if you are using another instance of the Smart+Connected Digital Platform
postData = {'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'client_credentials',
            'username': defaultUser,
            'password': defaultPass
            }

print('\nPost Data \n')
pprint(postData)

# urlencode the data
data = urllib.parse.urlencode(postData)

# use UTF-8 encoding for POST data and responses
encoding = 'UTF-8'

# POST needs binary data, so encode it
binary_data = data.encode(encoding)

print('\nLogging in \n(' + loginUrl + ')\n')
# urlopen with data causes a post request
request = urllib.request.Request(loginUrl, binary_data)
response = urllib.request.urlopen(request)

# process the results and put into a JSON object/dictionary
results = response.read().decode(encoding)
responseDictionary = json.loads(results)

print('responseDictionary')
print(responseDictionary)

# get the auth tokens from the response - these are needed in all future Smart+Connected Digital Platform API Requests
requestHeaders = {
    'WSO2-Authorization': 'oAuth Bearer ' + responseDictionary['app_access_token'],
    'Authorization': 'Bearer ' + responseDictionary['api_access_token'],
    'Accept': 'application/json'
}

print('requestHeaders')
print(requestHeaders)

# get user info for the logged in user
# <CDP-BaseURL>/accounts?loginName=user123@cdp.com

# username resource requires one queryparam: the username for which you are retrieving information
queryParams = urllib.parse.urlencode({'loginName': defaultUser})

requestUrl = baseUrl + '/accounts?%s' % queryParams

print('\nGetting **USER** Information (' + requestUrl + ')\n')

# create the request
request = urllib.request.Request(requestUrl)

# add headers (for API authorization)
for k, v in requestHeaders.items():
    request.add_header(k, v)

print('requestHeaders:\n')
pprint(requestHeaders)

print('request:\n')
pprint(request)

print('Performing the request...')

# perform the request
response = urllib.request.urlopen(request)

results = response.read().decode(encoding)
responseDictionary = json.loads(results)

print('results')
print(results)
