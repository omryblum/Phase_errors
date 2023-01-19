import numpy as np
import matplotlib.pyplot as plt

# Create Fibonachi serie

fib = [1, 2]

for ind in np.arange(2, 30):
    fib.append(fib[-2] + fib[-1])

fib = np.array(fib)

fig, ax = plt.subplots(2, 2)
fig.axes[0].plot(fib, linewidth=2)
fig.axes[2].plot(np.log(fib), linewidth=2)
fig.axes[3].plot(fib[1:]/fib[:-1], linewidth=2)
[ax.grid() for ax in fig.axes]
plt.show()