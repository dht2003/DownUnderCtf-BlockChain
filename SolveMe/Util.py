import requests


def init_challenge(url):
    r = requests.get(url)
    details = r.json()
    player_addr = details["player_wallet"]["address"]
    player_key = details["player_wallet"]["private_key"]
    contract_addr = details["contract_address"][0]["address"]
    return player_addr, player_key, contract_addr


