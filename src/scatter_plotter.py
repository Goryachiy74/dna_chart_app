import os
import glob
import pandas as pd
import plotly.express as px

class ScatterPlotter:
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def get_files(self):
        return glob.glob(os.path.join(self.input_dir, 'segments_output_*.csv')) + \
            glob.glob(os.path.join(self.input_dir, 'merged_segments_output_*.csv'))

    def process_and_plot(self, file):
        df = pd.read_csv(file)
        fig = px.scatter(df, x='Start', y='Length', color='Best Word')
        output_file = os.path.join(self.output_dir, os.path.basename(file).replace('.csv', '.html'))
        fig.write_html(output_file)
        print(f"✅ Scatter plot saved to {output_file}")

    def process_all(self):
        files = self.get_files()
        for file in files:
            self.process_and_plot(file)
