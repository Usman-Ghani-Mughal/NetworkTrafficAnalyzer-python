from Capture_Packet import*


class InterFaceFrame:
    def __init__(self, toplevel, root, username=""):
        self.root = root
        self.username = username
        self.frame = toplevel

        self.frame.title(interface_title)

        # ===== Add Icon ===== #
        self.icon = PhotoImage(file=interface_icon_path)
        self.frame.iconphoto(False, self.icon)

        # ===== Add close protocol ===== #
        self.frame.protocol("WM_DELETE_WINDOW", self.on_close)

        # ======== Adding BackGround Image ======= #
        self.bg_I = ImageTk.PhotoImage(file=interface_bg_path)
        self.bg_image_I = Label(self.frame, image=self.bg_I).place(x=0, y=0, relwidth=1, relheight=1)

        # ======== Adding menu Bar ======= #
        self.make_menu_bar()
        # ======== Adding items on This frame ======= #
        self.add_items_on_frame()

    def on_close(self):
        self.root.destroy()

    def make_menu_bar(self):
        main_menu = Menu(self.frame)
        self.frame.config(menu=main_menu)

        # ===== creating File menu ===== #
        file_menu = Menu(main_menu, tearoff=False)
        main_menu.add_cascade(label='File', menu=file_menu)

        # ===== creating File menu (open) ===== #
        file_menu.add_command(label='Open', command=self.clicking_on_menu_options)
        file_menu.add_command(label='Open Recent', command=self.clicking_on_menu_options)
        file_menu.add_command(label='Close', command=self.clicking_on_menu_options)

        file_menu.add_separator()

        # ===== creating File menu (save) ===== #
        file_menu.add_command(label='Save', command=self.clicking_on_menu_options)
        file_menu.add_command(label='Save As', command=self.clicking_on_menu_options)

        file_menu.add_separator()

        # ===== creating File menu (p/q) ===== #
        file_menu.add_cascade(label='Print', command=self.clicking_on_menu_options)
        file_menu.add_command(label='Quit', command=self.clicking_on_menu_options)

        # ======================================================================================================== #

        # ===== creating Edit menu ===== #
        edit_menu = Menu(main_menu, tearoff=False)
        main_menu.add_cascade(label='Edit', menu=edit_menu)

        # ===== creating File menu (open) ===== #
        edit_menu.add_command(label='Copy', command=self.clicking_on_menu_options)
        edit_menu.add_command(label='Find Packet', command=self.clicking_on_menu_options)
        edit_menu.add_command(label='Find Next', command=self.clicking_on_menu_options)
        edit_menu.add_command(label='Find Previous', command=self.clicking_on_menu_options)

        edit_menu.add_separator()

        # ===== creating File menu (save) ===== #
        edit_menu.add_command(label='Mark All', command=self.clicking_on_menu_options)
        edit_menu.add_command(label='Un Mark All', command=self.clicking_on_menu_options)
        edit_menu.add_command(label='Mark Next', command=self.clicking_on_menu_options)
        edit_menu.add_command(label='Mark Previous', command=self.clicking_on_menu_options)

        edit_menu.add_separator()

        # ===== creating File menu (p/q) ===== #
        edit_menu.add_cascade(label='Preferences', command=self.clicking_on_menu_options)

        # ======================================================================================================== #

        # ===== creating View menu ===== #
        view_menu = Menu(main_menu, tearoff=False)
        main_menu.add_cascade(label='View', menu=view_menu)

        # ======================================================================================================== #

        # ===== creating Capture menu ===== #
        cap_menu = Menu(main_menu, tearoff=False)
        main_menu.add_cascade(label='Capture', menu=cap_menu)

        # ======================================================================================================== #

        # ===== creating Capture menu ===== #
        analyse_menu = Menu(main_menu, tearoff=False)
        main_menu.add_cascade(label='Analyse', menu=analyse_menu)

        # ======================================================================================================== #

        # ===== creating tool menu ===== #
        tool_menu = Menu(main_menu, tearoff=False)
        main_menu.add_cascade(label='Tools', menu=tool_menu)

        # ======================================================================================================== #

        # ===== creating help menu ===== #
        help_menu = Menu(main_menu, tearoff=False)
        main_menu.add_cascade(label='Help', menu=help_menu)

    def add_items_on_frame(self):
        # ======== Data Frame ============ #
        frame_data_I = Frame(self.frame, bg=interface_bg_color, relief="sunken", borderwidth=2)
        frame_data_I.place(x=580, y=0, height=545, width=615)

        welcome = Label(
            frame_data_I, text="Welcome : {}".format(self.username), font=("Algerian", 30, "bold"), fg=menu_bar_color,
            bg=interface_bg_color, relief="groove", borderwidth=5).place(x=135, y=20)

        title = Label(
            frame_data_I, text="Network Traffic Analyser", font=("Comic Sans MS", 30, "bold"), fg=menu_bar_color,
            bg=interface_bg_color, relief="raised", borderwidth=2).place(x=55, y=120)


        info_label = Label(
            frame_data_I, text="Select Interface", font=(rockwell, 20), fg=menu_bar_color,
            bg=interface_bg_color).place(x=20, y=200)

        # ======== Interface ether Button ============ #
        ether_label = Label(frame_data_I, text="1: ", bg=dark_blue, fg="white", font=(comic_sans_ms, 16),
                        relief='raised').place(x=20, y=250, width=50, height=40)
        ether_button = Button(frame_data_I, text="Ethernet", bg=dark_blue, fg="white", font=(comic_sans_ms, 16),
                        relief='raised', command=self.start_capturing).place(x=70, y=250, width=250, height=40)

        # ======== Interface wifi Button ============ #
        wifi_label = Label(frame_data_I, text="2: ", bg=dark_blue, fg="white", font=(comic_sans_ms, 16),
                            relief='raised').place(x=20, y=300, width=50, height=40)
        wifi_button = Button(frame_data_I, text="Wi-Fi", bg=dark_blue, fg="white", font=(comic_sans_ms, 16),
                        relief='raised', command=self.start_capturing).place(x=70, y=300, width=250, height=40)

        # ======== Interface lAN Button ============ #
        wifi_label = Label(frame_data_I, text="3: ", bg=dark_blue, fg="white", font=(comic_sans_ms, 16),
                           relief='raised').place(x=20, y=350, width=50, height=40)
        lan_button = Button(frame_data_I, text="Local Area Connection", bg=dark_blue, fg="white",
                        font=(comic_sans_ms, 16),relief='raised', command=self.start_capturing).\
                        place(x=70, y=350, width=250, height=40)

        reference_label = Label(frame_data_I, text="Created by: Shaid Mehmood and Hanan Salik", bg=interface_bg_color,
                            fg="white", font=(comic_sans_ms, 8)).place(x=5, y=521, width=230, height=20)

    def clicking_on_menu_options(self):
        pass

    def start_capturing(self):
        toplevel1 = Toplevel(self.frame, bg=cap_packet_bg)
        self.frame.withdraw()
        toplevel1.geometry("1199x550+100+50")
        toplevel1.resizable(False, False)
        cap_obj = CapturePacket(toplevel1, self.frame, self.root)
