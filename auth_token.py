import requests
import config
username_elevat = config.username
password_elevat = config.password


# Step 1: The first step is to login with username and password and get access token

def authorization_token():
    print("\n\nStep 1: Getting the authorization token.................") 
    url = "https://parkerelevat-auth.parker.com/login"
    
   
    payload = {
        'email':username_elevat,
        'password':password_elevat
        }
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache"
        }

    response = requests.request("POST", url, data = payload, headers=headers)

    json_response = response.json()

    access = json_response['token']
    # End of Step 1: Organization token obtained and successfully stored in 'access'

    print("\nAuthorization token obtained") 
    return (access)
