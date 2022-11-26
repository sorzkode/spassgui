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
sorzkode
sorzkode@proton.me
https://github.com/sorzkode

MIT License
Copyright (c) 2022 sorzkode
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
from tkinter.font import BOLD
import PySimpleGUI as sg
import pyperclip as pc

# Database setup
con = sqlite3.connect("snazzy.db")
cur = con.cursor()

# PySimpleGUI version info
psversion = sg.version

# GUI window theme
sg.theme("Default1")

# Application dropdown menu
app_menu = [["&Help", ["&Usage", "&About"]],["&Database", ["&Query All", "&Delete All"]]]

# Password characters
abc_upper = list(string.ascii_uppercase)
abc_lower = list(string.ascii_lowercase)
numerical_characters = list(string.digits)
special_characters = ["!","@","#","$","%","^","&","*","(",")"]
avoid_ambiguity = ["1","O","l","0"]

# All GUI elements
layout = [
    [
        sg.Menu(
            app_menu,
            tearoff=False,
            key='-MENU-'
            )
    ],
    [
        sg.Image(
            filename='assets\splogo.png',
            key='-LOGO-'
            )
    ],
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
        sg.Text(
            "Password Length:",
            font=('Lucida', 14, BOLD)
            ),
        sg.Slider(
            orientation='horizontal', 
            range=(4,50),
            default_value=10, 
            font=('Lucida', 12, BOLD),
            text_color='Black', 
            pad=(5, 15),
            size=(35, 15),
            enable_events=True,
            key='-PASSLENGTH-',
            ),
    ],
    [
        sg.Text(
            "Password Setup:",
            font=("Lucida", 10, BOLD)
            ),
        sg.Checkbox(
            "Avoid Ambiguity", 
            default=True, 
            disabled=False, 
            key='-AMBIGUITY-',
            ),
        sg.Checkbox(
            "UPPER", 
            default=True, 
            disabled=False, 
            key='-CUPPER-',
            ),
        sg.Checkbox(
            "lower", 
            default=True, 
            disabled=False, 
            key='-CLOWER-',
            ),
        sg.Checkbox(
            "Numbers", 
            default=True, 
            disabled=False, 
            key='-CNUMBERS-',
            ),
        sg.Checkbox(
            "Special", 
            default=True, 
            disabled=False, 
            key='-CSPECIAL-',
            ),
    ],
    [
        sg.Text(
            "Password:",
            font=("Lucida", 10, BOLD)
            ),
        sg.In(
            "", 
            font=("Lucida", 12, BOLD), 
            pad=(5, 15),
            enable_events=True,
            disabled=True,
            key='-PASSOUTPUT-'
            ),
        sg.Button(
            "Copy", 
            font=("Lucida", 12, BOLD), 
            pad=(5, 15), 
            disabled=True
            ),
    ],
    [
        sg.Button(
            "Generate", 
            font=("Lucida", 12, BOLD), 
            pad=(5, 15), 
            disabled=False
            ),
        sg.Button(
            "Reset", 
            font=("Lucida", 12, BOLD), 
            pad=(5, 15), 
            disabled=True
            ),
        sg.Text(
            "Add Note:",
            font=("Lucida", 10, BOLD)
            ),
        sg.In(
            "", 
            font=("Lucida", 12, BOLD),
            size=20, 
            enable_events=True,
            disabled=True,
            key='-PASSNOTE-'
            ),
        sg.Button(
            "Save", 
            font=("Lucida", 12, BOLD), 
            pad=(5, 15),
            disabled=True
            ),
        sg.Button(
            "Exit", 
            font=("Lucida", 12, BOLD), 
            pad=(5, 15)
            ),
    ],
]

