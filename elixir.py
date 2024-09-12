import web3.exceptions
from web3 import Web3
from eth_account import Account as EthereumAccount
from config import ABI, GAS
from loguru import logger as ll
import time

class Elixir():
    def __init__(self, account_id, pk):
        self.account_id = account_id
        self.pk = pk
        self.w3 = self.w3 = Web3(Web3.HTTPProvider("https://ethereum-rpc.publicnode.com"))
        self.account = EthereumAccount.from_key(self.pk)
        self.contract_address = self.w3.to_checksum_address("0x4265f5D6c0cF127d733EeFA16D66d0df4b650D53")
        self.contract = self.w3.eth.contract(abi=ABI, address=self.contract_address)
        self.address = self.account.address
        self.balance = 0


    def wait_tx_finished(self, hash, max_wait_time = 180):
        start_time = time.time()
        while True:
            try:
                receipts = self.w3.eth.get_transaction_receipt(hash)
                status = receipts.get("status")
                if status == 1:
                    ll.success(f'[Wallet {self.account_id}] withdraw {self.w3.from_wei(self.balance, "ether")} ETH tx https://etherscan.io/tx/0x{hash}')
                    return True
                elif status is None:
                    time.sleep(0.5)
                else:
                    ll.error(f'[Wallet {self.account_id}] Transaction failed ---> https://etherscan.io/tx/{hash}')
                    return False
            except web3.exceptions.TransactionNotFound:
                if time.time() - start_time > max_wait_time:
                    ll.error(f'[Wallet {self.account_id}] Transaction failed ---> https://etherscan.io/tx{hash}')
                    return False
                else:
                    time.sleep(1)

    def check_balance_on_elixir(self):
        balance = self.contract.functions.unusedBalance(self.address).call()
        ll.info(f'[Wallet {self.account_id}] staked in Elixir {self.w3.from_wei(balance, "ether")} ETH')
        return balance

    def wait_gas(self):
        gas_price = self.w3.eth.gas_price
        gas = self.w3.to_wei(GAS, "gwei")
        while gas_price >= gas:
            ll.warning(f"Current gas {self.w3.from_wei(gas_price,'gwei')} GWEI | wait for {GAS} GWEI")
            time.sleep(20)
            gas_price = self.w3.eth.gas_price
        ll.info(f"[Wallet {self.account_id}] gas is good {self.w3.from_wei(gas_price,'gwei')} GWEI")

    def withdraw_balance(self):
        function_call = self.contract.functions.withdrawEth(self.balance)
        gas = int(function_call.estimate_gas({
            "from": self.address,
            "value": 0
        }) * 1.15)
        txn = {
                'from': self.w3.to_checksum_address(self.address),
                'value': 0,
                'gas': gas,
                'gasPrice': self.w3.eth.gas_price + self.w3.to_wei(0.1, "gwei"),
                'nonce': self.w3.eth.get_transaction_count(account=self.address),
            }
        txn = function_call.build_transaction(txn)
        signed_txn = self.w3.eth.account.sign_transaction(txn, self.pk)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        status = self.wait_tx_finished(tx_hash.hex())
        return status
    def elixir(self):
        self.balance = self.check_balance_on_elixir()
        if self.w3.from_wei(self.balance, "ether") > 0.0005:
            self.wait_gas()
            status = self.withdraw_balance()
            if status:
                return status
            else:
                return "skip"
        else:
            ll.error(f"[Wallet {self.account_id}] doesn't have staked ETH in Elixir")
            return "skip"


