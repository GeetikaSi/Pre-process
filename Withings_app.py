from flask import Flask, request, redirect
import requests
from requests_oauthlib import OAuth2Session
from flask.json import jsonify
import json
import urllib.parse as urlparse
from urllib.parse import parse_qs


app = Flask(__name__)


client_id = "Client ID"
customer_secret = "Customer secret"
STATE = "a_random_value"
ACCOUNT_URL = "https://account.withings.com/oauth2_user/authorize2"
WBSAPI_URL = "https://wbsapi.withings.net"
CALLBACK_URI = "Callback URI"

# Handles manual user authorization.
@app.route("/", methods=['GET'])
def auth_user():
    user = {"response_type": "code",
            "client_id": client_id,
            "state": STATE,
            "scope": "user.info,user.metrics,user.activity",
            "redirect_uri": CALLBACK_URI,
            }
    r = requests.get('https://account.withings.com/oauth2_user/authorize2',
                     params=user)
    return redirect(r.url)

access_token = ""

# Handles auth request made by Withings to pass down user code.
@app.route("/callback_uri")
def callback_uri():
    global access_token
    # handle callback from withings.
    user_code = request.args.get('code')
    print("user code: ", user_code)
    access_token = get_access_token(user_code)
    
    return "Testing withings here :)"


# Helper function to fetch the access token from 'user_code'.
def get_access_token(user_code):
    print("user_code: ", user_code)
    user_auth = {'action': 'requesttoken',
                 'grant_type': "authorization_code",
                 'client_id': client_id,
                 'client_secret':customer_secret,
                 'code': user_code,
                 'redirect_uri': CALLBACK_URI
                 }
    r_token = requests.post('https://account.withings.com/oauth2/token', data=user_auth).json()

    access_token = r_token.get('access_token', '')
    print("access token: ", access_token)
    return access_token

# Handler to fetch user data.
@app.route("/get_data")
def fetch_data():
    startdate= request.args.get("startdate")
    enddate = request.args.get("enddate")
    if access_token == "":
        print("Access token empty")
    # GET Some info with this token
    headers = {'Authorization': 'Bearer ' + access_token}
    payload = {'action': 'getdevice'}

    # List devices of returned user
    r_getdevice = requests.get(f'{WBSAPI_URL}/v2/user',
                               headers=headers,
                               params=payload).json()

    # Measurements of returned user
    meas_type = [1,4,11]
    headers_meas = {'Authorization': 'Bearer ' + access_token}
    payload_meas = {'action': 'getmeas',
                    'meas_types': meas_type,
                    'startdate': startdate,
                    'enddate': enddate}

    r_getmeas = requests.get(f'{WBSAPI_URL}/measure',
                               headers=headers_meas,
                               params=payload_meas).json()

    headers_act = {'Authorization': 'Bearer ' + access_token}
    payload_act = {'action': 'getactivity',
                   'startdateymd': startdate,
                   'enddateymd': enddate,
                   'data_fields': ['steps']}

    # Activity of returned user
    r_getact = requests.get(f'{WBSAPI_URL}/v2/measure',
                             headers=headers_act,
                             params=payload_act).json()
    print(r_getdevice)
    print(r_getmeas)
    print(r_getact)
    
    final_dict = {'device':r_getdevice, 'measure':r_getmeas, 'activity':r_getact}
    with open('data.json','w') as outfile:
        json.dump(final_dict, outfile)

    return final_dict


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)