class SnazzyWindow:

    '''Initializing main application'''

    def __init__(self, window):
        self.window = sg.Window(
            "Snazzy Pass",
            layout,
            resizable=True,
            icon="assets\spg.ico",
            grab_anywhere=True,
            keep_on_top=True,
        )
        self.start()

    def pass_strength(self):

        '''Updating status bar based on password length'''

        pass_value = self.values['-PASSLENGTH-']
        if pass_value in range(4,6,1):
            self.window['-SBAR-'].update("Why so weak?", background_color='Red')

        if pass_value in range(7,9,1):
            self.window['-SBAR-'].update("A little better...", background_color='Orange')

        if pass_value in range(10,15,1):
            self.window['-SBAR-'].update("Strong enough", background_color='Green')

        if pass_value in range(16,35,1):
            self.window['-SBAR-'].update("You must workout ;)", background_color='Green')

        if pass_value in range(36,49,1):
            self.window['-SBAR-'].update("Steroid Alert!", background_color='Green')

        if pass_value == 50:
            self.window['-SBAR-'].update("HERCULEAN!", background_color='Blue')

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
            generated_pass = []
            all_characters = []
            pass_length = int(self.values['-PASSLENGTH-'])

            # checking for pass options
            if self.values['-CUPPER-'] is True:
                for i in range(pass_length):
                    all_characters.append(random.choice(abc_upper))
           
            if self.values['-CLOWER-'] is True:
                for i in range(pass_length):
                    all_characters.append(random.choice(abc_lower))
           
            if self.values['-CNUMBERS-'] is True:
                for i in range(pass_length):
                    all_characters.append(random.choice(numerical_characters))
           
            if self.values['-CSPECIAL-'] is True:
                for i in range(pass_length):
                    all_characters.append(random.choice(special_characters))

            # Removing ambiguous characters if option is selected
            if self.values['-AMBIGUITY-'] is True:
                all_characters = [x for x in all_characters if x not in avoid_ambiguity]

            # Finalizng password
            for i in range(pass_length):
                generated_pass.append(random.choice(all_characters))

            random.shuffle(generated_pass)
            final_pass = (''.join(generated_pass))

            # Updating GUI 
            self.window['-PASSOUTPUT-'].update(final_pass, disabled=True)
            self.window["Copy"].update(disabled=False)
            self.window["Reset"].update(disabled=False)
            self.window["Save"].update(disabled=False)
            self.window['-PASSNOTE-'].update(disabled=False)

        except Exception as e_message:
            sg.popup(f"{e_message} - try again", grab_anywhere=True, keep_on_top=True)
            return
   
    def copy_pass(self):

        '''Copying password to clipboard'''

        final_pass = self.values['-PASSOUTPUT-']
        pc.copy(final_pass)
        sg.popup_ok("Copied to your clipboard", grab_anywhere=True, keep_on_top=True)

    def save_function(self):

        '''Saves note and password to database'''

        final_pass = self.values['-PASSOUTPUT-']
        pass_note = self.values['-PASSNOTE-']
        cur.execute('''
          CREATE TABLE IF NOT EXISTS snazzy_stuff
          ([pass_notes] TEXT, [passwords] TEXT)
          ''')
        cur.execute("INSERT INTO snazzy_stuff (pass_notes, passwords) values(?, ?)",(pass_note, final_pass))
        con.commit()
        sg.popup_ok("Saved to your Database", grab_anywhere=True, keep_on_top=True)

    def db_query(self):

        '''Queries and outputs all database contents'''

        query_list = []
        for row in cur.execute("select * from snazzy_stuff"):
            query_list.append(row)
        database_layout = [
            [
                sg.Text(
                    "Your Database Contents:",
                    font=('Lucida', 14, BOLD)
                    ),
            ],
            [
                sg.Listbox(
                    query_list,
                    size=(40,10),
                    disabled=True,
                    key='-DBKEY-'
                    ),
            ],
        ]
        sg.Window(
            "Database",
            database_layout,
            resizable=True,
            icon="assets\spg.ico",
            grab_anywhere=True,
            keep_on_top=True,
        ).read(close=True)

    def delete_db(self):
        """
        Delete all rows in the snazzy_stuff table
        :param con: Connection to the SQLite database
        :return:
        """
        warning_message = sg.popup_ok_cancel(
            "WARNING! This will delete all database contents.", 
            grab_anywhere=True, 
            keep_on_top=True
            )
        if warning_message == "OK":
            delete_command = 'DELETE FROM snazzy_stuff'
            cur.execute(delete_command)
            con.commit()
            sg.popup(
                "Database contents deleted",
                grab_anywhere=True,
                keep_on_top=True
                )
        if warning_message == "Cancel":
            sg.popup(
                "Database deletion cancelled",
                grab_anywhere=True,
                keep_on_top=True
                )

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
            "The local snazzy database isn't password protected and contents aren't encrypted or hashed",
            "Therefore, it should only be used locally and access to the application should be restricted if you plan to use the database to store passwords",
            "",
            f"PySimpleGUI Version: {psversion}",
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
                con.close()
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