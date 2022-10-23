from brownie import FundMe, network, config, MockV3Aggregator
from scripts.helpful_scripts import (
    deploy_mocks,
    get_account,
    LOCAL_DEVELOPMENT_NETWORKS,
    FORKED_ENVIRONMENTS,
)  ##pulling the get account method and deploy mocks method from helpful scripts

##the deploy script for fundme using either pricefeedaddress contract deployed by the testnets or deploying mocks
##setting the address and whether to publish the contract or not, as pulled from the brownie-config
def deploy_fundme():
    account = get_account()
    if len(FundMe) > 0:
        fund_me = FundMe[-1]
    else:
        if network.show_active() not in LOCAL_DEVELOPMENT_NETWORKS:
            priceFeedAddress = config["networks"][network.show_active()][
                "eth_usdt_price_feed"
            ]
            fund_me = FundMe.deploy(
                priceFeedAddress,
                {"from": account},
                publish_source=config["networks"][network.show_active()].get("verify"),
            )
            print(f"Contract deployed at {fund_me.address}")
        else:
            if len(MockV3Aggregator) <= 0:
                deploy_mocks()
            priceFeedAddress = MockV3Aggregator[-1]
            fund_me = FundMe.deploy(
                priceFeedAddress,
                {"from": account},
                publish_source=config["networks"][network.show_active()].get("verify"),
            )
            print(f"Contract deployed at {fund_me.address}")
    return (fund_me, account)


##main brownie method
def main():
    deploy_fundme()
