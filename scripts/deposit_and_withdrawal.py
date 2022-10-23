from brownie import FundMe
from scripts.helpful_scripts import get_account
from scripts.deployF import deploy_fundme


def deposit():
    fund_me, account = deploy_fundme()
    minFee = fund_me.getEntranceFee()
    print(f"The min entry fee is {minFee}")
    print("funding...")
    fund_me.fund({"from": account, "value": minFee})


def withdraw():
    fund_me, account = deploy_fundme()
    print("Withdrawing...")
    tx = fund_me.withdraw({"from": account})
    tx.wait(1)


def main():
    deposit()
    withdraw()
