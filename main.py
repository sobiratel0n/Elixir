import random
import time
from copy import copy
import questionary
from questionary import Choice
from config import WALLETS, SLEEP_MAX, SLEEP_MIN
from elixir import Elixir
from loguru import logger as ll
from okx import OKX

if __name__  == "__main__":

    task = questionary.select(
        "Peak task you need tyo solve",
        choices=[
            Choice("Withdraw from Elixir", 'elixir'),
            Choice("Deposit to OKX", "okx"),
        ],
        pointer="👉 "
    ).ask()

    if task == "elixir":
        wallet_id = 0
        wallets = copy(WALLETS)
        while wallets:
            count = len(wallets) - 1
            r = random.randint(0, count)
            wallet = wallets.pop(r)
            wallet_id = WALLETS.index(wallet) + 1
            account = Elixir(account_id=wallet_id, pk=wallet)
            status = account.elixir()
            if status == True:
                sleep = random.randint(SLEEP_MIN, SLEEP_MAX)
                ll.info(f"Sleep [{sleep} sec]")
                time.sleep(sleep)
            else:
                time.sleep(1)
        ll.success(f"All {len(WALLETS)} Wallets have withdrawn their funds from Elixir ")

    elif task == "okx":
        wallet_id = 0
        wallets = copy(WALLETS)
        while wallets:
            count = len(wallets) - 1
            r = random.randint(0, count)
            wallet = wallets.pop(r)
            wallet_id = WALLETS.index(wallet) + 1
            account = OKX(account_id=wallet_id, pk=wallet)
            status = account.act()
            if status:
                sleep = random.randint(300, 1200)
                time.sleep(sleep)
            else:
                time.sleep(1)
