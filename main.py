from InterFaceFrame import*
from RegistrationFrame import*
import sqlite3
from subprocess import call


class Login:
    def __init__(self, root):
        self.python_path = python_path_
        self.spider_path = spider_path_
        call([self.python_path, self.spider_path])

        self.iterfaceframe = None
        self.root = root
        self.icon = PhotoImage(file=login_icon_path)
        self.root.title(login_title)
        self.root.iconphoto(False, self.icon)
        self.root.geometry(login_geometry)
        self.root.resizable(False, False)
        # ======== Adding BackGround Image ======= #
        self.bg = ImageTk.PhotoImage(file=Login_bg_path)
        self.bg_image = Label(self.root, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)

        # ======== Data Frame ============ #
        frame_data = Frame(self.root, bg=frame_bg_color, relief="sunken", borderwidth=2)
        frame_data.place(x=50, y=100, height=340, width=500)
        # ======== Title ============ #
        title = Label(
            frame_data, text="Login Here", font=(comic_sans_ms, 35, "bold"), fg=dark_blue, bg=frame_bg_color).\
            place(x=135, y=20)
        # ======== Extra info ============ #
        members_label = Label(
            frame_data, text="Admin Team Should Login Here", font=(rockwell, 14, "bold"), fg=dark_blue,
            bg=frame_bg_color).place(x=100, y=95)

        # ======== User Name ============ #
        username_label = Label(frame_data, text="User Name", font=(rockwell, 14, "bold"), fg=dark_blue, bg=frame_bg_color)
        username_label.    place(x=40, y=160)
        self.username = Entry(frame_data, font=(rockwell, 14), bg=login_i_f_color)
        self.username.place(x=160, y=160, width=300, height=30)

        # ======== Password ============ #
        userpas_label = Label(
            frame_data, text="Password", font=(rockwell, 14, "bold"), fg=dark_blue, bg=frame_bg_color). \
            place(x=40, y=210)
        self.userpas = Entry(frame_data, font=(rockwell, 14), bg=login_i_f_color, show="*")
        self.userpas.place(x=160, y=210, width=300, height=30)

        # ======== Forget Button ============ #
        forget_button = Button(frame_data, text="Forget Password?", bd=0, bg=frame_bg_color, fg="black", font=(rockwell, 8)).\
            place(x=200, y=260, width=120, height=20)

        # ======== Login Button ============ #
        login_button = Button(frame_data, text="Login", bg=dark_blue, fg=white, font=(comic_sans_ms, 22), relief=
                        'groove', command=self.check_login).place(x=160, y=288, width=200, height=50)

        # ======== Skip button ============ #
        skip_button = Button(frame_data, text="Skip now", bg=frame_bg_color, fg="black", font=(comic_sans_ms, 8),
                      relief='raised', command=self.inter_face_frame).place(x=395, y=315, width=100, height=20)
        # ======== Register Button ============ #
        register_btn = Button(self.root, text="Register Now", font=(comic_sans_ms, 20),
                              bg=frame_bg_color, fg=dark_blue ,relief="raised", borderwidth=2, command=self.make_regForm)
        register_btn.place(x=200, y=470, height=50, width=220)

    def inter_face_frame(self):
        toplevel = Toplevel(self.root)
        self.root.withdraw()
        toplevel.geometry("1199x550+100+50")
        toplevel.resizable(False, False)
        interface_obj = InterFaceFrame(toplevel, self.root)

    def make_regForm(self):
        toplevel = Toplevel(self.root)
        # self.root.withdraw()
        toplevel.geometry("1199x550+100+50")
        toplevel.resizable(False, False)
        reg_form_obj = RegistrationFrame(toplevel, self.root)

    def check_login(self):
        username = str(self.username.get())
        password = str(self.userpas.get())

        if len(username) == 0 or len(password) == 0:
            messagebox.showerror("Error", "Invalid Username or Password!")
            return
        else:
            try:
                con = sqlite3.connect('Network_traffic.db')
                c = con.cursor()
                query = """
                            SELECT * FROM Users WHERE username = '{}' and password = '{}'
                        """.format(username, password)
                c.execute(query)
                result = c.fetchall()
                if result:
                    toplevel = Toplevel(self.root)
                    self.root.withdraw()
                    toplevel.geometry("1199x550+100+50")
                    toplevel.resizable(False, False)
                    interface_obj = InterFaceFrame(toplevel, self.root, username)
                else:
                    messagebox.showerror("Error", "Invalid user name or password")
                con.commit()
                con.close()
            except:
                messagebox.showerror("Error", "There is some error try again")


root = Tk()
obj = Login(root)
root.mainloop()


