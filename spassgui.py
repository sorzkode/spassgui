'''
███████ ███    ██  █████  ███████ ███████ ██    ██     ██████   █████  ███████ ███████ 
██      ████   ██ ██   ██    ███     ███   ██  ██      ██   ██ ██   ██ ██      ██      
███████ ██ ██  ██ ███████   ███     ███     ████       ██████  ███████ ███████ ███████ 
     ██ ██  ██ ██ ██   ██  ███     ███       ██        ██      ██   ██      ██      ██ 
███████ ██   ████ ██   ██ ███████ ███████    ██        ██      ██   ██ ███████ ███████ 
                                                                                       
                                                                                       
A random password generator with a tkinter GUI
-
Author:
sorzkode
sorzkode@proton.me
https://github.com/sorzkode

MIT License
Copyright (c) 2022 sorzkode

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

#Importing required libraries / modules
from tkinter import *
import tkinter as tk
from tkinter.ttk import *
import random
import string
from turtle import bgcolor
from PIL import Image, ImageTk
import tkinter.font as tkFont
from tkinter import messagebox
import clipboard as cb

#user interface setup
usr_interface = tk.Tk()
usr_interface.title("snazzy pass")
usr_interface.geometry('375x175')
ui_width = 375
ui_height = 175
x_left = int(usr_interface.winfo_screenwidth()/2 - ui_width/2)
y_top = int(usr_interface.winfo_screenheight()/2 - ui_height/2)
app_title = Label(usr_interface, text="snazzy pass - random generator", font=("Arial Bold", 14)).place(x=50, y=10)
def_font = tkFont.nametofont("TkDefaultFont")
def_font.config(size=12)
usr_interface.geometry("+{}+{}".format(x_left, y_top))

#icon insertion and placement
logo = Image.open("assets/Lock.png")
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.place(x=10, y=5)

#characters to generate password from
alphabets = list(string.ascii_letters)
digits = list(string.digits)
special_characters = list("!@#$%^&*()")
characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")

#password length selection
pass_length_label = Label(usr_interface, text="Password Length:", font=("Arial Bold", 12), background="yellow", width=40).place(x=5, y=50)
pnote_label = Label(usr_interface, text="(choose from 6 to 15 characters)", font=("Arial Italic", 8), background="yellow").place(x=190, y=52)
default_pass_length = IntVar()
default_pass_length.set(10)
pass_length = Spinbox(usr_interface, from_=6, to=15, width=3, textvariable=default_pass_length, font=("Arial Bold", 10))
pass_length.place(x=148, y=51)

#number of special characters to include
schar_nmbr_label = Label(usr_interface, text="Special Characters:", relief=SUNKEN, width=19).place(x=5, y=87)
default_schar_nmbr = IntVar()
default_schar_nmbr.set(1)
schar_nmbr = Spinbox(usr_interface, from_=0, to=3, width=3, textvariable=default_schar_nmbr)
schar_nmbr.place(x=140, y=90)

#amount of numbers to include
nmbr_label = Label(usr_interface, text="Numbers:", relief=SUNKEN, width=12).place(x=190, y=87)
default_nmbr = IntVar()
default_nmbr.set(2)
nmbr = Spinbox(usr_interface, from_=0, to=3, width=3, textvariable=default_nmbr)
nmbr.place(x=263, y=90)

#password generation 
def select_gen():
    schar_sel = int(schar_nmbr.get())
    l_sel = int(pass_length.get())
    n_sel = int(nmbr.get())
    total_chars = schar_sel + n_sel
    final_count = l_sel - total_chars 
    global text_box
    text_box = tk.Text(usr_interface, width=15, height=1)
    text_box.place(x=65, y=135)
    text_box.tag_configure("center", justify="center")
    text_box.tag_add("center", 1.0, "end")
    
    #creating pw list
    password = []
    
    for i in range(final_count):
        password.append(random.choice(alphabets))

    for i in range(n_sel):
        password.append(random.choice(digits))

    for i in range(schar_sel):
        password.append(random.choice(special_characters))

	#shuffling pw 
    random.shuffle(password)

	#final pw output
    text_box.insert(1.0,''.join(password))

#copy button command
def select_cpy():
    pw_results = text_box.get(1.0, END)
    cb.copy(pw_results)
    messagebox.showinfo("Success", "Copied to clipboard")

#exit button command
def select_ext():
    usr_interface.quit()

#reset button command
def select_rst():
    text_box.delete(1.0, END)

#exit button selection
ext_btn = tk.Button(usr_interface, command=lambda:select_ext(), text="Exit", bg="Red", fg="White")
ext_btn.place(x=330, y=130)

#generate button selection
gen_btn = tk.Button(usr_interface, command=lambda:select_gen(), text="GO", bg="green", fg="White", width=5)
gen_btn.place(x=312, y=80)
gen_lbl = Label(usr_interface, text="Output:", font=('Arial Bold', 11)).place(x=5, y=135)

#copy button selection
cpy_btn = tk.Button(usr_interface, command=lambda:select_cpy(), text="Copy")
cpy_btn.place(x=212, y=130)

#copy button selection
rst_btn = tk.Button(usr_interface, command=lambda:select_rst(), text="Reset", bg="black", fg="white")
rst_btn.place(x=263, y=130)

usr_interface.mainloop()