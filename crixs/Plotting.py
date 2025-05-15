import matplotlib.pyplot as plt
from cycler import cycler

import os
import subprocess
import platform


class Myplot:
    def __init__(self, style="seaborn-darkgrid", figsize=(8, 6), fontsize=12):

        science_style = {
            # Set color cycle
            "axes.prop_cycle": cycler(
                color=[
                    "#0072BD",
                    "#D95319",
                    "#EDB120",
                    "#7E2F8E",
                    "#77AC30",
                    "#4DBEEE",
                    "#A2142F",
                ]
            ),
            # Figure settings
            "figure.figsize": (3.6, 2.7),
            "figure.dpi": 300,
            "savefig.dpi": 300,
            "figure.autolayout": True,
            # Font sizes
            "axes.labelsize": 12,
            "xtick.labelsize": 12,
            "ytick.labelsize": 12,
            "legend.fontsize": 12,
            "font.size": 12,
            # X-axis settings
            "xtick.direction": "in",
            "xtick.major.size": 4,
            "xtick.major.width": 1.0,
            "xtick.minor.size": 2,
            "xtick.minor.width": 1.0,
            "xtick.minor.visible": True,
            "xtick.top": True,
            # Y-axis settings
            "ytick.direction": "in",
            "ytick.major.size": 4,
            "ytick.major.width": 1.0,
            "ytick.minor.size": 2,
            "ytick.minor.width": 1.0,
            "ytick.minor.visible": True,
            "ytick.right": True,
            # Line widths
            "axes.linewidth": 1.0,
            "grid.linewidth": 1.0,
            "lines.linewidth": 1.0,
            "lines.markersize": 6,
            # Legend settings
            "legend.frameon": False,
            # Error bar settings
            "errorbar.capsize": 3,
            # Font settings
            "ps.useafm": True,
            "pdf.compression": 0,
            "pdf.use14corefonts": True,
            "svg.fonttype": "path",
        }

        """Initialize the Plotter with default settings."""
        plt.style.use(science_style)

    def __getattr__(self, name):
        """Delegate all unknown attributes to plt."""
        return getattr(plt, name)

    def open_file(self, file_path):
        """Open the saved file using the default image viewer via subprocess."""
        system = platform.system()
        try:
            if system == "Darwin":  # macOS
                subprocess.run(["open", file_path])
            elif system == "Windows":  # Windows
                subprocess.run(["start", file_path], shell=True)
            else:  # Linux/Unix
                subprocess.run(["xdg-open", file_path])
        except Exception as e:
            print(f"Error opening file: {e}")

    def save(self, filename):
        """Save the figure."""
        plt.savefig(filename)

    def show(self, file_path="temp.svg", save_before_show=True, open_after_save=True):

        # Save a file in the current working directory
        current_working_directory = os.getcwd()
        file_path = os.path.join(current_working_directory, "temp.svg")

        if save_before_show and file_path:
            self.save(file_path)  # Call save() method to save the figure
        if open_after_save:
            self.open_file(file_path)  # Open the saved file after saving

        # plt.show()
