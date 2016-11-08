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

# print(results)

# LEARNING LAB 2 CODE BEGINS HERE
# CDP102 - Retrieving Addional Information from CDP

# Prerequisites: CDP101

# we need to get the customerid and userid from the response, these are needed to get data from CDP
customerId = None
userId = None

if 'id' in responseDict:
  userId = str(responseDict['id'])
  print("Retrieved User ID:" + userId)

if 'parentInfo' in responseDict:
  parentInfo = responseDict['parentInfo']
  if 'id' in parentInfo:
    customerId = str(parentInfo['id'])
    print("Retrieved Customer ID:" + customerId)

# get locations that this user has access to
# <CDP-BaseURL>/locations/userinfo/user/<user_id>

# make sure we have the userId
if userId:
  requestUrl = baseUrl + "/locations/userinfo/user/" + userId
  print("\nGetting **LOCATION** Information (" + requestUrl + ")\n");
  request = urllib.request.Request(requestUrl)
  # add headers (for API authorization)
  for k, v in requestHeaders.items():
    request.add_header(k, v)

  # perform the request
  response = urllib.request.urlopen(request)
  results = response.read().decode(encoding)

  # create a dictionary from the results
  responseDict = json.loads(results)

  print(results)
else:
  print("error retrieving user information. 'userId' was not present")

# get the capabilities of this CDP instance
# <CDP-BaseURL>/capabilities/customer/<customer_id>

# make sure we have the customerId
if customerId:
  requestUrl = baseUrl + "/capabilities/customer/" + customerId
  print("\nGetting **CAPABILITIES** Information (" + requestUrl + ")\n");
  request = urllib.request.Request(requestUrl)
  # add headers (for API authorization)
  for k, v in requestHeaders.items():
    request.add_header(k, v)

  # perform the request
  response = urllib.request.urlopen(request)
  results = response.read().decode(encoding)

  # create a dictionary from the results
  responseDict = json.loads(results)

  print(results)
else:
  print("error retrieving user information. 'customerId' was not present")


# LEARNING LAB 3 CODE BEGINS HERE
# CDP103 - Retrieving Real Time Device Data From CDP

# Prerequisites: CDP101, CDP102

# build the request URL and add the customerId and userId query params

# real time device data requests require two query params: UserKey and SensorCustomerKey
queryParams =  urllib.parse.urlencode({'UserKey': userId, 'SensorCustomerKey' : customerId, 'AppKey' : 'CDP-App'})

requestUrl = baseUrl + "/devices/lighting?%s" % queryParams;

# create the TQL POST Body
postData = {"Query":
  {"Find":
    {"Light":
      {"sid":
        {"ne":""}
      }
    }
  }
}

# urlencode the data
data = urllib.parse.urlencode(postData)

# use UTF-8 encoding for POST data and responses
encoding = 'UTF-8'

# POST needs binary data, so encode it
binary_data = data.encode(encoding)

# urlopen with data causes a POST request instead of a GET

request = urllib.request.Request(requestUrl, binary_data)

print("\nRequesting **Real Time Data** (" + requestUrl + ")\n");

# add headers (for API authorization)
for k, v in requestHeaders.items():
  request.add_header(k, v)

# perform the request
response = urllib.request.urlopen(request)
results = response.read().decode(encoding)

# create a dictionary from the results
responseDict = json.loads(results)

# print(results)
# draw pie chart instead

import matplotlib.pyplot as plt

# specify some colors
colors = ['yellowgreen', 'lightcoral']
# create the labes
labels = ['On', 'Off']
values = [0, 0]

if 'Find' in responseDict:
  findObject = responseDict['Find'];
  if 'Result' in findObject:
    results = findObject['Result']

    for r in results:
      if 'Light' in r:
        light = r['Light']

        # we now have an instance of a CDP light model

        # get the 'state' object
        # this contains 'intensityLevel', 'powerConsumption' and 'reliability'
        if light['state']:
          state = light['state']

          # increment the values array
          if state['intensityLevel'] > 0:
            # light is on
            values[0] = values[0] + 1
          else:
            # light is off
            values[1] = values[1] + 1

plt.pie(values, labels=labels,
      autopct='%1.1f%%', shadow=True)

# make the graph a circle (not setting this can result an an elipsis)
plt.axis('equal')

# set the title of the plot and add some additional information - the total number of lights
plt.title('Current Lighting States (Total Lights '+ str(values[0] + values[1]) + ')')

# show the graph
plt.show()
