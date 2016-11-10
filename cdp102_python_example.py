import urllib.parse, urllib.request, json

# Retrieving Information from the Smart+Connected Digital Platform

# This sample script demonstrates making several Smart+Connected Digital Platform
# Except for authentication, all Smart+Connected Digital Platform API requests require two access tokens that must be
#   passed in request headers.
# The main ideas in this sample are:
#   1) Logging in
#   2) Parsing the login reponse to get tokens needed for futher API calls
#   3) Using the tokens to make several API requests

# Smart+Connected Digital Platform API URL for Login
loginUrl = 'http://10.10.20.6/apigw/devnetlabtokenapi/login'

# Base Smart+Connected Digital Platform API URL for all other requests
baseUrl = 'http://10.10.20.6/apigw/devnetlabapi/cdp/v1'

# specify default values so you don't have to type them in every time
# @Note: these are not valid, so you need to replace them with your actual username and password
defaultUser = 'user123@cdp.com'
defaultPass = 'password'

# this dictionary contains the post body we will send to the /login API
# @Note: these are the DevNet sandbox client_id and client_secret values, so you will
#   need to replace them with yours if you are using another instance of the Smart+Connected Digital Platform
postData = {
    'client_id':'a27b18484c3c4e08a7c193e42c639347',
    'client_secret':'b863de8f453c4a05A88126F45B958CF1',
    'grant_type':'client_credentials'
}

# get username and password from commandline
#   @Note: this will use the defaults from above if you just press 'enter'
username = input('Enter username (email address): ')
if username == '':
    username = defaultUser

password = input('Enter password: ')
if password == '':
    password = defaultPass

# Add username/password to post data
postData['username'] = username
postData['password'] = password

# post data now includes client_secret, client_id, username, password and grant_type

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
    'WSO2-Authorization' : 'oAuth Bearer ' + responseDictionary['app_access_token'],
    'Authorization' : 'Bearer ' + responseDictionary['api_access_token'],
    'Accept': 'application/json'
}

print('requestHeaders')
print(requestHeaders)

# get user info for the logged in user
# <CDP-BaseURL>/accounts/username?loginName=user123@cdp.com

# username resource requires one queryparam: the username for which you are retrieving information
queryParams =  urllib.parse.urlencode({'loginName': postData['username']})

requestUrl = baseUrl + '/accounts/username?%s' % queryParams

print('\nGetting **USER** Information (' + requestUrl + ')\n')

# create the request
request = urllib.request.Request(requestUrl)

# add headers (for API authorization)
for k, v in requestHeaders.items():
    request.add_header(k, v)

# perform the request
response = urllib.request.urlopen(request)

results = response.read().decode(encoding)
responseDictionary = json.loads(results)

# LEARNING LAB 2 CODE BEGINS HERE
# CDP102 - Retrieving Addional Information from the Smart+Connected Digital Platform API

# Prerequisites: CDP101

# we need to get the customerid and userid from the response, these are needed to get data from the Smart+Connected Digital Platform API
customerId = None
userId = None

if 'id' in responseDictionary:
    userId = str(responseDictionary['id'])
    print("Retrieved User ID:" + userId)

if 'parentInfo' in responseDictionary:
    parentInfo = responseDictionary['parentInfo']
    if 'id' in parentInfo:
        customerId = str(parentInfo['id'])
        print("Retrieved Customer ID:" + customerId)

# get locations that this user has access to
# <CDP-BaseURL>/locations/userinfo/user/<user_id>

# make sure we have the userId
if userId:
    requestUrl = baseUrl + "/locations/userinfo/user/" + userId
    print("\nGetting **LOCATION** Information \n(" + requestUrl + ")\n")
    request = urllib.request.Request(requestUrl)
    # add headers (for API authorization)
    for k, v in requestHeaders.items():
        request.add_header(k, v)

  # perform the request
  response = urllib.request.urlopen(request)
  results = response.read().decode(encoding)

  # create a dictionary from the results
  responseDictionary = json.loads(results)

  print(results)
else:
  print("error retrieving user information. 'userId' was not present")

# get the capabilities of this Smart+Connected Digital Platform instance
# <CDP-BaseURL>/capabilities/customer/<customer_id>

# make sure we have the customerId
if customerId:
    requestUrl = baseUrl + "/capabilities/customer/" + customerId
    print("\nGetting **CAPABILITIES** Information (" + requestUrl + ")\n")
    request = urllib.request.Request(requestUrl)
    # add headers (for API authorization)
    for k, v in requestHeaders.items():
        request.add_header(k, v)

    # perform the request
    response = urllib.request.urlopen(request)
    results = response.read().decode(encoding)

    # create a dictionary from the results
    responseDictionary = json.loads(results)

    print(results)
else:
    print("error retrieving user information. 'customerId' was not present")
