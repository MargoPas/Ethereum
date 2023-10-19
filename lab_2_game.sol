// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract RockPaperScissors {
    address public player1;
    address public player2;
    string public choice1;
    string public choice2;
    bool public gameFinished;

    enum Choices { None, Rock, Paper, Scissors }

    mapping(string => Choices) choiceMapping;

    event GameResult(string result);

    constructor() {
        choiceMapping["rock"] = Choices.Rock;
        choiceMapping["paper"] = Choices.Paper;
        choiceMapping["scissors"] = Choices.Scissors;
    }

    modifier onlyPlayers() {
        require(msg.sender == player1 || msg.sender == player2, "You are not a player.");
        _;
    }

    modifier gameNotFinished() {
        require(!gameFinished, "The game is already finished.");
        _;
    }

    function register() public gameNotFinished {
        require(player1 == address(0) || player2 == address(0), "Both players are already registered.");
        if (player1 == address(0)) {
            player1 = msg.sender;
        } else {
            player2 = msg.sender;
        }
    }

    function play(string memory _choice) public onlyPlayers gameNotFinished {
        require(choiceMapping[_choice] != Choices.None, "Invalid choice. Use 'rock', 'paper' or 'scissors'.");
        require(msg.sender == player1 && bytes(choice1).length == 0 || msg.sender == player2 && bytes(choice2).length == 0, "You've already made a choice.");
        
        if (msg.sender == player1) {
            choice1 = _choice;
        } else {
            choice2 = _choice;
        }
        
        if (bytes(choice1).length != 0 && bytes(choice2).length != 0) {
            determineWinner();
        }
    }

    function determineWinner() internal {
        Choices player1Choice = choiceMapping[choice1];
        Choices player2Choice = choiceMapping[choice2];
        
        if (player1Choice == player2Choice) {
            emit GameResult("It's a draw!");
        } else if (
            player1Choice == Choices.Rock && player2Choice == Choices.Scissors ||
            player1Choice == Choices.Scissors && player2Choice == Choices.Paper ||
            player1Choice == Choices.Paper && player2Choice == Choices.Rock
        ) {
            emit GameResult("Player 1 wins!");
        } else {
            emit GameResult("Player 2 wins!");
        }
        
        gameFinished = true;
    }
}
