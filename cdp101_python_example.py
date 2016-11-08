import urllib.parse, urllib.request, json

# CDP URL for Login
loginUrl = 'https://cdp-dmz.cisco.com/apigw/devnettokenapis/login'

# Base CDP URL for all other requests
baseUrl = 'https://cdp-dmz.cisco.com/apigw/devnetapi/cdp/v1'

# specify default values so you don't have to type them in every time
# @Note: these are not valid, so you need to replace them with your actual username and password
defaultUser = 'user123@cdp.com'
defaultPass = 'password'

# this dictionary contains the post body we will send to the /login API
# @Note: these are the DevNet sandbox client_id and client_secret values are not valid, so you will
#   need to replace them with yours if you are using another instance of CDP
postData = {
  'client_id':'a27b18484c3c4e08a7c193e42c639347',
  'client_secret':'b863de8f453c4a05A88126F45B958CF1',
  'grant_type':'client_credentials'}

# get username and password from commandline
#   @Note: this will use the defaults from above if you just press 'enter'
username = input('Enter username (email address): ')
if username == '':
  username = defaultUser

password = input('Enter password: ')
if password == '':
  password = defaultPass

# Add username/password to post data
postData['username'] = username;
postData['password'] = password;

# post data now includes client_secret, client_id, username, password and grant_type

# urlencode the data
data = urllib.parse.urlencode(postData)

# use UTF-8 encoding for POST data and responses
encoding = 'UTF-8'

# POST needs binary data, so encode it
binary_data = data.encode(encoding)

print('Logging in (' + loginUrl + ')\n');
# urlopen with data causes a post request
request = urllib.request.Request(loginUrl, binary_data)
response = urllib.request.urlopen(request)

# process the results and put into a JSON object/dictionary
results = response.read().decode(encoding)
responseDict = json.loads(results)

print(responseDict)

# get the auth tokens from the response - these are needed in all future CDP API Requests
requestHeaders = {
    'WSO2-Authorization' : 'oAuth Bearer ' + responseDict['app_access_token'],
    'Authorization' : 'Bearer ' + responseDict['api_access_token'],
    'Accept': 'application/json'
}

print(requestHeaders)

# get user info for the logged in user
# <CDP-BaseURL>/accounts/username?loginName=user123@cdp.com

# username resource requires one queryparam: the username for which you are retrieving information
queryParams =  urllib.parse.urlencode({'loginName': postData['username']})

requestUrl = baseUrl + '/accounts/username?%s' % queryParams;

print('\nGetting **USER** Information (' + requestUrl + ')\n');

# create the request
request = urllib.request.Request(requestUrl)

# add headers (for API authorization)
for k, v in requestHeaders.items():
  request.add_header(k, v)

# perform the request
response = urllib.request.urlopen(request)

results = response.read().decode(encoding)
responseDict = json.loads(results)

print(results)
