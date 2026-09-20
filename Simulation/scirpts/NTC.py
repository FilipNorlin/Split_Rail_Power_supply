import math
import numpy as np
from scipy.optimize import fsolve


class NTC:

    def __init__(self, resistance_data, temperature_data):
        self.T0 = 273.15
        self.A = None
        self.B = None
        self.C = None
        self.solve_coefficient(resistance_data, temperature_data)
        self.R = 0
        self.temp = 0

        print(self.A)
        print(self.B)
        print(self.C)

    def set_resistance(self, value):
        if value <= 0:
            print("Value out of range")
            return
        if self.A is None or self.B is None or self.C is None:
            print("Coefficients are not set")
            return

        self.R = value

        T_inv = (
            self.A + self.B * math.log(self.R) + self.C * math.pow(math.log(self.R), 3)
        )

        self.temp = 1 / T_inv - self.T0

    def get_resistance(self):
        return self.R

    def get_temperature_range(self):
        return [self.temp_min, self.temp_max]

    def set_temperature(self, value):
        T_kelvin = value + self.T0

        def equation(R):
            return (
                self.A + self.B * np.log(R) + self.C * (np.log(R)) ** 3 - 1 / T_kelvin
            )

        # Initial guess (important!)
        R_guess = self.R if self.R > 0 else 10000

        R_solution = fsolve(equation, R_guess)[0]

        self.R = R_solution
        self.temp = value

    def get_temperature(self):
        return self.temp

    def solve_coefficient(self, resistances, temperatures):
        R_array = np.array(resistances)
        T_array = np.array(temperatures) + self.T0

        # Build matrix M
        M = np.column_stack((np.ones(3), np.log(R_array), np.log(R_array) ** 3))

        # Solve system
        coeff = np.linalg.solve(M, 1 / T_array)

        self.A, self.B, self.C = coeff

    def get_coefficients(self):
        return [self.A, self.B, self.C]
