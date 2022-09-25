from eth_utils import address
from web3 import Web3
import os
from solcx import compile_standard, install_solc
import json


with open("SolveMe.sol", "r") as file:
    contact_list_file = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SolveMe.sol": {"content": contact_list_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"] # output needed to interact with and deploy contract
                }
            }
        },
    },
    solc_version="0.8.0",
)
print(compiled_sol)
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)


bytecode = compiled_sol["contracts"]["SolveMe.sol"]["SolveMe"]["evm"]["bytecode"]["object"]
# get abi
abi = json.loads(compiled_sol["contracts"]["SolveMe.sol"]["SolveMe"]["metadata"])["output"]["abi"]


w3 = Web3(Web3.HTTPProvider("https://blockchain-solveme-06abe249835cc81d-eth.2022.ductf.dev:443"))
chain_id = 31337
address = "0x36628cDA83bf62b00A843fF1963E219ed65b3F79"
private_key = "0xb3ea4d0f5e3552c25a5e8cd890431f40ade7f99a93f61265fd87db0bd9d71afc" # leaving the private key like this is very insecure if you are working on real world project
# Create the contract in Python
ContactList = w3.eth.contract(abi=abi, bytecode=bytecode)
## Get the number of latest transaction
nonce = w3.eth.getTransactionCount(address)
#
transaction = ContactList.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": address,
        "nonce": nonce,
    }
)
# Sign the transaction
sign_transaction = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print("Deploying Contract!")
# Send the transaction
transaction_hash = w3.eth.send_raw_transaction(sign_transaction.rawTransaction)
# Wait for the transaction to be mined, and get the transaction receipt
print("Waiting for transaction to finish...")
transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
print(f"Done! Contract deployed to {transaction_receipt.contractAddress}")

contact_list = w3.eth.contract(address="0x8dc207890bCFF0AdaD18ca50FdAb19d222DB2C7B", abi=abi)
store_contact = contact_list.functions.solveChallenge(
).buildTransaction({"chainId": chain_id, "from": address, "gasPrice": w3.eth.gas_price, "nonce": nonce + 1})

# Sign the transaction
sign_store_contact = w3.eth.account.sign_transaction(
    store_contact, private_key=private_key
)
# Send the transaction
send_store_contact = w3.eth.send_raw_transaction(sign_store_contact.rawTransaction)
transaction_receipt = w3.eth.wait_for_transaction_receipt(send_store_contact)

print(contact_list.functions.solveChallenge().call())
