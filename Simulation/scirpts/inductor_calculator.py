import math
from dataclasses import dataclass


# ============================================================
# AUDIO AMPLIFIER SMPS OUTPUT INDUCTOR DESIGN TOOL
# ============================================================
#
# Calculates:
#
#   - Number of turns
#   - Actual inductance
#   - Air gap
#   - Peak flux density
#   - Saturation margin
#   - Winding geometry
#   - Turns per layer
#   - Number of layers
#   - Copper fill factor
#   - DC resistance
#   - Copper losses
#   - Core losses
#   - Total losses
#   - Estimated temperature rise
#
# ============================================================


# ============================================================
# USER REQUIREMENTS
# ============================================================

TARGET_L = 220e-6          # Target inductance [H]

# Maximum instantaneous current.
#
# This is primarily used for:
#   - Saturation
#   - Peak copper loss
#
I_PEAK = 9.0              # [A]


# Ratio between average copper-loss power and
# peak-current copper-loss power.
#
# Example:
#
# 0.25 means:
#
# P_average = 25% of P_peak
#
# Since:
#
# P = I²R
#
# I_RMS = sqrt(0.25) * I_PEAK
#
POWER_RATIO = 0.25


# Switching frequency
F_SW = 100e3               # [Hz]


# ============================================================
# DESIGN LIMITS
# ============================================================

# Maximum RMS current density
MAX_CURRENT_DENSITY = 6.0  # [A/mm²]


# Maximum window fill factor
#
# 0.40 means 40% of available window area
# is allowed to be occupied by copper.
#
MAX_FILL_FACTOR = 0.40


# Maximum fraction of saturation flux density
#
# 0.80 means:
#
# B_peak <= 80% of B_sat
#
MAX_B_RATIO = 0.80


# Maximum acceptable average copper loss
MAX_COPPER_LOSS = 5.0      # [W]


# Maximum acceptable total loss
MAX_TOTAL_LOSS = 8.0       # [W]


# Maximum estimated temperature rise
MAX_TEMP_RISE = 50.0       # [°C]


# Ambient temperature
AMBIENT_TEMP = 30.0        # [°C]


# ============================================================
# FERRITE MATERIAL
# ============================================================
#
# Steinmetz equation:
#
# Pv = k * f^alpha * B^beta
#
# where:
#
# Pv = core loss density [W/m³]
# f  = frequency [Hz]
# B  = AC flux density [T]
#
# IMPORTANT:
#
# These are example values only.
# Replace them with values from your actual ferrite
# manufacturer's datasheet.
#
# ============================================================

@dataclass
class Material:

    name: str

    B_sat: float

    steinmetz_k: float
    steinmetz_alpha: float
    steinmetz_beta: float


N87 = Material(

    name="N87",

    B_sat=0.35,

    # Approximate illustrative values
    steinmetz_k=3.0,

    steinmetz_alpha=1.45,

    steinmetz_beta=2.4,

)


# ============================================================
# CORE DATABASE
# ============================================================
#
# IMPORTANT:
#
# These are approximate example values.
#
# Replace them with exact values from the core manufacturer.
#
# window_width and window_height describe the available
# bobbin winding window.
#
# thermal_resistance is an approximate core-to-ambient
# thermal resistance.
#
# ============================================================

@dataclass
class Core:

    name: str

    Ae: float               # Effective core area [m²]

    le: float               # Magnetic path length [m]

    Ve: float               # Effective core volume [m³]

    window_width: float     # Winding window width [m]

    window_height: float    # Winding window height [m]

    thermal_resistance: float   # [°C/W]

    volume: float


