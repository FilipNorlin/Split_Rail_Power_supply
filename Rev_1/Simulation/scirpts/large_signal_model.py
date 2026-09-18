import numpy as np
import matplotlib.pyplot as plt

# -----------------------
# Parameters
# -----------------------
Vin = 325
n = 1.3
L = 220e-6
C = 470e-6
R = 10
Lm = 2e-3

fs = 100e3
T = 1/fs
D = 0.33

period_samples = 10
p = 0
dt = 50e-9                  # << MUST be much smaller than switching period
t_start = 0
t_end = t_start + period_samples*T + 40e-3
ss = False

steps = int(t_end / dt)

print(T)

# -----------------------
# States
# -----------------------
iL = 0.0
vC = 0.0
im = 0.0

# storage
t_arr = []
iL_arr = []
vC_arr = []
iC_arr_temp = []
iC_arr = []
im_arr = []
q_arr = []

proc = 0
steady_state = False
steady_state_arr = []
period = 0

# -----------------------
# Simulation loop
# -----------------------
for k in range(steps):
    t = k * dt

    # PWM
    q = 1.0 if (t % T) < D * T else 0.0

    # -----------------------
    # ON state (q = 1)
    # -----------------------
    if q > 0.5:
        diL = (n * Vin - vC) / L
        dvC = (iL - vC / R) / C
        dim = Vin / Lm

    # -----------------------
    # OFF state (q = 0)
    # -----------------------
    else:
        diL = (-vC) / L
        dvC = (iL - vC / R) / C

        if im > 0:
            dim = -Vin/Lm
        else:
            dim = 0
            im = 0



    # -----------------------
    # Integrate (Euler step)
    # -----------------------
    iL += diL * dt
    vC += dvC * dt
    iC = iL - (vC / R)
    im += dim * dt

    # -----------------------
    # store
    # -----------------------

    # Avarage capacitor current, 0 @ steady state over 1 period

    iC_arr_temp.append(iC)

    if k % (int(T / dt) * 5) == 0 and steady_state is False:
        sum = 0
        for i in iC_arr_temp:
            sum += i
        avg = sum / len(iC_arr_temp)

        if abs(avg) < 1e-6:
            steady_state = True
            print("Steady state", t)
            print(avg)

        iC_arr_temp = []


    if t >= t_start or (ss and steady_state):
        t_arr.append(t)
        iL_arr.append(iL)
        vC_arr.append(vC)
        iC_arr.append(iC)
        im_arr.append(im)
        q_arr.append(q)

        if ss and k % (int(T / dt)) == 0:
            p += 1

        if p == period_samples:
            break


    if k % (steps / 100) == 0:
        proc += 1
        print(f"{proc}%")

t_arr_millis = []

for t in t_arr:
    t_arr_millis.append(round(t*1000, 6))


sum = 0
for v in vC_arr:
    sum += v

avg = sum / len(vC_arr)
print(round(avg, 3), "V")
print(round(t_arr[-1], 3), "s")


# -----------------------
# Plot
# -----------------------
plt.figure()

plt.subplot(4,1,1)
plt.plot(t_arr_millis, q_arr)
plt.ylabel("q")
plt.grid()

plt.subplot(4,1,2)
plt.plot(t_arr_millis, iL_arr)
plt.ylabel("iL")
plt.grid()

plt.subplot(4,1,3)
plt.plot(t_arr_millis, vC_arr)
plt.ylabel("vC")
plt.grid()

plt.subplot(4,1,4)
plt.plot(t_arr_millis, im_arr)
plt.ylabel("im")
plt.xlabel("Time (s)")
plt.grid()

plt.tight_layout()
plt.savefig("test.png")
plt.show()