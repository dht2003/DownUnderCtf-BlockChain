import requests


def init_challenge(url):
    r = requests.get(url)
    details = r.json()
    player_addr = details["player_wallet"]["address"]
    player_key = details["player_wallet"]["private_key"]
    contract_address = details["contract_address"][0]["address"]
    print("Got All the addresses for the challenge")
    return player_addr, player_key, contract_address


def get_flag(url):
    r = requests.get(url)
    flag = r.json()["flag"]
    print(flag)
