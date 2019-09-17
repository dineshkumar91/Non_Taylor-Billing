remote_config = '/Billing/config.py'
local_config = 'config.py'

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
adlsFileSystemClient = core.AzureDLFileSystem(token, store_name=adlsAccountName)


print("Downloading config file from Azure Data Lake")
multithread.ADLDownloader(adlsFileSystemClient, lpath=local_config, rpath=remote_config, nthreads=64, overwrite=True, buffersize=4194304, blocksize=4194304)
print("Download completed\n")
    

import auth_token
import org_gateway_info
import previous_day
import generate_file
import upload_files

if __name__ == "__main__":  
    token = auth_token.authorization_token()
    org_gateway_info.get_org_children(token)
    org_gateway_info.clean()
    previous_day.download()
    generate_file.csv_output()
    upload_files.gateway_list()
    upload_files.csv_file()
    print("12")
