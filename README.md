# Expense Tracker

## Project setup
1. Run "make install" to setup a python environment with all the requirements already installed.
2. Run "make" to run the application.

## Overview

This project aims at developing a simple terminal app for tracking expenses across multiple banks or services.

## What is a transaction?
The whole project has to deal with transactions. They are represented as a simple object with attributes:
- date
- sender
- receiver
- amount (always positive)
- currency
- tag representing a category

## Functionalities

### Transactions parsing
The most important functionality this application must provide is that of reading a transaction file in excel (or other formats?) and parse it. The results must be "standardized" in a format the application will use to keep track of all transactions.

### Transaction labelling
Provide the user to label each transaction in order to keep track of user-defined expense motivations.

### Financial Dashboard
Provide the user with insights about his/her spending habits.

### Keep track of money
Provide the user with an overview of where all his/her money is across multiple accounts.
