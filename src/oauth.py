import requests
import os
from dotenv import load_dotenv
from pkce import generate_code_challenge, generate_code_verifier
from urllib.parse import urlencode

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")



def get_authorization_url(client_id, redirect_uri, state, code_challenge):
    url = "https://myanimelist.net/v1/oauth2/authorize"
    params = {
        "response_type":"code",
        "client_id":client_id,
        "redirect_uri":redirect_uri,
        "state":state,
        "code_challenge":code_challenge,
        "code_challenge_method":"plain" 
    }
    return f"{url}?{urlencode(params)}"



from requests.auth import HTTPBasicAuth


def exchange_code_for_tokens(client_id, client_secret, auth_code, redirect_uri, code_verifier):
    token_url="https://myanimelist.net/v1/oauth2/token"
    data = {
        "client_id":client_id,
        "grant_type":"authorization_code",
        "code":auth_code,
        "redirect_uri":redirect_uri,
        "code_verifier":code_verifier
    }
    print(redirect_uri)
    response = requests.post(token_url, data=data, auth=HTTPBasicAuth(client_id, client_secret))
    return response.json()


def refresh_access_token(client_id, client_secret, refresh_token):
    token_url = "https://myanimelist.net/v1/oauth2/token"
    data = {
        "grant_type":"refresh_token",
        "refresh_token":refresh_token
    }

    response = requests.post(token_url, data=data, auth=HTTPBasicAuth(client_id, client_secret))
    return response.json()



redirect_uri = "http://localhost:8000/callback"
state = "random_string_to_prevent_csrf"

code_verifier = os.getenv("CODE_VERIFIER")
code_challenge = os.getenv("CODE_CHALLENGE")


# res = get_authorization_url(client_id, redirect_uri, state, code_challenge)
# print("click here :   ", res)



code = "def50200fc55106bee3149177fdb2b617d7ae58a18762fe528e2f0add29d7f341ee2cbea0e3a96659d778dcc74d18cfc86e6d0a925b08d0efc68a3f16ac5aa401add6951075d85bd4adc10e8d633776a4c722e7a441743cdd968c64161336ad6a1a9f03f31a6b013e41161bb15dc13452e7578256c8865db250bbeb20d20453927cccc63f564360b40e2ccf616379298afbbf6954ba36bdd08b3cb0dddde707a320d8998087f4c2eb773e30d5c9884dfc2844e01a97fa71fc7e194f12e5301db525dce5a45fb01d9f184c2b975af141470cafa49831925fd0792d01f2adb0f5f8a43cca25c6e68c20e4f9e157c363444ab38aeebda65f633733a734bcc542c3e087617432c4c5efb9133b90d480632902926e56c1db7137017d2407691563f4d4bd4b03f3efc27f876532bc81ec575edd619d5027e455a020c68f1d719de6fdfe4a858a407c041e608f0a73bd8195785ba7fbe33d6a0df2678bce4b71e2732f60fcf35e9c32fe160dff11b23b713d5bd34a2601392351d1d5b9e5ab2c0a4d893da6f15703ab6557d0c3e03c2be166b3e735c6fad2589641f7acd59f0c912d96fc755e682be4d88dd0ec7c17ddc137b1abc1367d7"

tokens = exchange_code_for_tokens(client_id=client_id, client_secret=client_secret, auth_code=code, code_verifier=code_verifier, redirect_uri=redirect_uri)
print("IF THIS WORKS", tokens)
