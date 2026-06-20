# Smart Pipeline Elbow Digital Twin

A Python-based digital twin simulation for a 90-degree steel pipeline elbow subjected to pressure surge, thermal expansion, and fatigue loading.

## Project Overview

This project models the structural response of a steel pipeline elbow under changing operating conditions. The simulation calculates internal pressure response, pipe wall stresses, von Mises stress, fatigue damage, factor of safety, and a digital twin risk classification.

The dashboard is built using Streamlit and allows the user to interactively vary key engineering parameters such as wall thickness, valve closure time, temperature rise, operating pressure, flow rate, and elbow stress concentration factor.

## Engineering Problem

Pipeline elbows and welded junctions are critical infrastructure components because they experience stress concentration, pressure fluctuations, and thermal loading. Rapid valve closure can generate pressure surges, which increase pipe wall stress and may contribute to fatigue damage over time.

This project demonstrates how a simplified physics-based digital twin can be used to monitor structural health and compare operating risk across different scenarios.

## Physics Included

The model includes:

* Pressure surge caused by valve closure
* Hoop stress in a thin-walled pressure pipe
* Longitudinal pressure stress
* Restrained thermal stress
* von Mises equivalent stress
* Stress concentration at the elbow
* Fatigue damage using a simplified S-N curve and Miner's rule
* Factor of safety against yield
* Risk classification: Safe, Monitor, Warning, or Critical

## Main Equations

Hoop stress:

[
\sigma_h = \frac{Pr}{t}
]

Longitudinal pressure stress:

[
\sigma_l = \frac{Pr}{2t}
]

Thermal stress:

[
\sigma_T = E\alpha \Delta T
]

von Mises stress:

[
\sigma_{vm} = \sqrt{\sigma_h^2 - \sigma_h\sigma_l + \sigma_l^2}
]

Factor of safety:

[
FOS = \frac{\sigma_y}{\sigma_{vm,max}}
]

Fatigue damage is estimated using a simplified S-N curve and Miner's rule.

## Dashboard Features

The Streamlit dashboard includes:

* Interactive sliders for pipe and operating parameters
* Real-time pressure response plot
* Real-time stress response plot
* Fatigue damage plot
* Health index plot
* Maximum pressure calculation
* Maximum von Mises stress calculation
* Factor of safety calculation
* Automatic risk classification

## Technologies Used

* Python
* NumPy
* Pandas
* SciPy
* Plotly
* Streamlit
* Matplotlib

## How to Run

Install the required packages:

```bash
py -m pip install -r requirements.txt
```

Run the Streamlit dashboard:

```bash
py -m streamlit run app.py
```

## Project Status

Current version: Interactive digital twin dashboard with real-time parameter control.

Future improvements could include more realistic fatigue cycle counting, material selection, pressure sensor data input, and deployment to Streamlit Community Cloud.
