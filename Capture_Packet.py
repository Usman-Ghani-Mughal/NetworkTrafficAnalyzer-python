# from tkinter import*
# import tkinter as tk
# from tkinter import ttk
# import pcap
# import dpkt
# import time
# from PIL import ImageTk
# from all_const_strings import *
# from protocols_and_numbers import *
# import threading

from ShowGraph import*
import pandas as pd
from CheckBlackListIP import *


class CapturePacket:
    def __init__(self, toplevel1, root1, root0 ):
        self.root0 = root0
        self.root1 = root1
        self.frame = toplevel1

        self.icon = PhotoImage(file=capture_icon_path)
        self.frame.title(capture_title)
        self.frame.iconphoto(False, self.icon)

        self.tv = None
        self.index = 1
        self.listbox = None
        self.yscrollbar = None
        self.y_d_scrollbar = None
        self.packets_list = []
        self.cap_thread = None
        # ================================ Packet Info Items ========================================== #
        self.packets_src = None
        self.packets_dst = None
        self.packets_protocol = None
        self.packets_length = None
        self.packets_sum = None
        self.packets_ttl = None
        self.packets_offset = None
        self.packets_df = None
        self.packets_mk = None
        self.packets_off = None
        self.packets_df = None
        self.packets_data = None
        self.packets_hl = None
        self.packets_rf = None
        self.packets_sp = None
        self.packets_dp = None
        self.packets_sizeof = None
        self.packets_version = None
        # ============================================================================================= #

        # ===== Add close protocol ===== #
        self.frame.protocol("WM_DELETE_WINDOW", self.on_close)
        self.frame.title("Capturing Packets")
        self.sniffer = pcap.pcap(name=None, promisc=False, timeout_ms=50)
        # ============================================================================================= #
        self.tv = ttk.Treeview(self.frame, columns=(1, 2, 3, 4, 5, 6, 7), show="headings", height="10",
                               selectmode='browse')
        self.tv.pack(side=LEFT)
        self.tv.place(x=0, y=0)
        self.tv.heading(1, text="No.")
        self.tv.heading(2, text="Time")
        self.tv.heading(3, text="Source")
        self.tv.heading(4, text="Destination")
        self.tv.heading(5, text="Protocol")
        self.tv.heading(6, text="Length")
        self.tv.heading(7, text="CheckSum")
        self.tv.bind('<ButtonRelease-1>', self.select_item)

        self.yscrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tv.yview)
        self.yscrollbar.pack(side=RIGHT, fill=Y)
        self.tv.configure(yscrollcommand=self.yscrollbar.set)
        # ============================================================================================= #
        # ======== Adding menu Bar ======= #
        self.make_menu_bar()

        # ======== Adding items on Frame ======= #
        self.add_items_onframe()

    def on_close(self):
        self.root1.destroy()
        self.root0.destroy()

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
        file_menu.add_command(label='Save', command=self.save_packets)

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
        analyse_menu.add_command(label='show stats', command=self.show_graph)
        analyse_menu.add_command(label='show Black List IPs', command=self.show_black_list_ip)

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

    def show_graph(self):
        toplevel2 = Toplevel(self.frame)
        # self.root.withdraw()
        toplevel2.geometry("1200x885+100+50")
        toplevel2.resizable(False, False)
        show_graph_obj = ShowGraph(self.packets_list, toplevel2, self.frame, self.root0, self.root1)

    def show_black_list_ip(self):
        toplevel2 = Toplevel(self.frame)
        # self.root.withdraw()
        toplevel2.geometry("400x250+100+50")
        toplevel2.resizable(False, False)
        show_black_list_obj = CheckBlackListIP(self.packets_list, toplevel2, self.frame, self.root0, self.root1)

    def start_sniffing(self):
        # sniffer = pcap.pcap(name=None, promisc=False, timeout_ms=50)
        try:
            for t_s, r_b in self.sniffer:
                eth = dpkt.ethernet.Ethernet(r_b)
                if not isinstance(eth.data, dpkt.ip.IP):
                    print("Non Ip packet type not supported")
                    continue
                packet = eth.data
                # Storing Packet in a LIST
                self.packets_list.append(packet)

                row = []
                row = [self.index, "".join(time.strftime("%y-%m-%d %H:%M:%S", (time.localtime(t_s)))), list(packet.src),
                       list(packet.dst), get_protocol[packet.p], packet.len, packet.sum]
                self.tv.insert("", "end", values=row)
                self.index += 1
                break
            self.tv.after(100, self.start_sniffing)
        except Exception as e:
            messagebox.showerror("Error", "There is some error in sniffing packet")

    def select_item(self, a):
        try:
            print("Select Item")
            row_value = self.tv.item(self.tv.selection())
            row_index = row_value['values'][0]
            # <*> =========-------========= Packet Info Area =========--------============ <*>
            # ========================================================================================================== #
            #              ----------------------------------- ROW 1 -----------------------------------
            # ========================================================================================================== #

            # ------------ SRC ------------- #
            self.packets_src.config(text=list(self.packets_list[row_index - 1].src))

            # ------------ DST ------------- #
            self.packets_dst.config(text=list(self.packets_list[row_index - 1].dst))

            # ------------ Protocol ------------- #
            self.packets_protocol.config(text=get_protocol[self.packets_list[row_index - 1].p])

            # ------------ Length ------------- #
            self.packets_length.config(text=self.packets_list[row_index - 1].len)

            # ========================================================================================================== #
            #              ----------------------------------- ROW 2 -----------------------------------
            # ========================================================================================================== #

            # ------------ CHECK SUM ------------- #
            self.packets_sum.config(text=self.packets_list[row_index - 1].sum)

            # ------------ ttl ------------- #
            self.packets_ttl.config(text=self.packets_list[row_index - 1].ttl)

            # ------------ OFF SET ------------- #
            # Finding Offset
            offset = self.packets_list[row_index - 1].off & dpkt.ip.IP_OFFMASK
            # setting offset
            self.packets_offset.config(text=offset)

            # ------------ OFF ------------- #
            self.packets_off.config(text=self.packets_list[row_index - 1].off)

            # ========================================================================================================== #
            #              ----------------------------------- ROW 3 -----------------------------------
            # ========================================================================================================== #

            # Finding DF and MK
            df = bool(self.packets_list[row_index - 1].off & dpkt.ip.IP_DF)
            mf = bool(self.packets_list[row_index - 1].off & dpkt.ip.IP_MF)

            # ------------ DF ------------- #
            self.packets_df.config(text=df)

            # ------------MK ------------- #
            self.packets_mk.config(text=mf)

            # ------------ HL ------------- #
            self.packets_hl.config(text=self.packets_list[row_index - 1].hl)

            # ------------ RF ------------- #
            self.packets_rf.config(text=self.packets_list[row_index - 1].rf)

            # ========================================================================================================== #
            #              ----------------------------------- ROW 4 -----------------------------------
            # ========================================================================================================== #

            # ------------ Sport ------------- #
            self.packets_sp.config(text=list(self.packets_list[row_index - 1].data)[0][1])
            # list(packet.data)[0][1])
            # ------------D-port ------------- #
            self.packets_dp.config(text=list(self.packets_list[row_index - 1].data)[1][1])

            # ------------ Sizeof ------------- #
            self.packets_sizeof.config(text=self.packets_list[row_index - 1].__sizeof__())

            # ------------ version ------------- #
            self.packets_version.config(text=self.packets_list[row_index - 1].v)

            # <*> --------------------------------- Packet Data Area ---------------------------------- <*>
            self.packets_data.config(text=self.packets_list[row_index - 1].data)
        except Exception as e:
            messagebox.showerror("Error", "There is some error in selecting row")

    def add_items_onframe(self):
        self.cap_thread = threading.Thread(target=self.start_sniffing)
        self.cap_thread.start()
        # ============================================================================================= #
        # <*> =========-------========= Packet Info Area =========--------============ <*>

        # ========================================================================================================== #
        #              ----------------------------------- ROW 1 -----------------------------------
        # ========================================================================================================== #

        # ------------ SRC Labels ------------- #
        src_label = Label(self.frame, text="SRC: ", font=(rockwell, 12, "bold"), fg=white, bg=dark_blue)
        src_label.place(x=120, y=235)
        self.packets_src = Label(self.frame, font=(rockwell, 12), bg=dark_blue, fg=white)
        self.packets_src.place(x=171, y=235, width=150, height=25)

        # ------------ DST labels ------------- #
        dst_label = Label(self.frame, text="DST: ", font=(rockwell, 12, "bold"), fg=white, bg=dark_blue)
        dst_label.place(x=340, y=235)
        self.packets_dst = Label(self.frame, font=(rockwell, 12), bg=dark_blue, fg=white)
        self.packets_dst.place(x=390, y=235, width=150, height=25)

        # ------------ Protocol Labels ------------- #
        protocol_label = Label(self.frame, text="Protocol: ", font=(rockwell, 12, "bold"), fg=white, bg=dark_blue)
        protocol_label.place(x=560, y=235)
        self.packets_protocol = Label(self.frame, font=(rockwell, 12), bg=dark_blue, fg=white)
        self.packets_protocol.place(x=643, y=235, width=150, height=25)

        # ------------ Length ------------- #
        pk_len_label = Label(self.frame, text="Length: ", font=(rockwell, 12, "bold"), fg=white, bg=dark_blue)
        pk_len_label.place(x=810, y=235)
        self.packets_length = Label(self.frame, font=(rockwell, 12), bg=dark_blue, fg=white)
        self.packets_length.place(x=882, y=235, width=151, height=25)

        # ========================================================================================================== #
        #              ----------------------------------- ROW 2 -----------------------------------
        # ========================================================================================================== #

        # ------------ CHECK SUM ------------- #
        sum_label = Label(self.frame, text="SUM: ", font=(rockwell, 12, "bold"), fg=white, bg=dark_blue)
        sum_label.place(x=120, y=280)
        self.packets_sum = Label(self.frame, font=(rockwell, 12), bg=dark_blue, fg=white)
        self.packets_sum.place(x=174, y=280, width=150, height=25)

        # ------------ ttl ------------- #
        ttl_label = Label(self.frame, text="TTL: ", font=(rockwell, 12, "bold"), fg=white, bg=dark_blue)
        ttl_label.place(x=340, y=280)
        self.packets_ttl = Label(self.frame, font=(rockwell, 12), bg=dark_blue, fg=white)
        self.packets_ttl.place(x=389, y=280, width=151, height=25)

        # ------------ OFF SET ------------- #
        offset_label = Label(self.frame, text="OFFSET: ", font=(rockwell, 12, "bold"), fg=white, bg=dark_blue)
        offset_label.place(x=560, y=280)
        self.packets_offset = Label(self.frame, font=(rockwell, 12), bg=dark_blue, fg=white)
        self.packets_offset.place(x=642, y=280, width=151, height=25)

        # ------------ OFF ------------- #
        off_label = Label(self.frame, text="OFF: ", font=(rockwell, 12, "bold"), fg=white, bg=dark_blue)
        off_label.place(x=810, y=280)
        self.packets_off = Label(self.frame, font=(rockwell, 12), bg=dark_blue, fg=white)
        self.packets_off.place(x=861, y=280, width=170, height=25)

        # ========================================================================================================== #
        #              ----------------------------------- ROW 3 -----------------------------------
        # ========================================================================================================== #

        # ------------ DF ------------- #
        df_label = Label(self.frame, text="DF: ", font=(rockwell, 12, "bold"), fg=white, bg=dark_blue)
        df_label.place(x=120, y=325)
        self.packets_df = Label(self.frame, font=(rockwell, 12), bg=dark_blue, fg=white)
        self.packets_df.place(x=160, y=325, width=165, height=25)

        # ------------MK ------------- #
        mk_label = Label(self.frame, text="MK: ", font=(rockwell, 12, "bold"), fg=white, bg=dark_blue)
        mk_label.place(x=340, y=325)
        self.packets_mk = Label(self.frame, font=(rockwell, 12), bg=dark_blue, fg=white)
        self.packets_mk.place(x=387, y=325, width=152, height=25)

        # ------------ HL ------------- #
        hl_label = Label(self.frame, text="HL: ", font=(rockwell, 12, "bold"), fg=white, bg=dark_blue)
        hl_label.place(x=560, y=325)
        self.packets_hl = Label(self.frame, font=(rockwell, 12), bg=dark_blue, fg=white)
        self.packets_hl.place(x=599, y=325, width=192, height=25)

        # ------------RF ------------- #
        rf_label = Label(self.frame, text="RF: ", font=(rockwell, 12, "bold"), fg=white, bg=dark_blue)
        rf_label.place(x=810, y=325)
        self.packets_rf = Label(self.frame, font=(rockwell, 12), bg=dark_blue, fg=white)
        self.packets_rf.place(x=849, y=325, width=182, height=25)

        # ========================================================================================================== #
        #              ----------------------------------- ROW 4 -----------------------------------
        # ========================================================================================================== #

        # ------------ SPORT ------------- #
        sp_label = Label(self.frame, text="SPORT: ", font=(rockwell, 12, "bold"), fg=white, bg=dark_blue)
        sp_label.place(x=120, y=370)
        self.packets_sp = Label(self.frame, font=(rockwell, 12), bg=dark_blue, fg=white)
        self.packets_sp.place(x=194, y=370, width=131, height=25)

        # ------------D-PORT ------------- #
        dp_label = Label(self.frame, text="DPORT: ", font=(rockwell, 12, "bold"), fg=white, bg=dark_blue)
        dp_label.place(x=340, y=370)
        self.packets_dp = Label(self.frame, font=(rockwell, 12), bg=dark_blue, fg=white)
        self.packets_dp.place(x=418, y=370, width=121, height=25)

        # ------------ Sizeof ------------- #
        sizeof_label = Label(self.frame, text="Sizeof: ", font=(rockwell, 12, "bold"), fg=white, bg=dark_blue)
        sizeof_label.place(x=560, y=370)
        self.packets_sizeof = Label(self.frame, font=(rockwell, 12), bg=dark_blue, fg=white)
        self.packets_sizeof.place(x=625, y=370, width=170, height=25)

        # ------------ version ------------- #
        version_label = Label(self.frame, text="Version: ", font=(rockwell, 12, "bold"), fg=white, bg=dark_blue)
        version_label.place(x=810, y=370)
        self.packets_version = Label(self.frame, font=(rockwell, 12), bg=dark_blue, fg=white)
        self.packets_version.place(x=887, y=370, width=146, height=25)

        # <*> --------------------------------- Packet Data Area ---------------------------------- <*>
        data_label = Label(self.frame, text="Packet-Data", font=(rockwell, 14, "bold"), fg=dark_blue, bg=white)
        data_label.place(x=10, y=400)
        self.packets_data = Message(self.frame, font=(rockwell, 14), bg=login_i_f_color)
        self.packets_data.place(x=10, y=430, width=1160, height=110)
        # 1160
        # <> ===================================== Start Sniffing  =========================================== <> #

    def store_packets_in_file(self):
        try:
            col_names = ['SRC_IP', 'DST_IP', 'Protocol', 'Length', 'Check_SUM', 'TTL', 'OFFSET', 'OFF', 'DF', 'MK',
                         'HL', 'RF',
                         'SRC_PORT', 'DST_PORT', 'Sizeof', 'Version', 'Data']
            df = pd.DataFrame(columns=col_names)
            for packet in self.packets_list:
                row = dict()
                row['SRC_IP'] = list(packet.src)
                row['DST_IP'] = list(packet.dst)
                row['Protocol'] = packet.p
                row['Length'] = packet.len
                row['Check_SUM'] = packet.sum
                row['TTL'] = packet.ttl
                row['OFFSET'] = packet.off & dpkt.ip.IP_OFFMASK
                row['OFF'] = packet.off
                row['DF'] = packet.off & dpkt.ip.IP_DF
                row['MK'] = packet.off & dpkt.ip.IP_MF
                row['HL'] = packet.hl
                row['RF'] = packet.rf
                row['SRC_PORT'] = list(packet.data)[0][1]
                row['DST_PORT'] = list(packet.data)[1][1]
                row['Sizeof'] = packet.__sizeof__()
                row['Version'] = packet.v
                row['Data'] = packet.data

                df = df.append(row, ignore_index=True)
            df.to_csv('Packets.csv', index=False)
            messagebox.showinfo("INFO", "Successfully Saved!", parent=self.frame)
        except Exception as e:
            messagebox.showwarning("Warning", e, parent=self.frame)

    def save_packets(self):
        self.save_thread = threading.Thread(target=self.store_packets_in_file)
        self.save_thread.start()








