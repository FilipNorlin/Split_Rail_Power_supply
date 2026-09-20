import numpy as np
import matplotlib.pyplot as plt
from NTC import NTC

ntc_mosfet = NTC([28.7e3, 4.10e3, 987], [0, 50, 100])
ntc_diodes = NTC([28.7e3, 4.10e3, 987], [0, 50, 100])
ntc_board = NTC([28.88e3, 10e3, 4.16e3], [0, 25, 50])

Vcc = 3.3
R1 = 3.3e3
t_min = 0
t_max = 150

temp_lst = []

ntc_mosfet_res_lst = []
ntc_diode_res_lst = []
ntc_board_res_lst = []

vout_div_mosfet = []
vout_div_diode = []
vout_div_board = []

for t in range(t_min, t_max):
    ntc_mosfet.set_temperature(t)
    ntc_diodes.set_temperature(t)
    ntc_board.set_temperature(t)

    R_ntc_mosfet = ntc_mosfet.get_resistance()
    R_ntc_diode = ntc_diodes.get_resistance()
    R_ntc_board = ntc_board.get_resistance()

    ntc_mosfet_res_lst.append(R_ntc_mosfet)
    ntc_diode_res_lst.append(R_ntc_diode)
    ntc_board_res_lst.append(R_ntc_board)

    vout_div_mosfet.append((Vcc * (R_ntc_mosfet / (R_ntc_mosfet + R1))))
    vout_div_diode.append((Vcc * (R_ntc_diode / (R_ntc_diode + R1))))
    vout_div_board.append((Vcc * (R_ntc_board / (R_ntc_board + R1))))
    temp_lst.append(t)


plt.figure()
plt.plot(temp_lst, vout_div_mosfet, label="MOSFET")
plt.plot(temp_lst, vout_div_diode, label="DIODE")
plt.plot(temp_lst, vout_div_board, label="BOARD")
plt.title("Voltage out")
plt.xlabel("Temp (°C)")
plt.ylabel("Voltage (V)")
plt.legend()
plt.grid()
#plt.savefig(plot_folder + "Complete_Converter_Closed_Loop.png")
plt.show()
