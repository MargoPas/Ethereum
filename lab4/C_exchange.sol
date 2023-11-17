// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "contracts/A_contract.sol";

contract TokenExchange {
    CustomToken public tokenA;
    CustomToken public tokenB;

    event TokensExchanged(address indexed from, uint256 amount, string tokenFrom, string tokenTo);

    constructor(address _tokenA, address _tokenB) {
        tokenA = CustomToken(_tokenA);
        tokenB = CustomToken(_tokenB);
    }

    modifier hasBalance(address token, uint256 amount) {
        require(ERC20(token).balanceOf(msg.sender) >= amount, "Insufficient balance");
        _;
    }

    function exchangeTokens(address tokenFrom, address tokenTo, uint256 amount) external hasBalance(tokenFrom, amount) {
        ERC20(tokenFrom).transferFrom(msg.sender, address(this), amount);

        uint256 amountB = amount / 100;

        tokenB.transfer(msg.sender, amountB);

        emit TokensExchanged(msg.sender, amount, ERC20(tokenFrom).symbol(), tokenB.symbol());
    }

    function depositTokens(address token, uint256 amount) external hasBalance(token, amount) {
        ERC20(token).transferFrom(msg.sender, address(this), amount);
    }
}
