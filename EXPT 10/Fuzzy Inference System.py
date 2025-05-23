import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt


class FuzzyVariable:
    def __init__(self, name, universe_min, universe_max, universe_step=1):
        self.name = name
        self.universe = np.arange(
            universe_min, universe_max + universe_step, universe_step)
        self.mfs = {}

    def add_trimf(self, mf_name, params):
        self.mfs[mf_name] = fuzz.trimf(self.universe, params)

    def fuzzify(self, crisp_input):
        fuzzified_levels = {}
        for name, mf_array in self.mfs.items():
            fuzzified_levels[name] = fuzz.interp_membership(
                self.universe, mf_array, crisp_input)
        return fuzzified_levels

    def plot_mfs(self, ax):
        ax.set_title(f"{self.name} Membership Functions")
        for mf_name, mf_array in self.mfs.items():
            ax.plot(self.universe, mf_array, label=mf_name)
        ax.set_xlabel(self.name.split(
            '(')[0].strip())
        ax.set_ylabel("Membership Degree")
        ax.legend()


class FuzzyFanController:
    def __init__(self):
        self.temperature_var = FuzzyVariable("Temperature (°C)", 0, 40, 1)
        self.temperature_var.add_trimf('Low', [0, 0, 20])
        self.temperature_var.add_trimf('Medium', [10, 20, 30])
        self.temperature_var.add_trimf('High', [20, 30, 40])

        self.fan_speed_var = FuzzyVariable("Fan Speed", 0, 10, 1)
        self.fan_speed_var.add_trimf('Low', [0, 0, 5])
        self.fan_speed_var.add_trimf('Medium', [2, 5, 8])
        self.fan_speed_var.add_trimf('High', [5, 10, 10])

        self.rules_mapping = {
            'Low': 'Low',
            'Medium': 'Medium',
            'High': 'High'
        }

    def plot_all_membership_functions(self, filename="fuzzy_mfs_oop_original.png"):
        fig, (ax_temp, ax_fan) = plt.subplots(nrows=2, figsize=(10, 6))

        self.temperature_var.plot_mfs(ax_temp)
        self.fan_speed_var.plot_mfs(ax_fan)

        plt.tight_layout()
        plt.savefig(filename)
        print(f"Membership function plot saved as: {filename}")

    def compute_fan_speed(self, crisp_temperature_input):
        fuzzified_temp_levels = self.temperature_var.fuzzify(
            crisp_temperature_input)

        aggregated_fan_mfx = np.zeros_like(
            self.fan_speed_var.universe, dtype=float)
        active_rules = False

        for temp_mf_name, temp_activation_level in fuzzified_temp_levels.items():
            if temp_activation_level > 0:
                active_rules = True
                fan_mf_name = self.rules_mapping.get(temp_mf_name)
                if fan_mf_name:
                    fan_mf_array = self.fan_speed_var.mfs[fan_mf_name]
                    aggregated_fan_mfx += fan_mf_array * temp_activation_level

        if not active_rules or np.sum(aggregated_fan_mfx) < 1e-9:
            return np.nan

        crisp_fan_speed = fuzz.defuzz(
            self.fan_speed_var.universe, aggregated_fan_mfx, 'centroid')
        return crisp_fan_speed


if __name__ == "__main__":
    controller = FuzzyFanController()
    controller.plot_all_membership_functions()

    while True:
        try:
            temp_input_str = input(
                "Enter the current temperature (°C) (e.g., 28): ")
            if not temp_input_str:
                print("No input provided. Exiting.")
                exit()
            temperature_input = float(temp_input_str)
            min_temp_uni = controller.temperature_var.universe.min()
            max_temp_uni = controller.temperature_var.universe.max()
            if not (min_temp_uni <= temperature_input <= max_temp_uni):
                print(
                    f"Warning: Input temperature {temperature_input}°C is outside the defined universe [{min_temp_uni},{max_temp_uni}°C]. Results may be extrapolated or clipped.")
            break
        except ValueError:
            print("Invalid input. Please enter a numeric value for temperature.")
        except EOFError:
            print("EOF received. Exiting.")
            exit()

    calculated_speed = controller.compute_fan_speed(temperature_input)

    temp_display = f"{int(temperature_input)}" if temperature_input.is_integer(
    ) else f"{temperature_input}"
    print(f"\nTemperature: {temp_display}°C")

    if not np.isnan(calculated_speed):
        print(f"Fuzzified fan speed: {calculated_speed:.2f}")
    else:
        print("Fuzzified fan speed: Undefined (e.g., input outside active rule range or no rule activation).")
