import numpy as np
import matplotlib.pyplot as plt


# -----------------------
# Parameters
# -----------------------

V_rms = 230
V_pk = np.sqrt(2) * V_rms
f_line = 50

L = 1e-3
C = 680e-6
R = 50

fs = 10e3
T = 1 / fs

D = 0.8
phase_shift = 0.5

# Simulation timestep
dt = 500e-9

# Simulate several line cycles
line_period = 1 / f_line
switch_perdiod = 1 / fs
t_start = 1
t_end = t_start + 5 * switch_perdiod

steps = int(t_end / dt)


# -----------------------
# States
# -----------------------

i_la = 0.0
i_lb = 0.0
v_out = 0.0


# -----------------------
# Storage
# -----------------------

t_arr = []

i_la_arr = []
i_lb_arr = []

i_in_arr = []
v_in_arr = []

v_out_arr = []

qa_arr = []
qb_arr = []


# -----------------------
# Simulation
# -----------------------

for k in range(steps):

    t = k * dt

    # -----------------------
    # Rectified mains voltage
    # -----------------------

    v_in = V_pk * abs(np.sin(2 * np.pi * f_line * t))

    v_in = 5


    # -----------------------
    # PWM phase A
    # -----------------------

    pwm_time = t % T
    qa = 1.0 if pwm_time < D * T else 0.0

    # -----------------------
    # PWM phase B
    # -----------------------

    phase_b_time = (pwm_time - phase_shift * T) % T
    qb = 1.0 if phase_b_time < D * T else 0.0

    # -----------------------
    # Inductor A
    # -----------------------

    if qa:
        di_la = v_in / L
    else:
        di_la = (v_in - v_out) / L

    # -----------------------
    # Inductor B
    # -----------------------

    if qb:
        di_lb = v_in / L
    else:
        di_lb = (v_in - v_out) / L

    # -----------------------
    # Current delivered
    # to output
    # -----------------------

    if qa:
        i_out_a = 0.0
    else:
        i_out_a = i_la

    if qb:
        i_out_b = 0.0
    else:
        i_out_b = i_lb

    # -----------------------
    # Capacitor
    # -----------------------

    i_out = i_out_a + i_out_b
    dv_out = (i_out - v_out / R) / C


    # -----------------------
    # Input current
    # -----------------------

    i_in = i_la + i_lb

    # -----------------------
    # Euler integration
    # -----------------------

    i_la += di_la * dt
    i_lb += di_lb * dt
    v_out += dv_out * dt

    # -----------------------
    # Store
    # -----------------------

    if t >= t_start:
        t_arr.append(t)
        i_la_arr.append(i_la)
        i_lb_arr.append(i_lb)
        i_in_arr.append(i_in)
        v_in_arr.append(v_in)
        v_out_arr.append(v_out)
        qa_arr.append(qa)
        qb_arr.append(qb)

# -----------------------
# Convert to arrays
# -----------------------

t_arr = np.array(t_arr)

i_la_arr = np.array(i_la_arr)
i_lb_arr = np.array(i_lb_arr)

i_in_arr = np.array(i_in_arr)

v_in_arr = np.array(v_in_arr)
v_out_arr = np.array(v_out_arr)

qa_arr = np.array(qa_arr)
qb_arr = np.array(qb_arr)

# -----------------------
# Plot
# -----------------------

plt.figure()

plt.subplot(5, 1, 1)
plt.plot(t_arr * 1000, v_in_arr)
plt.ylabel("Vin (V)")
plt.grid()

plt.subplot(5, 1, 2)
plt.plot(t_arr * 1000, v_out_arr)
plt.ylabel("Vout (V)")
plt.grid()

plt.subplot(5, 1, 3)
plt.plot(t_arr * 1000, i_la_arr)
plt.plot(t_arr * 1000, i_lb_arr)
plt.ylabel("Inductor (A)")
plt.legend(["iLA", "iLB"])
plt.grid()

plt.subplot(5, 1, 4)
plt.plot(t_arr * 1000, i_in_arr)
plt.ylabel("Iin (A)")
plt.grid()

plt.subplot(5, 1, 5)
plt.plot(t_arr * 1000, qa_arr)
plt.plot(t_arr * 1000, qb_arr)
plt.ylabel("PWM")
plt.xlabel("Time (ms)")
plt.legend(["QA", "QB"])
plt.grid()

plt.tight_layout()

plt.savefig("interleaved_pfc.png", dpi=300)

plt.show()