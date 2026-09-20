import control as ct
import numpy as np
import matplotlib.pyplot as plt


def print_info(G):
    p = ct.poles(G)

    wn, zeta, poles = ct.damp(G)

    info = ct.step_info(G)

    print("\nPOLES")
    print(p)

    print("\nNatural frequency (rad/s)")
    print(wn)

    print("\nNatural frequency (Hz)")
    print(wn/(2*np.pi))

    print("\nDamping ratio")
    print(zeta)

    if zeta[0] > 1:
        print("Overdamped")

    elif zeta[0] > 0.7:
        print("Well damped")

    elif zeta[0] > 0:
        print("Underdamped")

    else:
        print("Unstable")

    print("\nStep info")

    for key, value in info.items():
        print(key, round(value, 6))
    
    # Bode plot
    G.bode_plot()

    # Pole Map
    plt.figure()
    ct.pzmap(G)
    plt.grid()
    plt.show()

    # Step response Open Loop
    t, y = ct.step_response(sys)

    plt.figure()
    plt.plot(t, y)
    plt.ylabel("Step Response")
    plt.grid()
    plt.show()

Vin = 325
n = 0.2
D = 0.3

L = 220e-6
C = 470e-6
R = 10

A = np.array([
    [0, -1/L],
    [1/C, -1/(R*C)]
])

B = np.array([
    [n*Vin/L],
    [0]
])

Cmat = np.array([
    [0, 1]
])

Dmat = np.array([
    [0]
])

sys = ct.ss(A, B, Cmat, Dmat)     # Steady state equation

# Convert to transfer function
G = ct.ss2tf(sys)
print("\n -------- Open Loop --------\n")
print_info(G)

# Closed loop
Kp = 0.05
Ki = 50
Gc = ct.tf([Kp, Ki], [1])
closed = ct.feedback(Gc*G, 1)
print("\n -------- Closed Loop --------\n")
print_info(closed)
