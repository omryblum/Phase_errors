import numpy as np

a = {'Oram': 46, 'Yair': 42, 'Yaakov': 52, 'Oded': 76, 'Eyal': 89, 'Eden': 73}
b = {'Meir': 61, 'Mark': 7, 'Matan': 8, 'Or': 50, 'Anatoli': 55, 'Alon': 67}

c = {'Eden': 73, 'Or': 50, 'Eyal': 89, 'Anatoli': 55, 'Alon': 67}

# np.random.permutation(list(c.keys()))

for num, team in enumerate([a, b, c]):
    print(f'team {num} mean is {np.mean(list(team.values())):.0f} and variance is {np.var(list(team.values())):.0f}')


