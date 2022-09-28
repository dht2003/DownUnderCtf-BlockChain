from eth_utils import address
from web3 import Web3
import json
from SolveMe.Util import init_challenge
from Compile import compile_sol

DETAILS_URL = "https://blockchain-solveme-06abe249835cc81d.2022.ductf.dev/challenge"
ENDPOINT_URL = "https://blockchain-solveme-06abe249835cc81d-eth.2022.ductf.dev/"
CHAIN_ID = 31337

SCRIPT_PATH = "SolveMe.sol"

compiled_sol = compile_sol(SCRIPT_PATH)

bytecode = compiled_sol["contracts"]["SolveMe.sol"]["SolveMe"]["evm"]["bytecode"]["object"]
# get abi
abi = json.loads(compiled_sol["contracts"]["SolveMe.sol"]["SolveMe"]["metadata"])["output"]["abi"]

w3 = Web3(Web3.HTTPProvider(ENDPOINT_URL))
player_address, private_key, contract_addr = init_challenge(DETAILS_URL)

nonce = w3.eth.getTransactionCount(player_address)
contact_list = w3.eth.contract(address=contract_addr, abi=abi)
store_contact = contact_list.functions.solveChallenge(
).buildTransaction({"chainId": CHAIN_ID, "from": player_address, "gasPrice": w3.eth.gas_price, "nonce": nonce})

# Sign the transaction
sign_store_contact = w3.eth.account.sign_transaction(
    store_contact, private_key=private_key
)
# Send the transaction
send_store_contact = w3.eth.send_raw_transaction(sign_store_contact.rawTransaction)
transaction_receipt = w3.eth.wait_for_transaction_receipt(send_store_contact)

print(contact_list.functions.solveChallenge().call())
