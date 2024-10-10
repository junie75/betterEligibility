# Description: This script retrieves an access token from the Availity API using the client_id and client_secret from the .env file, saves the token to a file, and checks if the token has expired before returning it. If the token has expired, a new token is retrieved from the API and saved to the file.
# Author: Juni Ejere
# Date: 2024-10-09
# Version: 1.0
# ***Please Note***: Access token is only valid for 5 minutes. You will need to run this script again to get a new token.

from dotenv import load_dotenv
import os
import requests
from requests.auth import HTTPBasicAuth
import json
import datetime

def getTokenFromAPI():
    # Load environment variables from the .env file
    load_dotenv()  # Make sure to call this function to load the variables

    # Retrieve the client_id and client_secret from environment variables
    client_id =  os.getenv('AVAILITY_CLIENT_ID')
    client_secret =  os.getenv('AVAILITY_CLIENT_SECRET')

    #determine api endpoint and required data
    token_url = 'https://api.availity.com/availity/v1/token'  # correct token endpoint

    # Obtain OAuth token encoding and putting credentials in header
    response = requests.post(token_url, auth=HTTPBasicAuth(client_id, client_secret), data={'grant_type': 'client_credentials', 'scope': 'hipaa'})

    # Check if the response is successful
    if response.status_code == 200:
        token = response.json().get('access_token')
        token_data = response.json()
        # print(f"Access token: {token}")
        # print(f'response: {response.json()}')
    else:
        errorMessage = f"Failed to get access token: {response.status_code}, {response.text}"

    # Return the token or error message
    if token:
        return token_data
    else:
        return errorMessage
    
def fetchSaveNewToken():
    #get new token from api
    token_data = getTokenFromAPI()

    #stamp date and time of token retrieval, add to token_data, save token to file
    token_data['time_retrieved'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('token.json', 'w') as file:
        json.dump(token_data, file)
        
    return token_data
    
def getToken():
    #check if token is in json file
    if os.path.exists('token.json'):
        with open('token.json', 'r') as file:
            token_data = json.load(file)
        
        #check if token has expired
        time_now = datetime.datetime.now()
        time_retrieved = datetime.datetime.strptime(token_data['time_retrieved'], "%Y-%m-%d %H:%M:%S") #convert string to datetime
        time_diff = int((time_now - time_retrieved).total_seconds() / 60) #get difference in minutes

        #if token has not expired (less than 5 minutes old), return access token
        if time_diff < 5:
            print('token from file',token_data,'\n time remaining:',5-time_diff)
            return token_data['access_token']
        
        #if token has expired, get new token from api, save token to file, return access token
        else:
            token_data = fetchSaveNewToken()
            print('token expired, new token from api',token_data)
            return token_data['access_token']
        
    #if token is not in file, get token from api, save token to file, return access token
    else:
        token_data = fetchSaveNewToken()
        print('no saved token found, token from api',token_data)
        return token_data['access_token']

if __name__ == '__main__':
    getToken()


