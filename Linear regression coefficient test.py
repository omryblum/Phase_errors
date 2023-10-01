import numpy as np
import matplotlib.pyplot as plt

a = 1 * np.linspace(-1, 1, 100)
b = np.sum(a**2)**(1/2)
print('value is ', b)

plt.plot(a)
plt.show()
