from tkinter import*
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
from all_const_strings import *
import sqlite3
from tkinter import messagebox
import re


class RegistrationFrame:
    def __init__(self, toplevel, root):
        self.root = root
        self.frame = toplevel
        self.frame.title(registration_title)

        self.icon = PhotoImage(file=registration_icon_path)
        self.frame.iconphoto(False, self.icon)

        # ===== Add close protocol ===== #
        self.frame.protocol("WM_DELETE_WINDOW", self.on_close)

        # ======== Adding BackGround Image ======= #
        self.bg_r = ImageTk.PhotoImage(file=registration_bg_path)
        self.bg_image_r = Label(self.frame, image=self.bg_r).place(x=0, y=0, relwidth=1, relheight=1)

        # ======== variables ============ #
        self.frame_data = None
        self.title = None
        self.username_label = None
        self.username = None
        self.useremail_label = None
        self.username_email = None
        self.userpas_label = None
        self.user_password = None
        self.reg_btn = None
        self.already_sign_in_btn = None

        # ========= Make Frame ============ #
        self.make_frame()

    def back_to_login(self):
        self.frame.destroy()

    def make_frame(self):
        # ======== Add Frame ============ #
        self.frame_data = Frame(self.frame, bg=reg_bg_color, relief="sunken", borderwidth=2)
        self.frame_data.place(x=4, y=4, height=544, width=745)

        # ======== Title ============ #
        self.title = Label(
            self.frame_data, text="Registration Form", font=("Comic Sans MS", 35, "bold"), fg=white, bg=reg_bg_color). \
            place(x=135, y=20)

        # ======== User Name ============ #
        self.username_label = Label(
            self.frame_data, text="User Name", font=(comic_sans_ms, 14, "bold"), fg=white, bg=reg_bg_color). \
            place(x=130, y=180)
        self.username = Entry(self.frame_data, font=("Rockwell", 14), fg=white, bg=reg_i_f_color)
        self.username.place(x=250, y=180, width=300, height=30)

        # ======== User Email ============ #
        self.useremail_label = Label(
            self.frame_data, text="Email", font=(comic_sans_ms, 14, "bold"), fg=white, bg=reg_bg_color). \
            place(x=130, y=230)
        self.username_email = Entry(self.frame_data, font=(rockwell, 14), fg=white, bg=reg_i_f_color)
        self.username_email.place(x=250, y=230, width=300, height=30)
        # ======== Password ============ #
        self.userpas_label = Label(
            self.frame_data, text="Password", font=(comic_sans_ms, 14, "bold"), fg=white, bg=reg_bg_color). \
            place(x=130, y=280)
        self.user_password = Entry(self.frame_data, font=(rockwell, 14), fg=white, bg=reg_i_f_color, show="*")
        self.user_password.place(x=250, y=280, width=300, height=30)

        # ======== Already Sign in Button ============ #
        self.already_sign_in_btn = Button(
            self.frame_data, text="Already Registered", bg=frame_bg_color, fg=dark_blue, font=(comic_sans_ms, 8, "bold"),
            relief=
            'groove', command=self.back_to_login).place(x=250, y=320, width=150, height=20)

        # ======== Register Button ============ #
        self.reg_btn = Button(
            self.frame_data, text="Register", bg=frame_bg_color, fg=dark_blue, font=(comic_sans_ms, 14, "bold"),
            relief=
            'groove', command=self.register_user).place(x=250, y=400, width=250, height=50)

    def register_user(self):
        username = str(self.username.get())
        email = str(self.username_email.get())
        password = str(self.user_password.get())

        if len(username) == 0 or len(email) == 0 or len(password) == 0:
            messagebox.showwarning("Warning", 'please fill all fields!', parent=self.frame)
        elif len(username) < 5 or len(username) > 20:
            messagebox.showwarning("Warning", 'user name must be between 5 to 20 characters!', parent=self.frame)
        elif not re.match(r"[\w-]{1,20}@\w{2,20}\.\w{2,3}$", email):
            messagebox.showwarning("Warning", 'Email is invalid please enter valid email!', parent=self.frame)
        elif len(password) < 5 or len(password) > 20:
            messagebox.showwarning("Warning", 'password must be between 5 to 20 characters!', parent=self.frame)
        else:
            try:
                con = sqlite3.connect(DB_NAME)  # Make connection with database
                c = con.cursor()
                query = user_register_query.format(username, email, password)  # Register Query
                c.execute(query)
                con.commit()
                con.close()
                messagebox.showinfo("INFO", "Successfully Registered!")
                self.back_to_login()
            except:
                messagebox.showerror("Error", "There is some error try again", parent=self.frame)

    def on_close(self):
        self.root.destroy()

