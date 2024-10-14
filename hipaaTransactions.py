# Description: This script retrieves HIPAA transactions from the Availity API using the access token retrieved from the getAccess.py script
# Author: Juni Ejere
# Date: 2024-10-09
# Version: 1.0
# ***IMPORTANT***: Availity no longer supports GET/v1/coverages endpoint & has replaced it with POST/v1/coverages endpoint

import requests
from dotenv import load_dotenv
import os
import json

# Function to get patient coverage information supporting ASC X12N 270 & 271 transactions; ****Note**** This function is designed for the coverages endpoint of the Availity API version 1.0.0
def getCoverages(sessionToken, payerID, memberID, lastName, firstName, birthDate):
    # Set the URL for the API endpoint
    url = "https://api.availity.com/availity/development-partner/v1/coverages"

    load_dotenv()  # Make sure to call this function to load the variables

    # Set the payload data for the POST request
    payload = {
        "payerId": "MOCK_PAYER_ID",                  # The payer's unique ID
        "providerLastName": os.getenv('PROVIDER_LAST_NAME'),   # Provider's last name
        "providerFirstName": os.getenv("PROVIDER_FIRST_NAME"),  # Provider's first name
        "providerNpi": os.getenv("PROVIDER_NPI"),               # Provider's NPI number
        "providerTaxId": os.getenv("PROVIDER_TAX_ID"),           # Provider's Tax ID
        "memberId": "MOCK_MEMBER_ID",             # Patient's insurance member ID
        "patientLastName": "DOE",      # Patient's last name
        "patientFirstName": "JOHN",    # Patient's first name
        "patientBirthDate": "1970-01-01",            # Patient's birthdate in format (YYYY-MM-DD)
        "serviceType": 30,               # Type of service (e.g., 30 for medical)
        # "procedureCode": "PROCEDURE_CODE"            # CPT or HCPCS procedure code
    }

    # ********TESTING************ dummy data 
    data = {
    "payerId": "123",
    "providerUserId": "123",
    "providerNpi": "123",
    "providerLastName": "ABC",
    "asOfDate": "1990-01-01",
    "serviceType[]": "30",
    "memberId": "ABC123",
    "patientBirthDate": "1900-01-01",
    "patientLastName": "LAST",
    "patientFirstName": "FIRST",
    "patientGender": "M",
    "patientState": "FL",
    "subscriberRelationship": "18",
    "requestedPatientSearchOption": "memberId,patientBirthDate,patientState"
}

    # Set the headers, including your OAuth token
    headers = {
        "Authorization": f"Bearer {sessionToken}", # Replace with your actual OAuth token
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json", 
        "X-Api-Mock-Scenario-ID": "200" # This header is used for interacting with the DEMO version of the Availity API
    }

    # Make the POST request to the Availity API
    # response = requests.post(url, data=payload, headers=headers)

    # ********TESTING************
    response = requests.post(url, data=data, headers=headers)

    # Check if the response contains valid JSON
    if response.status_code == 200:
        try:
            # Parse the response JSON
            response_json = response.json()

            # Pretty-print the JSON response
            pretty_response = json.dumps(response_json, indent=4)

            # Return the pretty-printed response
            return pretty_response

        except json.JSONDecodeError:
            # If the response is not valid JSON, return the raw text
            return f"Error: Unable to decode JSON response.\n {response.text}"
    else:
        return f"Error: HTTP Status Code {response.status_code}.\n{response.text}"

    # Output the response text
    # return(response.text)

# Retrieve a customized list of Availity payers and transactions. This function is designed for the payers endpoint of the Availity API version 1.0.4
def getPayerList(sessionToken, **kwargs):
    # Set the URL for the API endpoint
    url = "https://api.availity.com/availity/development-partner/v1/availity-payer-list"

    # Set the headers, including your OAuth token
    headers = {
        "Authorization": f"Bearer {sessionToken}", # Replace with your actual OAuth token
        # "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }

    # Set the payload data for the GET request (if any)
    payload = kwargs

    # Make the GET request to the Availity API
    response = requests.get(url, headers=headers, params=payload)

    # Check if the response contains valid JSON
    if response.status_code == 200:
        try:
            # Parse the response JSON
            response_json = response.json()

            # Pretty-print the JSON response
            pretty_response = json.dumps(response_json, indent=4)

            # Return the pretty-printed response
            return pretty_response

        except json.JSONDecodeError:
            # If the response is not valid JSON, return the raw text
            return f"Error: Unable to decode JSON response.\n {response.text}"
    else:
        return f"Error: HTTP Status Code {response.status_code}.\n{response.text}"

    # Output the response text
    # return(response.text)