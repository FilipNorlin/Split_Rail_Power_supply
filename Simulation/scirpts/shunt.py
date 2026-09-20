import numpy as np

V1 = 325
R_shunt = 20e-3
Av = 50
Av2 = 2/3
Vcc = 5

for I in np.arange(0.0, 10.0, 0.1):
    V_shunt = I * (R_shunt / 2)

    V_out = V_shunt * Av * Av2
    V_real = V_out
    P_shunt = (R_shunt * I**2) * 0.2

    P = V1 * I

    if V_real > Vcc:
        V_real = Vcc
      
    print(f"Current: {round(I, 3)},  Shunt Voltage: {round(V_shunt, 3)},  Voltage out: {round(V_out, 3)},  Shunt Powerloss: {round(P_shunt, 3)},  Power: {round(P, 3)}")
