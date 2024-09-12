import random

from config import LEAVE_MIN_BALANCE, LEAVE_MAX_BALANCE, WITHDRAW_FROM, OKX_WALLETS
from loguru import logger as ll
from elixir import Elixir
import web3
import time
class OKX(Elixir):
    def __init__(self, account_id, pk):
        super().__init__(account_id=account_id, pk=pk)
        self.leave_balance = random.randint(self.w3.to_wei(LEAVE_MIN_BALANCE, "ether"), self.w3.to_wei(LEAVE_MAX_BALANCE, "ether"))
        self.balance = 0

    def check_wallet_balance(self):
        self.balance = self.w3.from_wei(self.w3.eth.get_balance(self.address), "ether")
        if self.balance < WITHDRAW_FROM:
            return False
        else:
            r = random.randint(3, 6)
            self.balance = self.w3.to_wei(self.balance, "ether") - self.leave_balance
            self.balance = self.w3.to_wei(round(self.w3.from_wei(self.balance, 'ether'), r), 'ether')
            return True

    def wait_tx_finished_okx(self, hash, max_wait_time = 180):
        start_time = time.time()
        while True:
            try:
                receipts = self.w3.eth.get_transaction_receipt(hash)
                status = receipts.get("status")
                if status == 1:
                    ll.success(f'[Wallet {self.account_id}] tx https://etherscan.io/tx/0x{hash}')
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

    def deposit_to_okx(self):
        okx = OKX_WALLETS.get(self.address)
        tx = {
            "chainId": 1,
            'from': self.w3.to_checksum_address(self.address),
            "to": self.w3.to_checksum_address(okx),
            'value': self.balance,
            'gas': 0,
            'gasPrice': self.w3.eth.gas_price + self.w3.to_wei(0.1, "gwei"),
            'nonce': self.w3.eth.get_transaction_count(self.address)
        }
        tx['gas'] = self.w3.eth.estimate_gas(tx)
        ll.info(f"[Wallet {self.account_id}] deposit to OKX {self.w3.from_wei(self.balance, 'ether')} ETH")
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.pk)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        status = self.wait_tx_finished_okx(tx_hash.hex())
        return status

    def act(self):
        status = self.check_wallet_balance()
        if status:
            status = self.deposit_to_okx()
            return True
        else:
            ll.error(f"[Wallet {self.account_id}] you have less ETH than {self.w3.from_wei(self.leave_balance, 'ether')}")



