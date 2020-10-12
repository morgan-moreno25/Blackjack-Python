# BLACKJACK

This project is the Milestone 2 project from the [Python Bootcamp Udemy course](https://www.udemy.com/course/complete-python-bootcamp/) by Jose Portilla.

---

## OVERVIEW

The purpose of this project was to implement what I have learned since the first milestone project to create a text-based blackjack game. The learning topics include:

    - Object Oriented Programming
    - Modules and Packages
    - Errors and Exceptions Handling

For this project I used 5 classes and made use of class inheritence for the Player class.

- Card Object
    - This object represents one of the 52 cards used to play this game.
    - I used the global `suits` and `ranks` tuples as well as the global `values` dictionaries to create instances of this object in the Deck object
- Deck Object
    - This object represents a collection of 52 Card objects
    - It contains a method that will shuffle the list of cards into a random order
    - It contains another method that will deal one card from the deck
- Hand Object
    - This object represents the current hand for a player during the game
    - Has a hit method for when a player decides to hit during the game
        - Adds a single card to the current hand
    - Has an adjust_for_aces method which keeps the player from busting whenever an ace is added to their hand
- Dealer / Player Object
    - The Dealer object is used to represent the Dealer player in the game. It is the parent class to the Player object
    - The Player object inherits the attributes/methods from the dealer classes
        - Has it's own chips attribute which represents the current chip balance for the player
        - Has it's own collect_winnings method which is used to collect the winnings from a game when the player has won
- Game Object
    - This object contains all of the attributes and logic used to play the game

I also used the built-in Unittest library to write unit tests for functions that I felt needed to be tested in order to ensure the game ran as I wanted it to.

---

## Technology

    - Python
    - Unittest Library

---

## What I Learned

From the completion of this project, I gained experience with the following:

    - Using try/except/(else)/finally blocks to handle errors in user input
    - Python script global __name__ variable and using it to execute logic in a script
    - Using the Unittest library to set up unit tests and ensure that my classes and their methods are working as they should be
    - Class Inheritance in Python

---
