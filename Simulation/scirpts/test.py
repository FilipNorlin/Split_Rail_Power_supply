import math


# ============================================================
# SMPS OUTPUT FILTER CALCULATOR
# ============================================================
#
# Calculates:
#
#   - Output current
#   - Inductor ripple current
#   - Inductor peak current
#   - Inductor minimum current
#   - Inductor RMS current
#   - Output voltage ripple
#   - Capacitor ripple current
#   - Capacitor ESR losses
#   - DCM / CCM operation
#
# Designed for the Split Rail 1 kW SMPS project.
#
# ============================================================


# ============================================================
# USER INPUTS
# ============================================================

# ------------------------------------------------------------
# OUTPUT POWER
# ------------------------------------------------------------

P_OUT = 1000.0             # Maximum output power [W]


# ------------------------------------------------------------
# OUTPUT VOLTAGE
# ------------------------------------------------------------
#
# For ±70 V:
#
# +70 V to -70 V = 140 V total
#
# ------------------------------------------------------------

V_OUT = 140.0              # Total output voltage [V]


# ------------------------------------------------------------
# SWITCHING FREQUENCY
# ------------------------------------------------------------

F_SW = 100e3               # Switching frequency [Hz]


# ------------------------------------------------------------
# DUTY CYCLE
# ------------------------------------------------------------

D = 0.43                   # Duty cycle


# ------------------------------------------------------------
# INDUCTOR
# ------------------------------------------------------------

L = 220e-6                 # Inductance [H]


# ------------------------------------------------------------
# OUTPUT CAPACITOR
# ------------------------------------------------------------
#
# Total effective capacitance seen by the output.
#
# Example:
#
# 4700 uF = 4700e-6
#
# ------------------------------------------------------------

C_OUT = 11000e-6            # Output capacitance [F]


# ------------------------------------------------------------
# CAPACITOR ESR
# ------------------------------------------------------------

ESR = 10e-3                # ESR [Ω]


# ------------------------------------------------------------
# CAPACITOR BANK
# ------------------------------------------------------------
#
# Set to True if you want to include the capacitor bank
# as a power source during transient operation.
#
# ------------------------------------------------------------

USE_CAPACITOR_BANK = True


# Maximum power that the DC-DC converter supplies.
#
# The capacitor bank supplies the rest during peaks.
#
# Example:
#
# Converter = 800 W
# Amplifier = 1000 W
#
# Capacitor bank supplies:
#
# 1000 - 800 = 200 W
#
# ------------------------------------------------------------

P_CONVERTER = 800.0        # DC-DC converter power [W]


# ============================================================
# BASIC CALCULATIONS
# ============================================================

# ------------------------------------------------------------
# Average output current
# ------------------------------------------------------------

I_OUT = (

    P_OUT /
    V_OUT

)


# ------------------------------------------------------------
# Average inductor current
# ------------------------------------------------------------

I_L_AVG = I_OUT


# ------------------------------------------------------------
# Inductor ripple current
#
# ΔI = V * D / (L * f)
#
# ------------------------------------------------------------

DELTA_I = (

    V_OUT *
    D

    /

    (
        L *
        F_SW
    )

)


# ------------------------------------------------------------
# Peak inductor current
# ------------------------------------------------------------

I_L_PEAK = (

    I_L_AVG +
    DELTA_I / 2

)


# ------------------------------------------------------------
# Minimum inductor current
# ------------------------------------------------------------

I_L_MIN = (

    I_L_AVG -
    DELTA_I / 2

)


# ------------------------------------------------------------
# Inductor RMS current
#
# For triangular ripple:
#
# I_RMS = sqrt(
#
#   I_DC² +
#   ΔI² / 12
#
# )
#
# ------------------------------------------------------------

I_L_RMS = math.sqrt(

    I_L_AVG**2 +

    DELTA_I**2 / 12

)


# ============================================================
# CONDUCTION MODE
# ============================================================

if I_L_MIN > 0:

    CONDUCTION_MODE = "CCM (Continuous Conduction Mode)"

else:

    CONDUCTION_MODE = "DCM (Discontinuous Conduction Mode)"


# ============================================================
# OUTPUT VOLTAGE RIPPLE
# ============================================================

# ------------------------------------------------------------
# Capacitive voltage ripple
#
# ΔV_C = ΔI / (8 * f * C)
#
# This is the triangular-current approximation.
#
# ------------------------------------------------------------

DELTA_V_CAP = (

    DELTA_I

    /

    (

        8 *
        F_SW *
        C_OUT

    )

)


# ------------------------------------------------------------
# ESR voltage ripple
#
# ΔV_ESR = ΔI * ESR
#
# ------------------------------------------------------------

DELTA_V_ESR = (

    DELTA_I *
    ESR

)


# ------------------------------------------------------------
# Total output voltage ripple
#
# Conservative approximation:
#
# ΔV_TOTAL = ΔV_C + ΔV_ESR
#
# ------------------------------------------------------------

