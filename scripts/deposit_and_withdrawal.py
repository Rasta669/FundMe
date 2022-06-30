from brownie import FundMe
from scripts.helpful_scripts import get_account


def deposit():
    fund_me = FundMe[-1]
    minFee = fund_me.getEntranceFee()
    print(f"The min entry fee is {minFee}")
    print("funding...")
    account = get_account()
    fund_me.fund({"from": account, "value": minFee})


def withdraw():
    fund_me = FundMe[-1]
    account = get_account()
    print("Withdrawing...")
    fund_me.withdraw({"from": account})


def main():
    deposit()
    withdraw()