CORES = [

    Core(
        name="EE30", # E 30/15/7
        Ae=60e-6,      # Corrected from 83e-6 [3, 4]
        le=67e-3,      # Correct [3, 4]
        Ve=4.00e-6,    # Corrected from 5.56e-6 [3, 4]
        window_width=19.5e-3,  # Core inner width [4]
        window_height=9.7e-3,  # Core half-leg height [4]
        thermal_resistance=25, # Not specified in sources [5]
        volume=4.00e-6,
    ),

    # Core(
    #     name="ER35", # ER 35/20/11
    #     Ae=111e-6,     # Corrected from 96e-6 [2, 6]
    #     le=89.6e-3,    # Corrected from 80e-3 [2, 6]
    #     Ve=9.95e-6,    # Corrected from 7.68e-6 [2, 6]
    #     window_width=25.6e-3,  # Core inner width [2]
    #     window_height=14.7e-3, # Core half-leg height [2]
    #     thermal_resistance=20, # Not specified in sources [7]
    #     volume=9.95e-6,
    # ),

    Core(
        name="ETD39", # ETD 39/20/13
        Ae=125e-6,     # Correct [8, 9]
        le=92.2e-3,    # Correct [8, 9]
        Ve=11.5e-6,    # Correct [9, 10]
        window_width=29.3e-3,  # Correct core inner width [9]
        window_height=14.2e-3, # Correct core half-leg height [9]
        thermal_resistance=15, # Not specified in sources [11]
        volume=11.5e-6,
    ),

    Core(
        name="E42", # E 42/21/20
        Ae=234e-6,     # Corrected from 145e-6 [12, 13]
        le=97e-3,      # Correct [12, 13]
        Ve=22.7e-6,    # Corrected from 14.1e-6 [12, 13]
        window_width=29.5e-3,  # Core inner width [13]
        window_height=14.8e-3, # Core half-leg height [13]
        thermal_resistance=12, # Not specified in sources [14]
        volume=22.7e-6,
    ),

    Core(
        name="ETD44", # ETD 44/22/15
        Ae=173e-6,     # Correct [15, 16]
        le=103e-3,     # Corrected from 100e-3 [15, 16]
        Ve=17.8e-6,    # Corrected from 17.3e-6 [16, 17]
        window_width=32.5e-3,  # Core inner width [16]
        window_height=16.1e-3, # Core half-leg height [16]
        thermal_resistance=10, # Not specified in sources [18]
        volume=17.8e-6,
    ),

    Core(
        name="ETD49", # ETD 49/25/16
        Ae=211e-6,     # Correct [19, 20]
        le=114e-3,     # Corrected from 108e-3 [19, 20]
        Ve=24.1e-6,    # Corrected from 22.8e-6 [20, 21]
        window_width=36.1e-3,  # Core inner width [20]
        window_height=17.7e-3, # Core half-leg height [20]
        thermal_resistance=8,  # Not specified in sources [22]
        volume=24.1e-6,
    ),

]


# ============================================================
# AIR GAP OPTIONS
# ============================================================

AIR_GAPS = [

    0.5e-3,
    0.75e-3,
    1.0e-3,
    1.25e-3,
    1.5e-3,
    1.75e-3,
    2.0e-3,
    2.5e-3,
    3.0e-3,

]


# ============================================================
# WIRE OPTIONS
# ============================================================

WIRE_DIAMETERS = [

    0.30e-3,
    0.40e-3,
    0.50e-3,
    0.60e-3,
    0.70e-3,
    0.80e-3,
    1.00e-3,

]


PARALLEL_WIRES = [

    1,
    2,
    3,
    4,
    5,
    6,
    8,
    10,
    12,
    15,

]


# ============================================================
# CONSTANTS
# ============================================================

MU_0 = 4 * math.pi * 1e-7

MU_R = 2000

RHO_COPPER = 1.724e-8


# ============================================================
# CURRENT CALCULATION
# ============================================================

I_RMS = (

    math.sqrt(POWER_RATIO) *
    I_PEAK

)


# ============================================================
# INDUCTOR CALCULATION
# ============================================================

