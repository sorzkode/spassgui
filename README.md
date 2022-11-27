[![CodeQL](https://github.com/sorzkode/spassgui/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/sorzkode/spassgui/actions/workflows/codeql-analysis.yml)
[[CLI Version](https://github.com/sorzkode/spasscli)]
[[MIT Licence](https://en.wikipedia.org/wiki/MIT_License)]


![alt text](https://raw.githubusercontent.com/sorzkode/spassgui/master/assets/spgit.png)

# Snazzy Pass GUI

A random password generator and manager made with PySimpleGUI and SQLite3.

## Example

![alt text](https://raw.githubusercontent.com/sorzkode/spassgui/master/assets/example.png)

## Installation

Download zip from Github, changedir (cd) to the script directory and run the following:
```
pip install -e .
```
*This will install the Snazzy Pass package locally 

Installation isn't required to run the script but you will need to ensure the requirements below are met.

## Requirements

  [[Python 3](https://www.python.org/downloads/)]

  [[PySimpleGUI](https://pypi.org/project/PySimpleGUI/)] 

  [[pyperclip](https://pypi.org/project/pyperclip3/)]

  [[cryptography]](https://pypi.org/project/cryptography/)]

  [[tkinter](https://docs.python.org/3/library/tkinter.html)] :: Linux Users

## Usage

If installed you can use the following command syntax:
```
python -m spassgui
```

Otherwise you can run the script directly by changing directory (cd) in a terminal of your choice to the spassgui directory and using the following syntax:
```
python spassgui.py
```

Once initiated, use the following steps:
```            
1. Use the slider to select your password length',
2. Use the checkboxes to select options for your password',
3. Click the "Generate" button',
4. Type in a note to associate with your password and click the "Save" button to save to your local database',
5. Use the dropdown menus under "Database" to view database items or to delete the database',
```
## Features

  Password length of 4 to 50 characters
  
  Avoid Ambiguous characters (1,l,0,O)
  
  Include / exclude: 
    uppercase letters
    lowercase letters
    numbers
    special characters
  
  Copy button to copy output to your clipboard
  
  Reset button to clear fields / reset defaults

  Option to save the password with an associated note to a SQLite database
    database fields can be queried and or deleted using the "Database" dropdown menu
  
  Exit button closes the app

## Please Note

  Snazzy Pass is a password generator first and foremost

  The password management functionality is basic and was added in version 2
  
  The local snazzy database isn't password protected but passwords are encrypted using Fernet




