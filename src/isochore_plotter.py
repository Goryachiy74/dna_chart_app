import os
import glob
import pandas as pd
import matplotlib.pyplot as plt

# Define isochore class boundaries and colors
BOUNDARIES = [
    (37, 'blue', 'L1'),
    (41, 'cyan', 'L2'),
    (46, 'yellow', 'H1'),
    (53, 'orange', 'H2'),
    (100, 'red', 'H3')
]

DEFAULT_AVG_POINTS = 100
DEFAULT_MOVING_WINDOW = 50

# Function to determine color based on isochore class
def get_gc_class_color(gc_content):
    if gc_content < 37:
        return 'blue'
    elif 37 <= gc_content < 41:
        return 'cyan'
    elif 41 <= gc_content < 46:
        return 'yellow'
    elif 46 <= gc_content < 53:
        return 'orange'
    elif gc_content >= 53:
        return 'red'
    return 'gray'

class IsochorePlotter:
    def __init__(self, input_dir, output_dir, avg_points=DEFAULT_AVG_POINTS, moving_window=DEFAULT_MOVING_WINDOW):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.avg_points = avg_points
        self.moving_window = moving_window
        os.makedirs(self.output_dir, exist_ok=True)

    def get_files(self):
        file_pattern = os.path.join(self.input_dir, 'isochores_output_*.csv')
        files = glob.glob(file_pattern)
        if not files:
            print("⚠️ No files found in the input directory.")
        return files

    def plot_original(self, df, file):
        plt.figure(figsize=(16, 8))

        colors = [get_gc_class_color(gc) for gc in df['GC_Content']]
        if len(df) > 1:
            bar_width = 0.9 * (df['Start (Mb)'].iloc[1] - df['Start (Mb)'].iloc[0])
        else:
            bar_width = 0.1

        for i in range(len(df)):
            plt.bar(
                df['Start (Mb)'].iloc[i],
                df['GC_Content'].iloc[i],
                width=bar_width,
                color=colors[i],
                edgecolor=None,
                zorder=3
            )

        for boundary, color, label in BOUNDARIES:
            plt.axhline(boundary, color=color, linestyle='--', label=label, zorder=2)
            plt.fill_between(df['Start (Mb)'], boundary, boundary + 5, color=color, alpha=0.1, zorder=1)

        plt.title(f'GC Content - {os.path.basename(file)} (Original)')
        plt.xlabel('Start (Mb)')
        plt.ylabel('GC Content (%)')
        plt.legend(loc='upper right')
        plt.grid(True, zorder=0)

        output_file = os.path.join(self.output_dir, f"{os.path.basename(file).replace('.csv', '_original.png')}")
        plt.savefig(output_file, format='png', dpi=300)
        plt.close()
        print(f"✅ Original plot saved to {output_file}")

    def plot_simple_average(self, df, file):
        avg_points = min(self.avg_points, len(df))
        avg_gc_content = [
            df['GC_Content'].iloc[i:i + avg_points].mean()
            for i in range(0, len(df), avg_points)
        ]
        avg_start = [
            df['Start'].iloc[i]
            for i in range(0, len(df), avg_points)
        ]
        avg_end = [
            df['Start'].iloc[min(i + avg_points - 1, len(df) - 1)]
            for i in range(0, len(df), avg_points)
        ]

        plt.figure(figsize=(16, 8))
        plt.plot(df['Start (Mb)'], df['GC_Content'], label='GC Content (Original)', color='lightgray', alpha=0.5)

        plt.step(
            [x / 1e6 for x in avg_start],
            avg_gc_content,
            label=f'Simple Average ({avg_points} points)',
            color='black',
            linewidth=2,
            where='mid'
        )

        for boundary, color, label in BOUNDARIES:
            plt.axhline(boundary, color=color, linestyle='--', label=label, zorder=2)
            plt.fill_between(df['Start (Mb)'], boundary, boundary + 5, color=color, alpha=0.1, zorder=1)

        plt.title(f'GC Content - {os.path.basename(file)} (Simple Average)')
        plt.xlabel('Start (Mb)')
        plt.ylabel('GC Content (%)')
        plt.legend(loc='upper right')
        plt.grid(True, zorder=0)

        output_file = os.path.join(self.output_dir, f"{os.path.basename(file).replace('.csv', '_simple_average.png')}")
        plt.savefig(output_file, format='png', dpi=300)
        plt.close()
        print(f"✅ Simple average plot saved to {output_file}")

    def plot_histogram(self, df, file):
        plt.figure(figsize=(16, 8))

        # ✅ Histogram of GC Content distribution
        plt.hist(
            df['GC_Content'],
            bins=50,
            color='skyblue',
            edgecolor='black'
        )

        for boundary, color, label in BOUNDARIES:
            plt.axvline(boundary, color=color, linestyle='--', label=label)

        plt.title(f'GC Content Distribution - {os.path.basename(file)}')
        plt.xlabel('GC Content (%)')
        plt.ylabel('Frequency')
        plt.legend(loc='upper right')
        plt.grid(True)

        output_file = os.path.join(self.output_dir, f"{os.path.basename(file).replace('.csv', '_histogram.png')}")
        plt.savefig(output_file, format='png', dpi=300)
        plt.close()
        print(f"✅ Histogram saved to {output_file}")

    def process_and_plot(self, file):
        df = pd.read_csv(file)
        df['Start (Mb)'] = df['Start'] / 1e6

        self.plot_original(df, file)
        self.plot_simple_average(df, file)
        self.plot_histogram(df, file)

    def process_all(self):
        files = self.get_files()
        if not files:
            print("⚠️ No files matched the pattern.")
            return
        for file in files:
            self.process_and_plot(file)

# Example usage:
# plotter = IsochorePlotter('path_to_input', 'path_to_output', avg_points=100, moving_window=50)
# plotter.process_all()
