import matplotlib.pyplot as plt

from equations.duffing import DuffingOscillator
from data.simulator import Simulator

system = DuffingOscillator(alpha=1.0, beta=1.0, damping=0.1)
sim = Simulator(system, dt=0.01, T=30.0)
# print(system.alpha, system.beta, system.damping)

t, x = sim.run()
pos, vel = x[:, 0], x[:, 1]
plt.figure()
plt.plot(t, pos)
plt.xlabel("Time")
plt.ylabel("Position")
plt.title("Duffing Position")
plt.show()

plt.figure()
plt.plot(t, vel)
plt.xlabel("Time")
plt.ylabel("Velocity")
plt.title("Duffing Velocity")
plt.show()

plt.figure()
plt.plot(pos, vel)
plt.xlabel("Position")
plt.ylabel("Velocity")
plt.title("Phase Portrait")
plt.axis("equal")
plt.show()


# print("x shape:", x.shape)
# print("pos min/max:", pos.min(), pos.max())
# print("vel min/max:", vel.min(), vel.max())
