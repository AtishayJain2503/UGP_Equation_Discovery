import matplotlib.pyplot as plt

from equations.damped_oscillator import DampedOscillator
from data.simulator import Simulator

# Create system
system = DampedOscillator(omega=1.0, damping=0.2)

# Simulate
sim = Simulator(system, dt=0.01, T=20.0)
t, x = sim.run()

# Extract states
pos = x[:, 0]
vel = x[:, 1]

# Plot time series
plt.figure(figsize=(8, 4))
plt.plot(t, pos, label="Position")
plt.plot(t, vel, label="Velocity")
plt.xlabel("Time")
plt.legend()
plt.title("A2: Damped Harmonic Oscillator")
plt.show()

# Phase portrait
plt.figure(figsize=(4, 4))
plt.plot(pos, vel)
plt.xlabel("Position")
plt.ylabel("Velocity")
plt.title("Phase Portrait")
plt.show()
