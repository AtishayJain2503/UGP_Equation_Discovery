import matplotlib.pyplot as plt

from equations.pendulum import LargeAnglePendulum
from data.simulator import Simulator

# Create system
system = LargeAnglePendulum()

# Simulate
sim = Simulator(system, dt=0.01, T=20.0)
t, x = sim.run()

theta = x[:, 0]
omega = x[:, 1]

# Time series
plt.figure(figsize=(8, 4))
plt.plot(t, theta, label="Angle (rad)")
plt.plot(t, omega, label="Angular velocity")
plt.xlabel("Time")
plt.legend()
plt.title("B2: Large-Angle Pendulum")
plt.show()

# Phase portrait
plt.figure(figsize=(4, 4))
plt.plot(theta, omega)
plt.xlabel("θ")
plt.ylabel("ω")
plt.title("Phase Portrait")
plt.show()
