import numpy as np
import matplotlib.pyplot as plt
import itertools

class RobotSeqOptimizer():
    def __init__(self):
        """defining variables"""
        self.times = {'LP2AL': 3, 'AL2MU': 3, 'SWAP': 4, 'LP2MUbySwaps': 15}
        # self.wafers = {'MU1': {15: 3, 120: 3}, 'MU2': {15: 6, 120: 2}, 'Any': {40: 3}}  # grouped wafers by expected recipe time
        # self.wafers = {'MU1': {10: 4, 100: 2}, 'MU2': {20: 2, 100: 2}, 'Any': {40: 3}}  # grouped wafers by expected recipe time
        self.wafers = {'MU1': {10: 5, 60: 2}, 'MU2': {20: 4, 100: 1}, 'Any': {40: 3}}  # grouped wafers by expected recipe time
        self.shortest_path = []
        self.costs = {}

        self.time = []
        self.MU1_occupancy = []
        self.MU2_occupancy = []
        self.robot_busy = []
        self.possibilities = []  # (MU1, MU2)

    def possible_wafer_measurement_order(self):
        wafers = self.wafers.copy()

        wafers_seq = []
        for x in wafers['MU1']:
            for y in np.arange(wafers['MU1'][x]):
                wafers_seq.append((x, 'MU1'))

        for x in wafers['MU2']:
            for y in np.arange(wafers['MU2'][x]):
                wafers_seq.append((x, 'MU2'))

        self.possibilities = [[x] for x in list(set(wafers_seq))]
        while True:
            initial_seq = self.possibilities.pop(0)
            left_wafers = wafers_seq.copy()
            for x in initial_seq:
                left_wafers.pop(left_wafers.index(x))
            options = list(set(left_wafers))
            if not bool(options):
                break

            for x in options:
                self.possibilities.append(initial_seq + [x])

        print(str(len(self.possibilities)+1)+' sequence options available to be simulated')

    def calculate_time_from_wafer_list(self, wafers_seq, mu1_initial_delay=0, mu2_initial_delay=0, robot_initial_delay=0):
        mu1_ready_time = mu1_initial_delay
        mu2_ready_time = mu1_initial_delay
        robot_ready_time = robot_initial_delay

        for wafer in wafers_seq:
            if wafer[1] == 'MU1':
                next_wafer_time = max(robot_ready_time, mu1_ready_time)
                robot_ready_time = next_wafer_time + self.times['LP2MUbySwaps']
                mu1_ready_time = next_wafer_time + wafer[0]
            if wafer[1] == 'MU2':
                next_wafer_time = max(robot_ready_time, mu2_ready_time)
                robot_ready_time = next_wafer_time + self.times['LP2MUbySwaps']
                mu2_ready_time = next_wafer_time + wafer[0]

        return max(mu1_ready_time, mu2_ready_time)

    def plot_wafer_sequence(self, wafers_seq, mu1_initial_delay=0, mu2_initial_delay=0, robot_initial_delay=0, seq_time=10000):
        mu1_ready_time = mu1_initial_delay
        mu2_ready_time = mu1_initial_delay
        robot_ready_time = robot_initial_delay
        self.time = np.linspace(0, seq_time+1, seq_time+2)  # time in 1 sec intervals
        self.MU1_occupancy = np.zeros(self.time.size)
        self.MU2_occupancy = np.zeros(self.time.size)
        self.robot_busy = np.zeros(self.time.size)

        for wafer in wafers_seq:
            if wafer[1] == 'MU1':
                next_wafer_time = max(robot_ready_time, mu1_ready_time)
                robot_ready_time = next_wafer_time + self.times['LP2MUbySwaps']
                self.robot_busy[np.round(next_wafer_time):np.round(robot_ready_time)-1] = 1
                mu1_ready_time = next_wafer_time + wafer[0]
                self.MU1_occupancy[np.round(next_wafer_time):np.round(mu1_ready_time)-1] = 1
            if wafer[1] == 'MU2':
                next_wafer_time = max(robot_ready_time, mu2_ready_time)
                robot_ready_time = next_wafer_time + self.times['LP2MUbySwaps']
                self.robot_busy[np.round(next_wafer_time):np.round(robot_ready_time)-1] = 1
                mu2_ready_time = next_wafer_time + wafer[0]
                self.MU2_occupancy[np.round(next_wafer_time):np.round(mu2_ready_time)-1] = 1

        self.MU1_occupancy[0] = 0
        self.MU2_occupancy[0] = 0
        self.robot_busy[0] = 0

    def select_best_wafer_path(self):
        self.possible_wafer_measurement_order()
        run_times = []
        min_run_time = 1e6
        for seq in self.possibilities:
            run_time = self.calculate_time_from_wafer_list(seq, 0, 0, 0)
            run_times.append(run_time)
            if run_time < min_run_time:
                min_run_time = run_time
                best_seq = seq

        fig, ax = plt.subplots(2, 2)
        ax[0, 0].plot(run_times)
        ax[0, 0].set_title('possible sequence timings')
        ax[0, 0].set_ylabel('Time [sec]')
        ax[0, 0].grid(),

        ax[0, 1].hist(run_times, 30)
        ax[0, 1].set_title('sequence histogram')
        ax[0, 1].set_xlabel('Time [sec]')
        ax[0, 1].grid(),

        self.plot_wafer_sequence(best_seq, 0, 0, 0, min_run_time)

        # fig, ax = plt.subplots(1, 1)
        ax[1, 1].plot(self.time, self.MU1_occupancy + 6)
        ax[1, 1].plot(self.time, self.MU2_occupancy + 3)
        ax[1, 1].plot(self.time, self.robot_busy)
        ax[1, 1].set_yticks([0, 3, 6], ['Robot', 'MU1', 'MU2'])
        ax[1, 1].set_xlabel('Time [sec]')
        ax[1, 1].set_title('best sequence')
        ax[1, 1].grid(),

        plt.show()

r1 = RobotSeqOptimizer()
r1.select_best_wafer_path()