def calculate_inductor(

    core,
    material,
    air_gap,
    wire_diameter,
    parallel_wires,

):


    # --------------------------------------------------------
    # Wire cross-sectional area
    # --------------------------------------------------------

    single_wire_area = (

        math.pi *
        (wire_diameter / 2)**2

    )


    copper_area = (

        single_wire_area *
        parallel_wires

    )


    # --------------------------------------------------------
    # Number of turns
    # --------------------------------------------------------

    N_required = math.sqrt(

        TARGET_L *

        (
            core.le +
            MU_R *
            air_gap
        )

        /

        (
            MU_0 *
            MU_R *
            core.Ae
        )

    )


    N = math.ceil(N_required)


    # --------------------------------------------------------
    # Actual inductance
    # --------------------------------------------------------

    L_actual = (

        MU_0 *
        MU_R *
        core.Ae *
        N**2

        /

        (

            core.le +
            MU_R *
            air_gap

        )

    )


    # --------------------------------------------------------
    # Flux density
    # --------------------------------------------------------

    B_peak = (

        L_actual *
        I_PEAK

        /

        (

            N *
            core.Ae

        )

    )


    # --------------------------------------------------------
    # AC flux swing
    #
    # For a forward converter:
    #
    # ΔB = V * dt / (N * Ae)
    #
    #
    # We need an estimate of the applied voltage.
    #
    # Assume the inductor sees approximately 70 V
    # during the charging portion of the switching cycle.
    #
    # This should later be replaced with the actual
    # converter waveform.
    #
    # --------------------------------------------------------

    V_L = 70.0

    duty_cycle = 0.43

    delta_B = (

        V_L *
        duty_cycle

        /

        (

            N *
            core.Ae *
            F_SW

        )

    )


    # Core loss models normally use AC flux amplitude.
    #
    # Approximate:
    #
    # B_AC = ΔB / 2
    #
    B_AC = delta_B / 2

    # --------------------------------------------------------
    # Saturation margin
    # --------------------------------------------------------

    saturation_margin = (

        material.B_sat /
        B_peak

    )


    # --------------------------------------------------------
    # Current density
    # --------------------------------------------------------

    J_rms = (

        I_RMS /
        copper_area

    ) / 1e6


    J_peak = (

        I_PEAK /
        copper_area

    ) / 1e6


    # --------------------------------------------------------
    # Physical winding model
    # --------------------------------------------------------

    turns_per_layer = math.floor(

        core.window_width /
        wire_diameter

    )


    if turns_per_layer < 1:

        return None


    # Number of layers

    layers = math.ceil(

        N /
        turns_per_layer

    )


    # --------------------------------------------------------
    # Actual copper occupied area
    #
    # This is now:
    #
    # copper area / available window area
    #
    # --------------------------------------------------------

    window_area = (

        core.window_width *
        core.window_height

    )


    copper_fill = (

        N *
        copper_area

        /

        window_area

    )


    # --------------------------------------------------------
    # Check fill
    # --------------------------------------------------------

    if copper_fill > MAX_FILL_FACTOR:

        return None


    # --------------------------------------------------------
    # Winding height
    #
    # Each layer consists of one wire diameter.
    #
    # --------------------------------------------------------

    winding_height = (

        layers *
        wire_diameter

    )


    if winding_height > core.window_height:

        return None


    # --------------------------------------------------------
    # Average turn length
    #
    # We approximate the turn length increasing with
    # each additional layer.
    # --------------------------------------------------------

    average_layer = (

        layers - 1
    ) / 2


    mean_turn_length = (

        2 *

        (

            core.window_width +

            2 *
            average_layer *
            wire_diameter

        )

    )


    # --------------------------------------------------------
    # Total copper length
    # --------------------------------------------------------

    wire_length = (

        N *
        mean_turn_length

    )


    # --------------------------------------------------------
    # DC resistance
    # --------------------------------------------------------

    R_dc = (

        RHO_COPPER *
        wire_length

        /

        copper_area

    )


    # --------------------------------------------------------
    # Copper losses
    # --------------------------------------------------------

    P_copper_peak = (

        I_PEAK**2 *
        R_dc

    )


    P_copper_rms = (

        I_RMS**2 *
        R_dc

    )


    # --------------------------------------------------------
    # CORE LOSS
    #
    # Steinmetz:
    #
    # Pv = k f^alpha B^beta
    #
    # --------------------------------------------------------

    P_core_density = (

        material.steinmetz_k *

        F_SW **
        material.steinmetz_alpha *

        B_AC **
        material.steinmetz_beta

    )


    # Core loss

    P_core = (

        P_core_density *
        core.Ve

    )


    # --------------------------------------------------------
    # TOTAL LOSS
    # --------------------------------------------------------

    P_total = (

        P_copper_rms +
        P_core

    )


    # --------------------------------------------------------
    # TEMPERATURE RISE
    #
    # Simplified:
    #
    # ΔT = P_loss * Rθ
    #
    # --------------------------------------------------------

    temp_rise = (

        P_total *
        core.thermal_resistance

    )


    T_core = (

        AMBIENT_TEMP +
        temp_rise

    )


    # --------------------------------------------------------
    # Stored energy
    # --------------------------------------------------------

    E_stored = (

        0.5 *
        L_actual *
        I_PEAK**2

    )


    # --------------------------------------------------------
    # Return
    # --------------------------------------------------------

    return {

        "core": core,

        "material": material,

        "air_gap": air_gap,

        "wire_diameter":
            wire_diameter,

        "parallel_wires":
            parallel_wires,

        "turns":
            N,

        "turns_per_layer":
            turns_per_layer,

        "layers":
            layers,

        "inductance":
            L_actual,

        "B_peak":
            B_peak,

        "B_AC":
            B_AC,

        "delta_B":
            delta_B,

        "saturation_margin":
            saturation_margin,

        "copper_area":
            copper_area,

        "J_rms":
            J_rms,

        "J_peak":
            J_peak,

        "copper_fill":
            copper_fill,

        "winding_height":
            winding_height,

        "wire_length":
            wire_length,

        "R_dc":
            R_dc,

        "P_copper_peak":
            P_copper_peak,

        "P_copper_rms":
            P_copper_rms,

        "P_core":
            P_core,

        "P_total":
            P_total,

        "temp_rise":
            temp_rise,

        "T_core":
            T_core,

        "energy":
            E_stored,

    }


