import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 3, 300)
y = 10 * x / (1 + x**2)

plt.plot(x, y)
plt.show()