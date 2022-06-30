// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";

import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    using SafeMathChainlink for uint256;
    //0x8A753747A1Fa494EC906cE90E9f37563A8AF630e
    uint256 minimumAmount = 50 * (10**18); //50usd in wei; (50 usd*10**18)usd in wei is (0.017eth* 10**18 wei) eth in wei
    //uint256 minimumAmount = 50; //bujos way with the 'true' keyword fx
    address owner;
    address[] funders;
    mapping(address => uint256) public addressToAmountFunded;
    AggregatorV3Interface public aggregator;

    constructor(address _priceFeedAddress) public {
        owner = address(msg.sender);
        aggregator = AggregatorV3Interface(_priceFeedAddress);
    }

    //conversion to eth amount in wei
    function getEntranceFee() public view returns (uint256) {
        uint256 precision = 10**18;
        uint256 entranceFee = (minimumAmount * precision) / getEthPrice();
        return entranceFee;
    }

    function fund() public payable {
        //setting the minimum deposit value to 50 usd
        require(
            convertTrueEthPricetoUsd(msg.value) >= getEntranceFee(),
            "You need to send more Eth"
        );
        //mapping the address to the value deposited by that address
        addressToAmountFunded[msg.sender] += msg.value;
        // pushing the address to the funders array after depositing
        funders.push(msg.sender);
    }

    function balanceOfTheContract() public view returns (uint256) {
        uint256 balance = (address(this)).balance;
        return balance;
    }

    function getVersion() public view returns (uint256) {
        // calling the contract using the interface by locating where the address lives (ETHUSD price feed contract on rinkeby network)
        //AggregatorV3Interface aggregator = AggregatorV3Interface(
        //   0x8A753747A1Fa494EC906cE90E9f37563A8AF630e
        //);
        uint256 thisVersion = aggregator.version();
        return thisVersion;
    }

    function getEthPrice() public view returns (uint256) {
        //AggregatorV3Interface aggregator = AggregatorV3Interface(
        //  0x8A753747A1Fa494EC906cE90E9f37563A8AF630e
        //);
        (, int256 answer, , , ) = aggregator.latestRoundData();
        return uint256(answer * 10**10);
    }

    function getTrueEthPrice() public view returns (uint256) {
        //AggregatorV3Interface aggregator = AggregatorV3Interface(
        //   0x8A753747A1Fa494EC906cE90E9f37563A8AF630e
        //);
        (, int256 answer, , , ) = aggregator.latestRoundData();
        return uint256(answer / 10**8);
    }

    function convertEthtoUsd(uint256 _ethvalue) public view returns (uint256) {
        uint256 ethprice = getEthPrice();
        return ((ethprice * _ethvalue) / 10**18);
    }

    function convertTrueEthPricetoUsd(uint256 _ethvalue)
        public
        view
        returns (uint256)
    {
        uint256 ethprice = getTrueEthPrice();
        return (ethprice * _ethvalue);
    }

    modifier onlyOwner() {
        require(owner == msg.sender, "Admins only");
        _;
    }

    function withdraw() public payable onlyOwner {
        //sending this contract's balance to the admin who was initialized as the owner in the constructor using send method
        bool didSend = msg.sender.send(address(this).balance);
        require(didSend);
        //funders length starts from 1 whereas the index starts from zero hence loops until its no truer
        //during the looping all addresses balances mapped to the funders addresses will be set to zero
        for (
            uint256 fundersIndex = 0;
            fundersIndex < funders.length;
            fundersIndex++
        ) {
            addressToAmountFunded[funders[fundersIndex]] = 0;
        }
        //resetting the funders array to the new empty array
        funders = new address[](0);
    }
}
