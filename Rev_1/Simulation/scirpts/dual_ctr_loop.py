import control as ct
import numpy as np
import matplotlib.pyplot as plt

# -------------------
# Converter
# -------------------

plot_folder = "dual_converter/"

Vin = 325
n = 1.3

L = 220e-6
C = 10000e-6
R = 10

# Plant:
# Duty → Current

Gid = ct.tf(
    [n*Vin],
    [L, 0]
)

print("Inner plant:")
print(Gid)

# -------------------
# Current PI
# -------------------

Kpi = 0.1
Kii = 2000

Gci = ct.tf(
    [Kpi, Kii],
    [1, 0]
)

# Closed current loop
Ti = ct.feedback(
    Gci * Gid,
    1
)

print("\nCurrent loop poles:")
print(ct.poles(Ti))

# Plot current-loop step response

plt.figure()

t, y = ct.step_response(Ti)

plt.plot(t, y)

plt.title("Inner Current Loop")

plt.xlabel("Time (s)")
plt.ylabel("Current")

plt.grid()

plt.savefig(plot_folder + "Inner_Current_Loop.png")
#plt.show()

# Plot current-loop poles

p = ct.poles(Ti)

plt.figure()

plt.axvline(0)

plt.axhline(0)

plt.scatter(
    p.real,
    p.imag,
    s=150
)

plt.xlabel("Real")

plt.ylabel("Imaginary")

plt.title("Current Loop Poles")

plt.grid()

plt.savefig(plot_folder + "Current_Loop_Poles.png")
#plt.show()

# Build outer voltage plant

Gv = ct.tf(
    [R],
    [R*C, 1]
)

# Actual outer plant:
Gouter = Ti * Gv

# Add outer voltage PI

Kpv = 1.8
Kiv = 45

Gcv = ct.tf(
    [Kpv, Kiv],
    [1, 0]
)

Tv = ct.feedback(
    Gcv * Gouter,
    1
)

print("\nVoltage loop poles:")
print(ct.poles(Tv))

# Plot output voltage response

plt.figure()

t, y = ct.step_response(Tv)

plt.plot(t, y)

plt.title("Complete Converter Closed Loop")

plt.xlabel("Time (s)")
plt.ylabel("Voltage")

plt.grid()
plt.savefig(plot_folder + "Complete_Converter_Closed_Loop.png")
#plt.show()

# Bode plot

ct.bode_plot(
    Tv,
    dB=True,
    margins=True
)

plt.savefig(plot_folder + "Bode_plot.png")
#plt.show()

# Extract metrics automatically

info = ct.step_info(Tv)

print("\n------- Voltage Loop -------\n")

for key, value in info.items():
    print(key, ":", value)

info = ct.step_info(Ti)

print("\n------- Current Loop -------\n")

for key, value in info.items():
    print(key, ":", value)


# Time Domain

v_ref = 140

t = np.linspace(
    0,
    0.250,
    10000
)

u = np.ones_like(t)*v_ref

t, y = ct.forced_response(
    Tv,
    T=t,
    U=u
)

plt.figure()
plt.plot(
    t,
    y
)
plt.grid()

plt.savefig(plot_folder + "Time_Domain.png")
#plt.show()