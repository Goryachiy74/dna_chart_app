import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

BOUNDARIES = [
    (37, 'red', 'L1/L2 boundary'),
    (42, 'green', 'H1/H2 boundary'),
    (47, 'purple', 'H2/H3 boundary')
]

class IsochorePlotter:
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def get_files(self):
        file_pattern = os.path.join(self.input_dir, 'isochores_output_*.csv')
        return glob.glob(file_pattern)

    def process_and_plot(self, file):
        try:
            df = pd.read_csv(file)
            df['Start (Mb)'] = df['Start'] / 1e6

            plt.figure(figsize=(16, 8))
            plt.plot(df['Start (Mb)'], df['GC_Content'], label='GC Content', color='blue')

            for boundary, color, label in BOUNDARIES:
                plt.axhline(boundary, color=color, linestyle='--', label=label)

            plt.title(f'GC Content - {os.path.basename(file)}')
            plt.xlabel('Start (Mb)')
            plt.ylabel('GC Content (%)')
            plt.legend()
            plt.grid(True)

            output_file = os.path.join(self.output_dir, os.path.basename(file).replace('.csv', '.png'))
            plt.savefig(output_file, format='png', dpi=300)
            plt.close()

            print(f"✅ Isochore plot saved to {output_file}")

        except Exception as e:
            print(f"❌ Error processing {file}: {e}")

    def process_all(self):
        files = self.get_files()
        for file in files:
            self.process_and_plot(file)