# ============================================================
# VALIDATE DESIGN
# ============================================================

def is_valid(result):


    # Saturation

    if (

        result["B_peak"]

        >

        result["material"].B_sat *
        MAX_B_RATIO

    ):

        return False


    # Current density

    if (

        result["J_rms"]

        >

        MAX_CURRENT_DENSITY

    ):

        return False


    # Copper loss

    if (

        result["P_copper_rms"]

        >

        MAX_COPPER_LOSS

    ):

        return False


    # Total loss

    if (

        result["P_total"]

        >

        MAX_TOTAL_LOSS

    ):

        return False


    # Temperature

    if (

        result["temp_rise"]

        >

        MAX_TEMP_RISE

    ):

        return False


    return True


# ============================================================
# SEARCH
# ============================================================

def search_designs():


    valid_designs = []


    for core in CORES:


        for air_gap in AIR_GAPS:


            for wire_diameter in WIRE_DIAMETERS:


                for parallel_wires in PARALLEL_WIRES:


                    result = calculate_inductor(

                        core,

                        N87,

                        air_gap,

                        wire_diameter,

                        parallel_wires,

                    )


                    if result is None:

                        continue


                    if is_valid(result):

                        valid_designs.append(

                            result

                        )


    return valid_designs


# ============================================================
# PRINT RESULT
# ============================================================

