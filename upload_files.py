import requests
import json
import os.path
import csv
import datetime
today = datetime.date.today()
from dateutil import relativedelta
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
import sys
import glob
import os
remote_path = '/Billing/Non_Taylor/'
remote_gateway_path = '/Billing/Gateway_list/'

## Use this only for Azure AD multi-factor authentication
from msrestazure.azure_active_directory import AADTokenCredentials

## Required for Azure Data Lake Store filesystem management
from azure.datalake.store import core, lib, multithread

# Common Azure imports
import adal
from azure.mgmt.resource.resources import ResourceManagementClient
from azure.mgmt.resource.resources.models import ResourceGroup

## Use these as needed for your application
import logging, getpass, pprint, uuid, time

## Declare variables
adlsAccountName = 'phciotiqanconnect'
authority_host_url = "https://login.microsoftonline.com"
tenant = "parkercorp.onmicrosoft.com"
authority_url = authority_host_url + '/' + tenant
client_id = '7d960b27-c1a5-4424-93bf-e4565df8ac39'
redirect = 'urn:ietf:wg:oauth:2.0:oob'
RESOURCE = 'https://management.core.windows.net/'

authority_host_uri = 'https://login.microsoftonline.com'
tenant = 'parkercorp.onmicrosoft.com'
authority_uri = authority_host_uri + '/' + tenant
resource_uri = 'https://management.core.windows.net/'
client_id = '7d960b27-c1a5-4424-93bf-e4565df8ac39'
client_secret = 'SKzEkkDO0uCs08A1MLIovNKFCKclR7f5xn86/+jU1zQ='


context = adal.AuthenticationContext(authority_uri, api_version=None)
mgmt_token = context.acquire_token_with_client_credentials(resource_uri, client_id, client_secret)
credentials = AADTokenCredentials(mgmt_token, client_id)

token = lib.auth(tenant_id = 'b5da5f35-6442-4f5a-9622-92ec6a535127', client_secret = 'SKzEkkDO0uCs08A1MLIovNKFCKclR7f5xn86/+jU1zQ=', client_id = '7d960b27-c1a5-4424-93bf-e4565df8ac39')
print("The first step is getting the access token from Azure Active Directory\n")
adlsFileSystemClient = core.AzureDLFileSystem(token, store_name=adlsAccountName)


def gateway_list():
    print("Uploading gateway list  to the Azure Data lake")
    todays=today.strftime('%Y-%m-%d')
    updated_remote_gateway_file = remote_gateway_path + todays + '.txt'
    gateway_list_name = 'gateway_needed_info.txt'
    print("Uploading the generated file to the Azure Data Lake....")
    multithread.ADLUploader(adlsFileSystemClient, lpath=gateway_list_name, rpath=updated_remote_gateway_file, nthreads=64, overwrite=True, buffersize=4194304, blocksize=4194304)
    os.remove('config.py')
    os.remove('gateway_needed_info.txt')
    os.remove('gateway_needed_info_old.txt')


def csv_file():
    print("Upload data to the Azure Data lake")
    todays=today.strftime('%Y-%m-%d')
    updated_remote_file = remote_path + todays + '.csv'
    output_name = todays + '.csv'
    print("Uploading the generated file to the Azure Data Lake....")
    multithread.ADLUploader(adlsFileSystemClient, lpath=output_name, rpath=updated_remote_file, nthreads=64, overwrite=True, buffersize=4194304, blocksize=4194304)
    print("All steps completed------------------------------------")
