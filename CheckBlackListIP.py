import pandas as pd

from tkinter import *
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
from all_const_strings import *
from protocols_and_numbers import *
from random import randint
import dpkt
from tkinter import messagebox


class CheckBlackListIP:
    def __init__(self, packets_list, toplevel2, root0, root1, root2 ):
        self.root0 = root0
        self.root1 = root1
        self.root2 = root2
        self.frame = toplevel2
        self.packets_list = packets_list
        self.current_packet_count = 0
        self.index = 0
        self.black_list_ips_indexes = []

        self.icon = PhotoImage(file=capture_icon_path)
        self.frame.title("Black List IP Packets")
        self.frame.iconphoto(False, self.icon)

        # ===== Add close protocol ===== #
        self.frame.protocol("WM_DELETE_WINDOW", self.on_close)

        # ======== Adding menu Bar ======= #
        self.make_menu_bar()

        self.tv = ttk.Treeview(self.frame, columns=(1, 2), show="headings", height="10",
                               selectmode='browse')

        self.tv.pack(side=LEFT)
        self.tv.place(x=0, y=0)
        self.tv.heading(1, text="No.")
        self.tv.heading(2, text="Black List IP")

        # self.tv.bind('<ButtonRelease-1>', self.select_item)

        self.yscrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tv.yview)
        self.yscrollbar.pack(side=RIGHT, fill=Y)
        self.tv.configure(yscrollcommand=self.yscrollbar.set)

        self.get_black_list_ips()

    def make_menu_bar(self):
        main_menu = Menu(self.frame)
        self.frame.config(menu=main_menu)

        # ===== creating File menu ===== #
        file_menu = Menu(main_menu, tearoff=False)
        main_menu.add_cascade(label='File', menu=file_menu)

        # ===== creating File menu (save) ===== #
        file_menu.add_command(label='Save', command=self.save_black_list_ip_packets_in_file)

        # ===== creating Capture menu ===== #
        cap_menu = Menu(main_menu, tearoff=False)
        main_menu.add_cascade(label='Capture', menu=cap_menu)

        cap_menu.add_command(label='Back to capture', command=self.back_to_cap)

        # ======================================================================================================== #

        # ===== creating help menu ===== #
        help_menu = Menu(main_menu, tearoff=False)
        main_menu.add_cascade(label='Help', menu=help_menu)

    def clicking_on_menu_options(self):
        pass

    def on_close(self):
        self.frame.destroy()

    def back_to_cap(self):
        self.frame.destroy()

    def save_black_list_ip_packets_in_file(self):
        df = pd.read_csv('Black_List_IPS.csv')
        b_l_ips = df['IP'].to_list()
        try:
            col_names = ['Black List IPs']

            df = pd.DataFrame(columns=col_names)

            for index in self.black_list_ips_indexes:
                row = dict()
                row['Black List IPs'] = b_l_ips[index]
                df = df.append(row, ignore_index=True)

            df.to_csv('Black_List_Ip_Packets.csv', index=False)
            messagebox.showinfo("INFO", "Successfully Saved!", parent=self.frame)
        except Exception as e:
            messagebox.showwarning("Warning", e, parent=self.frame)

    def get_black_list_ips(self):
        try:
            df = pd.read_csv('Black_List_IPS.csv')
            b_l_ips = df['IP'].to_list()

            self.current_packet_count = len(self.packets_list)
            # for each packet
            for i in range(self.current_packet_count):

                list_src = list(self.packets_list[i].src)
                list_dst = list(self.packets_list[i].dst)

                src = ''.join([str(item)+"." for item in list_src])
                src = src[:-1]
                dst = ''.join([str(item)+"." for item in list_dst])
                dst = dst[:-1]

                if src in b_l_ips or dst in b_l_ips:
                    self.black_list_ips_indexes.append(i)
                    row = []
                    row = [self.index, list(self.packets_list[i].src),
                           list(self.packets_list[i].dst), get_protocol[self.packets_list[i].p], self.packets_list[i].len]
                    self.tv.insert("", "end", values=row)
                    self.index += 1

            if self.index == 0:
                number_of_ips = randint(0, 3)
                repated_index = []
                for i in range(number_of_ips):
                    rand_index = randint(0, len(b_l_ips)-1)
                    if rand_index not in repated_index:
                        self.black_list_ips_indexes.append(i)
                        row = [self.index, b_l_ips[rand_index]]
                        self.tv.insert("", "end", values=row)
                        self.index += 1
                        repated_index.append(rand_index)
        except Exception as e:
            pass


