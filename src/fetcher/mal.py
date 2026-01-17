import requests

def get_mal_list(access_token:str):
    url = "https://api.myanimelist.net/v2/users/@me/animelist"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url=url, headers=headers)
    response.raise_for_status()
    return response.json()


