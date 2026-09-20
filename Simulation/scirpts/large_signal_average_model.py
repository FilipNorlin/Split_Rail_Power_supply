import numpy as np
import matplotlib.pyplot as plt

# Parameters
Vin = 325
n = 1.13
L = 220e-6
C = 470e-6
R = 10
Lm = 2e-3

D = 0.33          # average duty

dt = 100e-9

t_start = 0
t_end = t_start + 130e-3

steps = int(t_end/dt)

# states
iL = 0
vC = 0
im = 0

# storage
t_arr=[]
iL_arr=[]
vC_arr=[]
im_arr=[]
proc = 1

for k in range(steps):

    t = k*dt

    # LARGE SIGNAL AVERAGED MODEL

    diL = (D*n*Vin - vC)/L

    dvC = (iL - vC/R)/C

    dim = ((2*D-1)*Vin)/Lm

    # Euler
    iL += diL*dt
    vC += dvC*dt
    im += dim*dt


    # store
    if t >= t_start:
        t_arr.append(t*1000)
        iL_arr.append(iL)
        vC_arr.append(vC)
        im_arr.append(im)
    
    if k % (int(steps / 100)) == 0:
        print(f"{proc}%")
        proc += 1

# Plot
plt.figure(figsize=(8,6))

plt.subplot(211)
plt.plot(t_arr,iL_arr)
plt.ylabel("iL (A)")
plt.grid()

plt.subplot(212)
plt.plot(t_arr,vC_arr)
plt.ylabel("vC (V)")
plt.grid()

#plt.subplot(313)
#plt.plot(t_arr,im_arr)
#plt.ylabel("im (A)")
#plt.xlabel("ms")
#plt.grid()

plt.tight_layout()
plt.show()