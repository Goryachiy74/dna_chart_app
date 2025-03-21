import os
import glob
import pandas as pd
import matplotlib.pyplot as plt

BOUNDARIES = [
    (37, 'red', 'L1/L2 boundary'),
    (42, 'green', 'H1/H2 boundary'),
    (47, 'purple', 'H2/H3 boundary')
]

DEFAULT_AVG_POINTS = 100
DEFAULT_MOVING_WINDOW = 50

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

    def process_and_plot(self, file):
        try:
            df = pd.read_csv(file)
            if df.empty:
                print(f"⚠️ Skipping {file}: File is empty.")
                return

            df['Start (Mb)'] = df['Start'] / 1e6

            # === SIMPLE AVERAGE ===
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

            # === SAVE SIMPLE AVERAGE AS CSV ===
            output_csv = os.path.join(self.output_dir, f'{os.path.basename(file).replace(".csv", "_simple_average.csv")}')
            simple_avg_df = pd.DataFrame({
                'Start': avg_start,
                'End': avg_end,
                'GC_Content': avg_gc_content
            })
            simple_avg_df.to_csv(output_csv, sep='\t', index=False)  # Use tab separation
            print(f"✅ Simple average data saved to {output_csv}")

            # === ORIGINAL PLOT ===
            plt.figure(figsize=(16, 8))
            plt.plot(df['Start (Mb)'], df['GC_Content'], label='GC Content (Original)', color='blue', alpha=0.7)

            for boundary, color, label in BOUNDARIES:
                plt.axhline(boundary, color=color, linestyle='--', label=label)
                plt.fill_between(df['Start (Mb)'], boundary, boundary + 5, color=color, alpha=0.1)

            plt.title(f'GC Content - {os.path.basename(file)} (Original)')
            plt.xlabel('Start (Mb)')
            plt.ylabel('GC Content (%)')
            plt.legend(loc='upper right')
            plt.grid(True)

            output_file_original = os.path.join(self.output_dir, f'{os.path.basename(file).replace(".csv", "_original.png")}')
            plt.savefig(output_file_original, format='png', dpi=300)
            plt.close()
            print(f"✅ Original plot saved to {output_file_original}")

            # === SIMPLE AVERAGE PLOT ===
            plt.figure(figsize=(16, 8))
            plt.plot(df['Start (Mb)'], df['GC_Content'], label='GC Content (Original)', color='blue', alpha=0.5)

            plt.step(
                [x / 1e6 for x in avg_start],  # Convert base pairs to Mb
                avg_gc_content,
                label=f'Simple Average ({avg_points} points)',
                color='black',
                where='mid',
                linewidth=2
            )

            for boundary, color, label in BOUNDARIES:
                plt.axhline(boundary, color=color, linestyle='--', label=label)
                plt.fill_between(df['Start (Mb)'], boundary, boundary + 5, color=color, alpha=0.1)

            plt.title(f'GC Content - {os.path.basename(file)} (Simple Average)')
            plt.xlabel('Start (Mb)')
            plt.ylabel('GC Content (%)')
            plt.legend(loc='upper right')
            plt.grid(True)

            output_file_simple_avg = os.path.join(self.output_dir, f'{os.path.basename(file).replace(".csv", "_simple_average.png")}')
            plt.savefig(output_file_simple_avg, format='png', dpi=300)
            plt.close()
            print(f"✅ Simple average plot saved to {output_file_simple_avg}")

            # === MOVING AVERAGE PLOT ===
            df['Moving_Avg_GC_Content'] = df['GC_Content'].rolling(window=self.moving_window, min_periods=1).mean()

            plt.figure(figsize=(16, 8))
            plt.plot(df['Start (Mb)'], df['GC_Content'], label='GC Content (Original)', color='blue', alpha=0.5)

            plt.plot(df['Start (Mb)'], df['Moving_Avg_GC_Content'],
                     label=f'Moving Average (Window={self.moving_window})',
                     color='orange', linewidth=2)

            for boundary, color, label in BOUNDARIES:
                plt.axhline(boundary, color=color, linestyle='--', label=label)
                plt.fill_between(df['Start (Mb)'], boundary, boundary + 5, color=color, alpha=0.1)

            plt.title(f'GC Content - {os.path.basename(file)} (Moving Average)')
            plt.xlabel('Start (Mb)')
            plt.ylabel('GC Content (%)')
            plt.legend(loc='upper right')
            plt.grid(True)

            output_file_moving_avg = os.path.join(self.output_dir, f'{os.path.basename(file).replace(".csv", "_moving_average.png")}')
            plt.savefig(output_file_moving_avg, format='png', dpi=300)
            plt.close()
            print(f"✅ Moving average plot saved to {output_file_moving_avg}")

        except FileNotFoundError:
            print(f"❌ File not found: {file}")
        except pd.errors.EmptyDataError:
            print(f"❌ File is empty: {file}")
        except Exception as e:
            print(f"❌ Error processing {file}: {e}")

    def process_all(self):
        files = self.get_files()
        if not files:
            print("⚠️ No files matched the pattern. Please check the input directory and filename format.")
            return
        for file in files:
            self.process_and_plot(file)

# Example usage:
# plotter = IsochorePlotter('path_to_input', 'path_to_output', avg_points=100, moving_window=50)
# plotter.process_all()
