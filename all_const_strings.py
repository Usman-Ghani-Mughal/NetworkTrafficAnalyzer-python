# ============================= Colors ======================================= #
frame_bg_color = "#A9CCE3"
dark_blue = "#1A5276"
interface_bg_color = "#113D65"
menu_bar_color = "#FDFEFE"
cap_packet_bg = "#0671C4"
reg_bg_color = "#013C77"
white = "#FDFEFE"
login_i_f_color = "#D6EAF8"
reg_i_f_color = "#005FA1"
red = "#FF0000"

# ============================= Fonts ======================================= #
comic_sans_ms = "Comic Sans MS"
rockwell = "Rockwell"

# ============================= Icons Paths ======================================= #
login_icon_path = "images\\Icons\\login_icon.png"
registration_icon_path = "images\\Icons\\register_icon.png"
interface_icon_path = "images\\Icons\\network_icon.png"
capture_icon_path = "images\\Icons\\capture_packets_icon.png"

# ============================= Background images Paths ======================================= #
Login_bg_path = "images\\BackGrounds\\login_BG.jpg"
registration_bg_path = "images\\BackGrounds\\register_BG.jpg"
interface_bg_path = "images\\BackGrounds\\interface_BG.jpeg"

# ============================= Const Strings ======================================= #

# Titles
login_title = "Login"
registration_title = "Registration"
capture_title = "Capturing Packets"
interface_title = "Interface Selection"
show_graph_title = "Graphs"

# Geometries of frames
login_geometry = "1199x550+100+50"
registration_geometry = "1199x550+100+50"


# ============================= Queries ======================================= #

user_register_query = """INSERT INTO Users (username, email, password) VALUES ('{}', '{}', '{}') """

# ============================= DataBase Info ======================================= #
DB_NAME = "Network_traffic.db"

python_path_ = "C:\\Users\\usman\\OneDrive\\Desktop\\Network_Trafic_analysier\\NetworkTraficAnalyser\\venv\\Scripts\\python"
spider_path_ = "C:\\Users\\usman\\OneDrive\\Desktop\\Network_Trafic_analysier\\NetworkTraficAnalyser\\BlackListSpider.py"
