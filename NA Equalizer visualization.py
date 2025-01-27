import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import griddata

class PolarInterpolationPlotter:
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)
        self.theta = self.df['Azimuth'].values
        self.r = self.df['IA'].values
        wavelength = self.df.columns[2:].to_numpy()
        self.wavelength = [wavelength[int(wavelength.shape[0]*0)], wavelength[int(wavelength.shape[0]*0.05)], wavelength[int(wavelength.shape[0]*0.1)]]
        self.wavelength_num = wavelength.astype(float)

    def convert_to_cartesian(self):
        self.y = self.r * np.cos(np.radians(self.theta))
        self.x = self.r * np.sin(np.radians(self.theta))

    def interpolate_data(self):
        self.x_interp = np.linspace(min(self.x), max(self.x), 100)
        self.y_interp = np.linspace(min(self.y), max(self.y), 100)
        self.x_grid, self.y_grid = np.meshgrid(self.x_interp, self.y_interp)

        self.intensity_grids = []
        for wavelength in self.wavelength:
            intensity = self.df[wavelength].values
            intensity_grid = griddata((self.x, self.y), intensity, (self.x_grid, self.y_grid), method='cubic')
            self.intensity_grids.append(intensity_grid)

    def plot_NA(self):
        fig, ax = plt.subplots(2, len(self.wavelength), figsize=(12, 6))

        for i, (wavelength, intensity_grid) in enumerate(zip(self.wavelength, self.intensity_grids)):
            sc = ax[0, i].scatter(self.x, self.y, c=self.df[wavelength].values, cmap='viridis')
            ax[0, i].set_title(f'Original {wavelength}nm')
            ax[0, i].set_xlabel('Azimuth')
            ax[0, i].set_ylabel('AOI')
            ax[0, i].set_aspect('equal')
            fig.colorbar(sc, ax=ax[0, i])

            c = ax[1, i].pcolormesh(self.x_grid, self.y_grid, intensity_grid, shading='auto', cmap='viridis')
            ax[1, i].set_title(f'Interpolated {wavelength}nm')
            ax[1, i].set_xlabel('Azimuth')
            ax[1, i].set_ylabel('AOI')
            ax[1, i].set_aspect('equal')
            fig.colorbar(c, ax=ax[1, i])

        plt.tight_layout()
        plt.show()

    def plot_spectra(self):
        fig, ax = plt.subplots(1, 1, figsize=(12, 6))

        new_df = self.df.iloc[self.r<7][self.df.columns[2:]].to_numpy()

        for i in range(0, new_df.shape[0]):
            color = plt.cm.viridis(i / (new_df.shape[0]+ 1))  # Normalize the index for colormap
            ax.plot(self.wavelength_num, new_df[i,:], label=f'Az {self.theta[i]}, Rad {self.r[i]}', color=color)
        ax.plot(self.wavelength_num, np.mean(new_df, axis=0), label=f'Averaged NA signal', color='black', linewidth=4)

        # new_df.plot(ax=ax, marker='o', linestyle='-', title='Selected Rows Plot')

        # You can also customize the first subplot further
        ax.set_xlabel('Wavelength')
        ax.set_ylabel('Reflectivity')
        ax.set_title('Spectra per NA ray')
        # ax.legend(loc='upper right')
        ax.grid(True)

        plt.tight_layout()
        plt.show()

    def plot_relative_energy(self):
        fig, ax = plt.subplots(1, 2, figsize=(12, 6))

        new_df = self.df.iloc[self.r < 7][self.df.columns[2:]].to_numpy()
        new_df = np.flip(np.sort(new_df, axis=0), axis=0)
        new_df = (new_df / np.sum(new_df, axis=0)) - 1 / new_df.shape[0]
        new_df = np.cumsum(new_df, axis=0)

        for i in range(0, new_df.shape[1]):
            color = plt.cm.viridis(i / (new_df.shape[1] + 1))  # Normalize the index for colormap
            ax[0].plot(np.linspace(0, 100, new_df.shape[0]), new_df[:, i], label=f'wl {self.wavelength_num[i]}',
                       color=color)

        # You can also customize the first subplot further
        ax[0].set_xlabel('NA rays #')
        ax[0].set_ylabel('Reflectivity')
        ax[0].set_title('Energy over smooth NA')
        # ax[0].legend(loc='upper right')
        ax[0].grid(True)

        # plotting energy over smooth NA at 10% top rays
        for i in range(1, 10):
            color = plt.cm.viridis(i / 10)  # Normalize the index for colormap
            ax[1].plot(self.wavelength_num, new_df[int(float(i) / 10 * new_df.shape[0]), :],
                       label=f'{i * 10}% energy curve', color=color)

        ax[1].set_xlabel('Wavelength')
        ax[1].set_ylabel('Energy non symmetry')
        ax[1].set_title('Energy over smooth NA at 10% top rays, Most NA sensitive wavelength')
        ax[1].legend(loc='upper right')
        ax[1].grid(True)

        plt.tight_layout()
        plt.show()

    def plot_abs_energy(self):
        fig, ax = plt.subplots(1, 2, figsize=(12, 6))

        new_df = self.df.iloc[self.r < 7][self.df.columns[2:]].to_numpy()
        new_df = np.flip(np.sort(new_df, axis=0), axis=0)
        new_df_sum = np.mean(new_df, axis=0)
        new_df = (new_df / np.sum(new_df, axis=0)) - 1 / new_df.shape[0]
        new_df = np.cumsum(new_df, axis=0)

        for i in range(0, new_df.shape[1]):
            color = plt.cm.viridis(i / (new_df.shape[1] + 1))  # Normalize the index for colormap
            ax[0].plot(np.linspace(0, 100, new_df.shape[0]), new_df[:, i], label=f'wl {self.wavelength_num[i]}', color=color)

        # You can also customize the first subplot further
        ax[0].set_xlabel('NA rays %')
        ax[0].set_ylabel('Additional energy %')
        ax[0].set_title('Energy over smooth NA %')
        # ax[0].legend(loc='upper right')
        ax[0].grid(True)

        # plotting energy over smooth NA at 10% top rays
        for i in range(1, 4):
            color = plt.cm.viridis(i / 3)  # Normalize the index for colormap
            ax[1].plot(self.wavelength_num, new_df_sum * new_df[int(float(i)/10 * new_df.shape[0]), :], label=f'{i*10}% energy curve', color=color)

        ax[1].set_xlabel('Wavelength')
        ax[1].set_ylabel('Total reflectivity above mean')
        ax[1].set_title('Energy over smooth NA at 10% of rays, Most sensitive WL')
        ax[1].legend(loc='upper right')
        ax[1].grid(True)

        plt.tight_layout()
        plt.show()


# Usage
folder_path = r"C:\Users\omry-b\Nova\Project Management (DMD) - General\SA Product Line\Sustain\Investigations\NA induced T2T\NA Grids reflectivity\\"
file_path = folder_path+r'Silicon 18A - Oblique 0_Xpol.csv'
plotter = PolarInterpolationPlotter(file_path)
plotter.convert_to_cartesian()
plotter.interpolate_data()
plotter.plot_NA()
plotter.plot_spectra()
# plotter.plot_relative_energy()
plotter.plot_abs_energy()
