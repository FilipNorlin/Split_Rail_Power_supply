Vref = 0.6
Vin = 12
Vout = 5
fsw = 500e3
Iout = 3
k = 0.3

# Components

R_fbb = 4.7e3
L = 6.8e-6
C_out = 47e-6
C_out_ESR = 20e-3

# Feedback

R_fbt = ((Vout - Vref) / Vref) * R_fbb
R_fbt = 34e3

# Inductor

L_min = (Vin - Vout) / (Iout * k) * (Vout / (Vin * fsw))
I_L_delta = (Vout * (Vin - Vout)) / (Vin * L_min * fsw)

# Output Capacitor

Vout_delta_ESR = I_L_delta * C_out_ESR
Vout_delta = I_L_delta / (8 * fsw * C_out)

Vout = Vref * (1 + (R_fbt / R_fbb))

# Printout

print(f"Input Voltage: {Vin}V")
print(f"Output Voltage: {round(Vout, 3)}V")
print(f"Output current: {Iout}A")
print(f"FB resistors: {round(R_fbt, 3)}, {round(R_fbb, 3)}")
print()

print(f"Inductor min: {round(L_min * 10**6, 3)}uH")
print(f"Current ripple: {round(I_L_delta, 3)}A")
print(f"Voltage ripple: {round(Vout_delta, 3)}")
print(f"Voltage ripple (ESR): {round(Vout_delta_ESR, 3)}")