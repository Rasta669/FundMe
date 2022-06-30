from brownie import network, accounts, config, MockV3Aggregator

##from web3 import Web3 - as referred to the 18 decimal mockv3 constructor deployment.

LOCAL_DEVELOPMENT_NETWORKS = ["development", "local-ganache"]
FORKED_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]

##get the deploying account based on the network used whether its local development or testnet
def get_account():
    if (
        network.show_active() in LOCAL_DEVELOPMENT_NETWORKS
        or network.show_active() in FORKED_ENVIRONMENTS
    ):
        return accounts[0]
    else:
        return accounts.load("rastas")


##deploying mockv3 script
def deploy_mocks():
    account = accounts[0]
    print("Deploying mockV3Aggregator!")
    ##mock = MockV3Aggregator.deploy(8, Web3.toWei(2000, "ether"), {"from": account}) - for 18 decimals
    mock = MockV3Aggregator.deploy(
        8, 20000000000, {"from": account}
    )  ##for the fundme-getEthPrice fx
    print(f"MockV3 deployed at {mock.address}")
    return mock.address
