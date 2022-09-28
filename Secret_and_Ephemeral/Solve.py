from web3 import Web3
import json
from Secret_and_Ephemeral.Util import init_challenge, get_flag
from web3.middleware import geth_poa_middleware
from web3.contract import Contract
from Compile import compile_sol


# Contract owner is 0x7BCF8A237e5d8900445C148FC2b119670807575b

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

contract = w3.eth.contract(contract_addr, abi=abi)


for i in range(10):
    transaction = w3.eth.getBlock(i)["transactions"]
    if transaction:
        for j in range(len(transaction)):
            input_field = w3.eth.get_transaction(f"{transaction[j].hex()}")['input']
            print(contract.decode_function_input(input_field))


#print(w3.eth.getStorageAt(contract_addr,1))