DELTA_V_TOTAL = (

    DELTA_V_CAP +
    DELTA_V_ESR

)


# ============================================================
# CAPACITOR RMS CURRENT
# ============================================================

# For triangular ripple current:
#
# I_C_RMS = ΔI / sqrt(12)
#
# ------------------------------------------------------------

I_C_RMS = (

    DELTA_I /
    math.sqrt(12)

)


# ============================================================
# CAPACITOR ESR POWER LOSS
# ============================================================

P_CAP_ESR = (

    I_C_RMS**2 *
    ESR

)


# ============================================================
# CAPACITOR BANK
# ============================================================

if USE_CAPACITOR_BANK:


    # --------------------------------------------------------
    # Power supplied by capacitor bank
    # --------------------------------------------------------

    P_CAP_BANK = max(

        P_OUT -
        P_CONVERTER,

        0

    )


    # --------------------------------------------------------
    # Current supplied by capacitor bank
    # --------------------------------------------------------

    I_CAP_BANK = (

        P_CAP_BANK /
        V_OUT

    )


else:


    P_CAP_BANK = 0.0

    I_CAP_BANK = 0.0


# ============================================================
# PRINT RESULTS
# ============================================================

print()

print("=" * 70)

print(
    "SMPS OUTPUT FILTER CALCULATOR"
)

print("=" * 70)


# ------------------------------------------------------------
# BASIC SYSTEM
# ------------------------------------------------------------

print()

print(
    "SYSTEM"
)

print("-" * 70)


print(

    f"Output power:              "
    f"{P_OUT:.1f} W"

)


print(

    f"Output voltage:            "
    f"{V_OUT:.1f} V"

)


print(

    f"Switching frequency:       "
    f"{F_SW/1000:.1f} kHz"

)


print(

    f"Duty cycle:                "
    f"{D*100:.1f} %"

)


# ------------------------------------------------------------
# CURRENT
# ------------------------------------------------------------

print()

print(
    "CURRENT"
)

print("-" * 70)


print(

    f"Average output current:    "
    f"{I_OUT:.3f} A"

)


print(

    f"Average inductor current:  "
    f"{I_L_AVG:.3f} A"

)


print(

    f"Inductor ripple current:   "
    f"{DELTA_I:.3f} A p-p"

)


print(

    f"Inductor peak current:     "
    f"{I_L_PEAK:.3f} A"

)


print(

    f"Inductor minimum current:   "
    f"{I_L_MIN:.3f} A"

)


print(

    f"Inductor RMS current:      "
    f"{I_L_RMS:.3f} A"

)


print()

print(

    f"Conduction mode:            "
    f"{CONDUCTION_MODE}"

)


# ------------------------------------------------------------
# VOLTAGE RIPPLE
# ------------------------------------------------------------

print()

print(
    "OUTPUT VOLTAGE RIPPLE"
)

print("-" * 70)


print(

    f"Capacitive ripple:         "
    f"{DELTA_V_CAP*1000:.3f} mV p-p"

)


print(

    f"ESR ripple:                "
    f"{DELTA_V_ESR*1000:.3f} mV p-p"

)


print(

    f"Total estimated ripple:    "
    f"{DELTA_V_TOTAL*1000:.3f} mV p-p"

)


print(

    f"Ripple percentage:         "
    f"{DELTA_V_TOTAL/V_OUT*100:.5f} %"

)


# ------------------------------------------------------------
# CAPACITOR
# ------------------------------------------------------------

print()

print(
    "OUTPUT CAPACITOR"
)

print("-" * 70)


print(

    f"Capacitance:               "
    f"{C_OUT*1e6:.0f} µF"

)


print(

    f"ESR:                       "
    f"{ESR*1000:.2f} mΩ"

)


print(

    f"Capacitor RMS ripple:      "
    f"{I_C_RMS:.3f} A"

)


print(

    f"Capacitor ESR loss:        "
    f"{P_CAP_ESR:.3f} W"

)


# ------------------------------------------------------------
# CAPACITOR BANK
# ------------------------------------------------------------

if USE_CAPACITOR_BANK:


    print()

    print(
        "CAPACITOR BANK"
    )

    print("-" * 70)


    print(

        f"DC-DC converter power:     "
        f"{P_CONVERTER:.1f} W"

    )


    print(

        f"Capacitor bank power:      "
        f"{P_CAP_BANK:.1f} W"

    )


    print(

        f"Capacitor bank current:    "
        f"{I_CAP_BANK:.3f} A"

    )


# ------------------------------------------------------------
# INDUCTOR ENERGY
# ------------------------------------------------------------

E_INDUCTOR = (

    0.5 *
    L *
    I_L_PEAK**2

)


print()

print(
    "INDUCTOR"
)

print("-" * 70)


print(

    f"Inductance:                "
    f"{L*1e6:.1f} µH"

)


print(

    f"Peak stored energy:        "
    f"{E_INDUCTOR*1000:.3f} mJ"

)


print()

print("=" * 70)