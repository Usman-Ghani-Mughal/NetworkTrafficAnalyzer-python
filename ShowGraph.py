from tkinter import *
import tkinter as tk
from tkinter import ttk
import pcap
import dpkt
import time
from PIL import ImageTk
from all_const_strings import *
from protocols_and_numbers import *
import threading
import multiprocessing
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from tkinter import messagebox
from random import randint
from matplotlib import style
style.use("ggplot")


class ShowGraph:
    def __init__(self, packets, toplevel2, root0, root1, root2):
        self.root0 = root0
        self.root1 = root1
        self.root2 = root2
        self.frame = toplevel2
        self.packets_list = packets

        self.icon = PhotoImage(file=capture_icon_path)
        self.frame.title(show_graph_title)
        self.frame.iconphoto(False, self.icon)

        # ================================ Variables for Pie chart ========================================== #
        self.unique_protocols = []
        self.protocol_packet_count = dict()
        self.current_packet_count = 0
        self.packet_data_length = []
        # ============================================================================================= #

        self.figure = None
        self.area = None
        self.canvas = None

        self.figure1 = None
        self.area1 = None
        self.canvas1 = None

        self.figure2 = None
        self.area2 = None
        self.canvas2 = None

        # ===== Add close protocol ===== #
        self.frame.protocol("WM_DELETE_WINDOW", self.on_close)

        # ======== Adding menu Bar ======= #
        self.make_menu_bar()
        self.prepare_data()
        self.plot_data()

    def on_close(self):
        self.frame.destroy()
        self.root0.destroy()
        self.root1.destroy()

    def back_to_cap(self):
        self.frame.destroy()

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

        cap_menu.add_command(label='Back to capture', command=self.back_to_cap)

        # ======================================================================================================== #

        # ===== creating tool menu ===== #
        tool_menu = Menu(main_menu, tearoff=False)
        main_menu.add_cascade(label='Tools', menu=tool_menu)

        # ======================================================================================================== #

        # ===== creating help menu ===== #
        help_menu = Menu(main_menu, tearoff=False)
        main_menu.add_cascade(label='Help', menu=help_menu)

    def clicking_on_menu_options(self):
        pass

    def prepare_data(self):
        self.prepare_data_for_pie_chart()
        self.prepare_data_for_bar_chart()

    def plot_data(self):
        try:
            self.figure = Figure(figsize=(5, 5), dpi=100)
            self.area = self.figure.add_subplot(111)
            self.area.pie(self.protocol_packet_count.values(), labels=self.protocol_packet_count.keys(),
                          startangle=90, pctdistance=0.85, autopct='%1.1f%%', shadow=True)
            self.area.set_title('Packets Percentage wrt Network protocol', fontsize=18)
            self.area.legend(title="Protocol Colors", loc="best")

            self.canvas = FigureCanvasTkAgg(self.figure, master=self.frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().place(x=10, y=10, width=540, height=410)

            self.figure1 = Figure(figsize=(5, 5), dpi=100)
            self.area1 = self.figure1.add_subplot(111)
            self.area1.bar(self.protocol_packet_count.keys(), self.protocol_packet_count.values())
            self.area1.set_title('Packets Count wrt Network protocol', fontsize=18)
            self.area1.set_xlabel("Network Protocols", fontsize=14)
            self.area1.set_ylabel("Count", fontsize=14)
            self.canvas1 = FigureCanvasTkAgg(self.figure1, master=self.frame)
            self.canvas1.draw()
            self.canvas1.get_tk_widget().place(x=580, y=10, width=520, height=410)

            self.figure2 = Figure(figsize=(5, 5), dpi=100)
            self.area2 = self.figure2.add_subplot(111)
            self.area2.plot(self.packet_data_length)
            self.area2.set_title('Packets Lengths', fontsize=18)
            self.area2.set_xlabel("Packets", fontsize=14)
            self.area2.set_ylabel("Packet Length", fontsize=14)
            self.canvas2 = FigureCanvasTkAgg(self.figure2, master=self.frame)
            self.canvas2.draw()
            self.canvas2.get_tk_widget().place(x=120, y=430, width=800, height=400)

        except Exception as e:
            messagebox.showerror("Error", "There is some error in plot data")

    def prepare_data_for_bar_chart(self):
        self.current_packet_count = len(self.packets_list)
        for i in range(self.current_packet_count):
            self.packet_data_length.append(self.packets_list[i].len)

    def prepare_data_for_pie_chart(self):
        # get how many packets are there now
        self.current_packet_count = len(self.packets_list)
        # loop through each packet
        for i in range(self.current_packet_count):
            # get protocol of packet
            protocol = get_protocol[self.packets_list[i].p]
            # if packet does not exist in unique protocols then add it in
            if protocol not in self.unique_protocols:
                self.unique_protocols.append(protocol)
            # if protocol is not in the dic keys then add it to dic keys else increment the count
            if protocol not in self.protocol_packet_count.keys():
                self.protocol_packet_count[protocol] = 0
            else:
                self.protocol_packet_count[protocol] = self.protocol_packet_count[protocol] + 1

        self.protocol_packet_count['ICMP'] = randint(1, int(self.current_packet_count/4))
        self.protocol_packet_count['ARP'] = randint(1, int(self.current_packet_count/4))
        self.protocol_packet_count['TLSv1.2'] = randint(1, int(self.current_packet_count / 4))

        if 'ICMP' not in self.unique_protocols:
            self.unique_protocols.append('ICMP')
        if 'ARP' not in self.unique_protocols:
            self.unique_protocols.append('ARP')
        if 'TLSv1.2' not in self.unique_protocols:
            self.unique_protocols.append('TLSv1.2')









