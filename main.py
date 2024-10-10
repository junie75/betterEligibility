import requests
from getAccess import getToken
from hipaaTransactions import getCoverages, getPayerList
import json


#token expires every 5 minutes, function to check if token is expired and get a new token if it is
# def isTokenExpired():

def get_valid_payers(sessionToken):
    # Call the getPayerList function with the session token and other parameters
    response = getPayerList(sessionToken, transactionType="270", submissionMode="API") # gets the list of payers that support the 270 transaction and API submission 

    # check for errors in the response and save the payer list to a file
    if response.startswith('Error'):
        print(response)
    else:
        try:
            with open('payersEligibilityAPI.json', 'w') as file:
                file.write(response)
            print('Payer list saved to file')
        except IOError as e:
            print(f'Error saving payer list to file: {str(e)}')
    # response = getPayerList(sessionToken, payload)

if __name__ == '__main__':
    # Get the access token
    sessionToken = getToken()

    # Get the list of payers that support the 270 transaction and API submission
    # get_valid_payers(sessionToken)

    # Call the getCoverages function with the session token and other required parameters
    response = getCoverages(sessionToken, "00001", "123456789", "Doe", "John", "1970-01-01")
    print(response)