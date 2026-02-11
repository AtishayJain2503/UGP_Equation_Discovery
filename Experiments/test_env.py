import numpy as np
import scipy
import matplotlib.pyplot as plt

print("NumPy:", np.__version__)
print("SciPy:", scipy.__version__)

x = np.linspace(0, 10, 100)
plt.plot(x, np.sin(x))
plt.show()
