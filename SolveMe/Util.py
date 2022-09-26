import requests
import json
from solcx import compile_standard
import os


def init_challenge(url):
    r = requests.get(url)
    details = r.json()
    player_addr = details["player_wallet"]["address"]
    player_key = details["player_wallet"]["private_key"]
    contract_addr = details["contract_address"][0]["address"]
    return player_addr, player_key, contract_addr


def compile_sol(script_path):
    script_name = os.path.basename(script_path)
    with open(script_path, "r") as file:
        contact_list_file = file.read()

    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {script_name: {"content": contact_list_file}},
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                    }
                }
            },
        },
        solc_version="0.8.0",
    )
    with open("compiled_code.json", "w") as file:
        json.dump(compiled_sol, file)
    return compiled_sol

