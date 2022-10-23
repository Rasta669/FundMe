from brownie import network, accounts, exceptions
from scripts.deployF import deploy_fundme
from scripts.helpful_scripts import get_account, LOCAL_DEVELOPMENT_NETWORKS
import pytest


def test_can_deposit_and_withdraw():
    if network.show_active() not in LOCAL_DEVELOPMENT_NETWORKS:
        pytest.skip("Only for local testing")
    (fund_me, account) = deploy_fundme()
    entry_fee = fund_me.getEntranceFee()
    tx = fund_me.fund({"from": account, "value": entry_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account) == entry_fee
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.balanceOfTheContract() == 0


##Using pytest to demonstrate how to skip a certain test aimed only for local testing
##also using pytest to pass a certain test when an exception or error is raised as expected.
def test_only_owner():
    if network.show_active() not in LOCAL_DEVELOPMENT_NETWORKS:
        pytest.skip("Only for local testing")
    (fund_me, account) = deploy_fundme()
    bad_actor = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