def print_result(result):


    core = result["core"]


    print()

    print("=" * 70)

    print(

        f"CORE: {core.name}"

    )

    print("=" * 70)


    print()

    print(

        f"Air gap:              "
        f"{result['air_gap']*1000:.2f} mm"

    )


    print(

        f"Turns:                "
        f"{result['turns']}"

    )


    print(

        f"Turns/layer:          "
        f"{result['turns_per_layer']}"

    )


    print(

        f"Layers:               "
        f"{result['layers']}"

    )


    print()

    print(

        f"Inductance:           "
        f"{result['inductance']*1e6:.2f} µH"

    )


    print(

        f"Peak B:               "
        f"{result['B_peak']:.3f} T"

    )


    print(

        f"AC B:                 "
        f"{result['B_AC']:.3f} T"

    )


    print(

        f"Saturation margin:    "
        f"{result['saturation_margin']:.2f}x"

    )


    print()

    print(

        f"Wire:                 "
        f"{result['wire_diameter']*1000:.2f} mm"

    )


    print(

        f"Parallel wires:       "
        f"{result['parallel_wires']}"

    )


    print(

        f"Copper area:          "
        f"{result['copper_area']*1e6:.2f} mm²"

    )


    print(

        f"RMS current density:  "
        f"{result['J_rms']:.2f} A/mm²"

    )


    print(

        f"Peak current density: "
        f"{result['J_peak']:.2f} A/mm²"

    )


    print(

        f"Window fill:          "
        f"{result['copper_fill']*100:.1f} %"

    )


    print()

    print(

        f"Wire length:          "
        f"{result['wire_length']:.2f} m"

    )


    print(

        f"DC resistance:        "
        f"{result['R_dc']*1000:.2f} mΩ"

    )


    print()

    print(

        f"Peak copper loss:     "
        f"{result['P_copper_peak']:.2f} W"

    )


    print(

        f"RMS copper loss:      "
        f"{result['P_copper_rms']:.2f} W"

    )


    print(

        f"Core loss:            "
        f"{result['P_core']:.2f} W"

    )


    print(

        f"Total loss:           "
        f"{result['P_total']:.2f} W"

    )


    print()

    print(

        f"Temperature rise:     "
        f"{result['temp_rise']:.1f} °C"

    )


    print(

        f"Estimated core temp:  "
        f"{result['T_core']:.1f} °C"

    )


    print()

    print(

        f"Stored energy:        "
        f"{result['energy']*1000:.2f} mJ"

    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":


    print()

    print(
        "AUDIO AMPLIFIER OUTPUT INDUCTOR DESIGN"
    )

    print("=" * 70)


    print()

    print(

        f"Target inductance:     "
        f"{TARGET_L*1e6:.1f} µH"

    )


    print(

        f"Peak current:           "
        f"{I_PEAK:.2f} A"

    )


    print(

        f"Power ratio:            "
        f"{POWER_RATIO*100:.1f} %"

    )


    print(

        f"Calculated RMS current: "
        f"{I_RMS:.2f} A"

    )


    print()

    print(
        "Searching..."
    )


    designs = search_designs()


    if not designs:


        print()

        print(
            "No valid designs found."
        )


        print()

        print(
            "Try relaxing:"
        )

        print(
            "  - MAX_CURRENT_DENSITY"
        )

        print(
            "  - MAX_COPPER_LOSS"
        )

        print(
            "  - MAX_TOTAL_LOSS"
        )

        print(
            "  - MAX_TEMP_RISE"
        )


    else:


        # Sort by core volume

        designs.sort(

            key=lambda x:

            (

                x["core"].volume,

                x["P_total"]

            )

        )


        print()

        print(

            f"Found {len(designs)} valid designs."

        )


        print()

        print(
            "SMALLEST VALID DESIGN"
        )


        print_result(

            designs[0]

        )


        print()

        print("=" * 70)

        print(
            "TOP 10 DESIGNS"
        )

        print("=" * 70)


        for i, result in enumerate(

            designs[:10],

            start=1

        ):


            print(

                f"{i:2d}. "

                f"{result['core'].name:6s} | "

                f"Gap: "
                f"{result['air_gap']*1000:4.2f} mm | "

                f"{result['turns']:2d} turns | "

                f"{result['wire_diameter']*1000:4.2f} mm × "

                f"{result['parallel_wires']:2d} | "

                f"Layers: "
                f"{result['layers']:2d} | "

                f"Core: "
                f"{result['P_core']:.2f} W | "

                f"Total: "
                f"{result['P_total']:.2f} W"

            )