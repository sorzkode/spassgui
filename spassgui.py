#!/usr/bin/env python3
#%%
'''
███████ ███    ██  █████  ███████ ███████ ██    ██     ██████   █████  ███████ ███████ 
██      ████   ██ ██   ██    ███     ███   ██  ██      ██   ██ ██   ██ ██      ██      
███████ ██ ██  ██ ███████   ███     ███     ████       ██████  ███████ ███████ ███████ 
     ██ ██  ██ ██ ██   ██  ███     ███       ██        ██      ██   ██      ██      ██ 
███████ ██   ████ ██   ██ ███████ ███████    ██        ██      ██   ██ ███████ ███████ 
                                                                                       
                                                                                                                                                                                                                                                                           
A random password generator and manager made with PySimpleGUI and SQLite3.
-
Author:
Mister Riley
sorzkode@proton.me
https://github.com/sorzkode

MIT License
Copyright (c) 2023 Mister Riley
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), 
to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

# Dependencies
import random
import string
import sqlite3
import base64
from tkinter.font import BOLD
import PySimpleGUI as sg
import pyperclip as pc
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Database setup
CON = sqlite3.connect("snazzy.db")
CUR = CON.cursor()

# PySimpleGUI version info
SGVERSION = sg.version

# GUI window theme
sg.theme("Default1")

# Application dropdown menu
APP_MENU = [["&Help", ["&Usage", "&About"]],["&Database", ["&Query All", "&Delete All"]]]

# Password characters
ABC_UPPER = list(string.ascii_uppercase)
ABC_LOWER = list(string.ascii_lowercase)
NUMERICAL_CHARACTERS = list(string.digits)
SPECIAL_CHARACTERS = ["!","@","#","$","%","^","&","*","(",")"]
AVOID_AMBIGUITY = ["1","O","l","0"]

# Defined fonts
FONT_TITLE = ("Lucida", 14, "bold")
FONT_LABEL = ("Lucida", 10, "bold")
FONT_INPUT = ("Lucida", 12, "bold")
FONT_BUTTON = ("Lucida", 12, "bold")

# All GUI elements
LAYOUT = [
    [sg.Menu(APP_MENU, tearoff=False, key='-MENU-')],
    [sg.Image(filename='assets/splogo.png', key='-LOGO-')],
    [
        sg.StatusBar(
            "Strong Enough",
            justification='center',
            text_color='White',
            background_color='Green',
            enable_events=True,
            key='-SBAR-'
        )
    ],
    [
        sg.Text("Password Length:", font=FONT_TITLE),
        sg.Slider(
            orientation='horizontal',
            range=(4, 50),
            default_value=10,
            font=FONT_INPUT,
            text_color='Black',
            pad=(5, 15),
            size=(35, 15),
            enable_events=True,
            key='-PASSLENGTH-',
        ),
    ],
    [
        sg.Text("Password Setup:", font=FONT_LABEL),
        sg.Checkbox("Avoid Ambiguity", default=True, disabled=False, key='-AMBIGUITY-', font=FONT_LABEL),
        sg.Checkbox("UPPER", default=True, disabled=False, key='-CUPPER-', font=FONT_LABEL),
        sg.Checkbox("lower", default=True, disabled=False, key='-CLOWER-', font=FONT_LABEL),
        sg.Checkbox("Numbers", default=True, disabled=False, key='-CNUMBERS-', font=FONT_LABEL),
        sg.Checkbox("Special", default=True, disabled=False, key='-CSPECIAL-', font=FONT_LABEL),
    ],
    [
        sg.Text("Password:", font=FONT_LABEL),
        sg.In("", font=FONT_INPUT, pad=(5, 15), enable_events=True, disabled=True, key='-PASSOUTPUT-'),
        sg.Button("Copy", font=FONT_BUTTON, pad=(5, 15), disabled=True),
    ],
    [
        sg.Button("Generate", font=FONT_BUTTON, pad=(5, 15), disabled=False),
        sg.Button("Reset", font=FONT_BUTTON, pad=(5, 15), disabled=True),
        sg.Text("Add Note:", font=FONT_LABEL),
        sg.In("", font=FONT_INPUT, size=20, enable_events=True, disabled=True, key='-PASSNOTE-'),
        sg.Button("Save", font=FONT_BUTTON, pad=(5, 15), disabled=True),
        sg.Button("Exit", font=FONT_BUTTON, pad=(5, 15)),
    ],
]

class SnazzyWindow:

    '''Initializing main application'''

    def __init__(self, window):
        self.window = sg.Window(
            "Snazzy Pass",
            LAYOUT,
            resizable=True,
            icon="assets\spg.ico",
            grab_anywhere=True,
            keep_on_top=True,
        )
        self.start()

    def pass_strength(self):
        '''Updating status bar based on password length'''
        try:
            pass_value = self.values['-PASSLENGTH-']
            if pass_value in range(4, 6, 1):
                self.window['-SBAR-'].update("Why so weak?", background_color='Red')
            elif pass_value in range(7, 9, 1):
                self.window['-SBAR-'].update("A little better...", background_color='Orange')
            elif pass_value in range(10, 15, 1):
                self.window['-SBAR-'].update("Strong enough", background_color='Green')
            elif pass_value in range(16, 35, 1):
                self.window['-SBAR-'].update("You must workout ;)", background_color='Green')
            elif pass_value in range(36, 49, 1):
                self.window['-SBAR-'].update("Steroid Alert!", background_color='Green')
            elif pass_value == 50:
                self.window['-SBAR-'].update("HERCULEAN!", background_color='Blue')
        except Exception as e:
            print(f"Error occurred in pass_strength: {e}")

    def reset_defaults(self):

        '''Application interface defaults'''

        self.window['-PASSOUTPUT-'].update("")
        self.window['-PASSLENGTH-'].update(10)     
        self.window['-CUPPER-'].update(True)
        self.window['-CLOWER-'].update(True)
        self.window['-CNUMBERS-'].update(True)
        self.window['-CSPECIAL-'].update(True)
        self.window['-AMBIGUITY-'].update(True)
        self.window["Copy"].update(disabled=True)
        self.window["Reset"].update(disabled=True)
        self.window['-PASSNOTE-'].update("", disabled=True)
        self.window["Save"].update(disabled=True)

    def generate_pass(self):
        '''Generating the password'''
        try:
            GENERATED_PASS = []
            ALL_CHARACTERS = []
            PASS_LENGTH = int(self.values['-PASSLENGTH-'])

            # checking for pass options
            if self.values['-CUPPER-'] is True:
                for i in range(PASS_LENGTH):
                    ALL_CHARACTERS.append(random.choice(ABC_UPPER))
           
            if self.values['-CLOWER-'] is True:
                for i in range(PASS_LENGTH):
                    ALL_CHARACTERS.append(random.choice(ABC_LOWER))
           
            if self.values['-CNUMBERS-'] is True:
                for i in range(PASS_LENGTH):
                    ALL_CHARACTERS.append(random.choice(NUMERICAL_CHARACTERS))
           
            if self.values['-CSPECIAL-'] is True:
                for i in range(PASS_LENGTH):
                    ALL_CHARACTERS.append(random.choice(SPECIAL_CHARACTERS))

            # Removing ambiguous characters if option is selected
            if self.values['-AMBIGUITY-'] is True:
                ALL_CHARACTERS = [x for x in ALL_CHARACTERS if x not in AVOID_AMBIGUITY]

            # Finalizing password
            if len(ALL_CHARACTERS) == 0:
                raise ValueError("No password options selected")

            for i in range(PASS_LENGTH):
                GENERATED_PASS.append(random.choice(ALL_CHARACTERS))

            random.shuffle(GENERATED_PASS)
            FINAL_PASS = ''.join(GENERATED_PASS)

            # Updating GUI
            self.window['-PASSOUTPUT-'].update(FINAL_PASS, disabled=True)
            self.window["Copy"].update(disabled=False)
            self.window["Reset"].update(disabled=False)
            self.window["Save"].update(disabled=False)
            self.window['-PASSNOTE-'].update(disabled=False)

        except ValueError as ve:
            sg.popup(f"Error: {ve}", grab_anywhere=True, keep_on_top=True)
        except Exception as e:
            sg.popup(f"An error occurred: {e}", grab_anywhere=True, keep_on_top=True)
   
    def copy_pass(self):
        '''Copying password to clipboard'''
        try:
            FINAL_PASS = self.values['-PASSOUTPUT-']
            pc.copy(FINAL_PASS)
            sg.popup_ok(
                "Copied to your clipboard",
                grab_anywhere=True,
                keep_on_top=True
            )
        except Exception as e:
            sg.popup(f"An error occurred while copying the password: {e}", grab_anywhere=True, keep_on_top=True)
    
    def check_defaults(self):
        '''Checks if default pass and salt exist'''

        # Replacing default password with user selected pass
        with open('psettings.txt', 'r') as PFILE:
            SNAZZY_PASSWORD = PFILE.readline().strip()
        
        if SNAZZY_PASSWORD == 'snazzypassdefault':
            try:
                NEWPASS = sg.popup_get_text(
                    "Please enter a new password to use Database",
                    grab_anywhere=True,
                    keep_on_top=True
                )
                with open('psettings.txt', 'w') as PFILE:
                    PFILE.write(NEWPASS)
            except Exception as e_message:
                sg.popup(
                    f"{e_message}",
                    grab_anywhere=True,
                    keep_on_top=True
                )

        with open('psettings.txt', 'r') as PFILE:
            SNAZZY_PASSWORD = PFILE.readline().strip()

        # Replacing default salt with user selected salt
        with open('ssettings.txt', 'r') as SFILE:
            SNAZZY_SALT = SFILE.readline().strip()

        if SNAZZY_SALT == 'snazzysaltdefault':
            try:
                NEWSALT = sg.popup_get_text(
                    "Please enter a new salt (any string of letters) to use Database",
                    grab_anywhere=True,
                    keep_on_top=True
                )
                with open('ssettings.txt', 'w') as SFILE:
                    SFILE.write(NEWSALT)
            except Exception as e_message:
                sg.popup(
                    f"{e_message}",
                    grab_anywhere=True,
                    keep_on_top=True
                )

        with open('ssettings.txt', 'r') as SFILE:
            SNAZZY_SALT = SFILE.readline().strip()

        ENCODED_PASSWORD = SNAZZY_PASSWORD.encode()
        ENCODED_SALT = SNAZZY_SALT.encode()

        KDF = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=ENCODED_SALT,
            iterations=390000,
        )

        SECRET_KEY = base64.urlsafe_b64encode(KDF.derive(ENCODED_PASSWORD))
        return SECRET_KEY

    def save_function(self):

        '''Saves note and password to database'''

        try:
            SECRET_KEY = self.check_defaults()
            FINAL_PASS = self.values['-PASSOUTPUT-']
            PASS_NOTE = self.values['-PASSNOTE-']
            ENCRYPTED_PASS = Fernet(SECRET_KEY).encrypt(FINAL_PASS.encode())
            CUR.execute('''
              CREATE TABLE IF NOT EXISTS snazzy_stuff
              ([pass_notes] TEXT, [passwords] TEXT)
              ''')
            CUR.execute(
                "INSERT INTO snazzy_stuff (pass_notes, passwords) values(?, ?)",
                (PASS_NOTE, ENCRYPTED_PASS.decode())
            )
            CON.commit()
            sg.popup_ok(
                "Saved to your Database",
                grab_anywhere=True,
                keep_on_top=True
            )
        except Exception as e:
            sg.popup_error(f"An error occurred while saving to the database: {str(e)}")

    def db_query(self):
        '''Queries and outputs all database contents'''
        try:
            SECRET_KEY = self.check_defaults()
            NOTES_LIST = []
            PASS_LIST = []

            for row in CUR.execute("select pass_notes from snazzy_stuff"):
                NOTES_LIST.append(row)

            for row in CUR.execute("select passwords from snazzy_stuff"):
                ITEMS = bytes(str(row), encoding='UTF-8')
                DECRYPTED_PASS = Fernet(SECRET_KEY).decrypt(ITEMS)
                PASS_LIST.append(DECRYPTED_PASS)

            DBLAYOUT = [
                [
                    sg.Text("Your Database Contents:", font=(FONT_TITLE)),
                ],
                [
                    sg.Listbox(NOTES_LIST, size=(20,10), disabled=True, key='-DBNOTES-'),
                    sg.Listbox(PASS_LIST, size=(20,10), disabled=True, key='-DBPASS-'),
                ],
            ]
            sg.Window(
                "Database",
                DBLAYOUT,
                resizable=True,
                icon="assets\spg.ico",
                grab_anywhere=True,
                keep_on_top=True,
            ).read(close=True)
        except Exception as e:
            sg.popup_error(f"An error occurred while querying the database: {str(e)}")

    def delete_db(self):
        """
        Delete all rows in the snazzy_stuff table
        :param con: Connection to the SQLite database
        :return:
        """
        try:
            WARNING_MESSAGE = sg.popup_ok_cancel(
                "WARNING! This will delete all database contents.",
                grab_anywhere=True,
                keep_on_top=True
            )
            if WARNING_MESSAGE == "OK":
                DELETE_COMMAND = 'DELETE FROM snazzy_stuff'
                CUR.execute(DELETE_COMMAND)
                CON.commit()
                sg.popup(
                    "Database contents deleted",
                    grab_anywhere=True,
                    keep_on_top=True
                )
            elif WARNING_MESSAGE == "Cancel":
                sg.popup(
                    "Database deletion cancelled",
                    grab_anywhere=True,
                    keep_on_top=True
                )
        except Exception as e:
            sg.popup_error(f"An error occurred while deleting the database: {str(e)}")

    def about_gui(self):
        '''About menu item'''
        sg.popup(
            "A random password generator and manager.",
            "",
            "Author: sorzkode",
            "Website: https://github.com/sorzkode",
            "License: MIT",
            "",
            "Snazzy Pass is a password generator first and foremost",
            "The password management functionality is basic and was added in version 2",
            "The local snazzy database isn't password protected but passwords are encrypted using Fernet",
            "",
            f"PySimpleGUI Version: {SGVERSION}",
            "",
            grab_anywhere=True,
            keep_on_top=True,
            title="About",
        )

    def usage_gui(self):

        '''Usage menu option'''

        sg.popup(
            "Follow these basic steps:",
            "",
            '1. Use the slider to select your password length',
            '2. Use the checkboxes to select options for your password',
            '3. Click the "Generate" button',
            '4. Type in a note to associate with your password and click the "Save" button to save to your local database',
            '5. Use the dropdown menus under "Database" to view database items or to delete the database',
            "",
            grab_anywhere=True,
            keep_on_top=True,
            title="Usage",
        )

    def start(self):

        '''Initilization function'''

        # Event loops when buttons are pressed / actions are taken in the app
        while True:
            self.event, self.values = self.window.read()

            # Window closed event
            if self.event == sg.WIN_CLOSED or self.event == "Exit":
                CON.close()
                break
            # Matching events to functions
            match self.event:
                case "-PASSLENGTH-":
                    self.pass_strength()
                case "Generate":
                    self.generate_pass()
                case "Reset":
                    self.reset_defaults()
                case "Copy":
                    self.copy_pass()
                case "Save":
                    self.save_function()
                case "About":
                    self.about_gui()
                case "Usage":
                    self.usage_gui()
                case "Query All":
                    self.db_query()
                case "Delete All":
                    self.delete_db()

        self.window.close()

if __name__ == "__main__":
    SnazzyWindow(sg)