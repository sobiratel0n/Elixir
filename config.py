import json

with open("abi.json", 'r') as file:
    ABI = json.load(file)

with open("wallets.txt", "r") as file:
    WALLETS = [row.strip() for row in file]

with open("okx_wallets.json", "r") as file:
    OKX_WALLETS = json.load(file)

# --->>> Elixir setup <<<---
GAS = 1.1
SLEEP_MAX = 180
SLEEP_MIN = 30

# --->>> OKX setup <<<---
LEAVE_MIN_BALANCE = 0.005 # MIN AMOUNT OF ETH THAT  YOU WANT TO LEAVE ON THE WALLET
LEAVE_MAX_BALANCE = 0.007 # MAX AMOUNT OF ETH THAT  YOU WANT TO LEAVE ON THE WALLET
WITHDRAW_FROM = 0.015 # AMOUNT OF ETH FROM WHICH YOU CAN MAKE A WITHDRAWAL

# --->>> In okx_wallets.json you need to add your okx wallet that connected to evm wallet in format {"evm_wallet": "okx_wallet"} <<<---