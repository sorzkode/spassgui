[[CLI Version](https://github.com/sorzkode/spasscli)]
[[MIT Licence](https://en.wikipedia.org/wiki/MIT_License)]


![alt text](https://raw.githubusercontent.com/sorzkode/spassgui/master/assets/splogo.png)

# Snazzy Pass GUI

A random password generator with tkinter GUI.

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

  [[PIL (Pillow) module](https://pypi.org/project/Pillow/)] 

  [[clipboard module](https://pypi.org/project/clipboard/)]

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
Select your password length
Select the number of special charactors you want to include
Selectthe number of digits you want to include
Click "GO"
```
## Features

  Password length of 6 to 15 characters
  
  Zero to 3 special characters
  
  Zero to 3 numbers
  
  Copy button to copy output to your clipboard
  
  Reset button to clear password field
  
  Exit button closes the app




