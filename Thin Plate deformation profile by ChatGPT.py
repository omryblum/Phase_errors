import numpy as np
from scipy.integrate import solve_bvp
import matplotlib.pyplot as plt

# Plate properties
E = 0.005e9  # Young's modulus for silicone in Pa
nu = 0.4     # Poisson's ratio for silicone
h = 0.0008   # Thickness in m

# Flexural rigidity
D = E * h**3 / (12 * (1 - nu**2))

# Define the Kirchhoff-Love plate equation
def fun(x, y, P):
    w, dwdx = y
    dw2dx2 = -1/(D * h**3) * (q(x, P) - D * h**3 * (dwdx**2))
    return np.array([dwdx, dw2dx2])

# Uniformly distributed load with internal compression force P
def q(x, P):
    return -P / (h * D)  # Load distribution with internal compression force

# Radial distances
r_values = np.linspace(0, D/2, num=10000)

# Boundary conditions: w(0) = 0 (at the center of the plate), dw/dx(0) = 0 (no bending at center)
def bc(ya, yb, P):
    return np.array([ya[0], yb[0]])

# Internal compression force as a free parameter
P = 1e-5  # Adjust the value of internal compression force as needed

# Solve the boundary value problem
sol = solve_bvp(lambda x, y: fun(x, y, P), lambda ya, yb: bc(ya, yb, P), r_values, [np.zeros_like(r_values), np.zeros_like(r_values)])

# Calculate the deflection along the radial distances
deflection = sol.sol(r_values)[0]

# Plot the results
plt.plot(r_values, deflection)
plt.xlabel('Radial Distance (m)')
plt.ylabel('Deflection (m)')
plt.title('Deflection of Thin Circular Plate with Internal Compression Force')
plt.grid(True)
plt.show()
