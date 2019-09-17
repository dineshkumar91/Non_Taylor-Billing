import datetime
today = datetime.date.today()
from dateutil import relativedelta
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta


y1 = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
remote_path = '/Billing/Non_Taylor/'

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



def download():
    print("Downloading previous day's information from the Azure data lake")
    remote_file = remote_path + y1 + '.csv'
    local_file = y1 + '.csv'
    ## Download a file
    multithread.ADLDownloader(adlsFileSystemClient, lpath=local_file, rpath=remote_file, nthreads=64, overwrite=True, buffersize=4194304, blocksize=4194304)
    print("Download completed\n")

    ##############Previous day's file downloaded########################
