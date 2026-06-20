import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp


def simulate_pipeline(
    t_wall=0.012,
    closure_duration=2.0,
    delta_T=30.0,
    Kt=1.5,
    P0=2.0e6,
    Q0=0.10,
    r=0.25,
    t_end=60
):
    """
    Simulates a steel pipeline elbow subjected to pressure surge,
    thermal expansion, and fatigue damage.
    """

    # ----------------------------
    # Material and fluid properties
    # ----------------------------
    E = 200e9
    alpha = 12e-6
    rho = 1000
    wave_speed = 1000

    # ----------------------------
    # Valve and surge parameters
    # ----------------------------
    t_close_start = 10
    min_opening = 0.10
    surge_damping = 0.18
    surge_frequency = 1.2
    tau_pressure = 0.15

    # ----------------------------
    # Fatigue parameters
    # ----------------------------
    A_fatigue = 1e12
    m_fatigue = 3
    cycle_frequency = 0.2

    area = np.pi * r**2

    def valve_opening(t):
        if t < t_close_start:
            return 1.0
        elif t <= t_close_start + closure_duration:
            x = (t - t_close_start) / closure_duration
            opening = min_opening + (1 - min_opening) * 0.5 * (1 + np.cos(np.pi * x))
            return opening
        else:
            return min_opening

    def pressure_target(t):
        V0 = Q0 / area
        delta_V = V0 * (1 - min_opening)
        delta_P_max = rho * wave_speed * delta_V

        if t < t_close_start:
            return P0

        tau = t - t_close_start
        closure_fraction = 1 - valve_opening(t)

        surge = (
            delta_P_max
            * closure_fraction
            * np.exp(-surge_damping * tau)
            * (1 + 0.25 * np.sin(2 * np.pi * surge_frequency * tau))
        )

        return P0 + surge

    def ode_system(t, y):
        P = y[0]
        D = y[1]

        dPdt = (pressure_target(t) - P) / tau_pressure

        sigma_hoop = (P * r) / t_wall
        sigma_long_pressure = (P * r) / (2 * t_wall)
        sigma_thermal = E * alpha * delta_T
        sigma_long = sigma_long_pressure + sigma_thermal

        sigma_vm = np.sqrt(
            sigma_hoop**2
            - sigma_hoop * sigma_long
            + sigma_long**2
        )

        sigma_vm_elbow = Kt * sigma_vm

        sigma_hoop_base = (P0 * r) / t_wall
        sigma_long_base = (P0 * r) / (2 * t_wall) + sigma_thermal

        sigma_vm_base = np.sqrt(
            sigma_hoop_base**2
            - sigma_hoop_base * sigma_long_base
            + sigma_long_base**2
        )

        sigma_vm_base = Kt * sigma_vm_base

        delta_sigma = abs(sigma_vm_elbow - sigma_vm_base)
        delta_sigma_MPa = max(delta_sigma / 1e6, 0.001)

        Nf = A_fatigue * (delta_sigma_MPa ** (-m_fatigue))
        dDdt = cycle_frequency / Nf

        return [dPdt, dDdt]

    time_points = np.linspace(0, t_end, 2000)

    solution = solve_ivp(
        ode_system,
        [0, t_end],
        [P0, 0],
        t_eval=time_points,
        method="RK45"
    )

    t = solution.t
    P = solution.y[0]
    D = solution.y[1]

    sigma_hoop = (P * r) / t_wall
    sigma_long_pressure = (P * r) / (2 * t_wall)
    sigma_thermal = E * alpha * delta_T
    sigma_long = sigma_long_pressure + sigma_thermal

    sigma_vm = np.sqrt(
        sigma_hoop**2
        - sigma_hoop * sigma_long
        + sigma_long**2
    )

    sigma_vm_elbow = Kt * sigma_vm

    health_index = (1 - D) * 100

    data = pd.DataFrame({
        "Time (s)": t,
        "Pressure (MPa)": P / 1e6,
        "Hoop Stress (MPa)": sigma_hoop / 1e6,
        "Longitudinal Stress (MPa)": sigma_long / 1e6,
        "von Mises Stress (MPa)": sigma_vm_elbow / 1e6,
        "Fatigue Damage": D,
        "Health Index (%)": health_index
    })

    max_pressure = data["Pressure (MPa)"].max()
    max_vm = data["von Mises Stress (MPa)"].max()
    final_damage = data["Fatigue Damage"].iloc[-1]
    final_health = data["Health Index (%)"].iloc[-1]

    yield_strength_MPa = 250
    factor_of_safety = yield_strength_MPa / max_vm

    if factor_of_safety < 1:
        safety_check = "Fail"
    elif factor_of_safety < 1.5:
        safety_check = "Borderline"
    else:
        safety_check = "Pass"

    if max_vm > 350 or factor_of_safety < 1:
        risk_level = "Critical"
    elif max_vm > 250 or factor_of_safety < 1.5:
        risk_level = "Warning"
    elif max_vm > 150:
        risk_level = "Monitor"
    else:
        risk_level = "Safe"

    metrics = {
        "Max Pressure (MPa)": max_pressure,
        "Max von Mises Stress (MPa)": max_vm,
        "Final Fatigue Damage": final_damage,
        "Health Index (%)": final_health,
        "Factor of Safety": factor_of_safety,
        "Static Safety Check": safety_check,
        "Risk Level": risk_level
    }

    return data, metrics