import pandas as pd
import matplotlib.pyplot as plt
import os
import glob


class ChartGenerator:
    def __init__(self, input_dir, output_dir, threshold):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.threshold = threshold
        os.makedirs(self.output_dir, exist_ok=True)

    def get_files(self):
        all_files = glob.glob(os.path.join(self.input_dir, '*.csv'))
        segment_files = [f for f in all_files if 'segments_output_' in f]
        merged_files = [f for f in all_files if 'merged_segments_output_' in f]
        return segment_files, merged_files

    def create_chart(self, file_path):
        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            print(f"Failed to load {file_path}: {e}")
            return

        if 'Best Word' not in df.columns:
            print(f"Skipping {file_path} - 'Best Word' column not found.")
            return

        # Count occurrences of each word
        word_counts = df['Best Word'].value_counts().reset_index()
        word_counts.columns = ['Word', 'Count']

        # Filter based on threshold
        word_counts = word_counts[word_counts['Count'] >= self.threshold]

        if word_counts.empty:
            print(f"No significant words to plot for {file_path}")
            return

        plt.figure(figsize=(12, 6))
        plt.bar(word_counts['Word'], word_counts['Count'], color='green')
        plt.xlabel('Word')
        plt.ylabel('Count')
        plt.title(f"Word Frequency - {os.path.basename(file_path)}")
        plt.xticks(rotation=45)

        output_file = os.path.join(self.output_dir, os.path.basename(file_path).replace('.csv', '.png'))
        plt.savefig(output_file, format='png')
        plt.close()

        print(f"✅ Chart saved to {output_file}")

    def process_files(self):
        segment_files, merged_files = self.get_files()

        if not segment_files and not merged_files:
            print("⚠️ No matching files found.")
            return

        print("\nProcessing segments_output_ files:")
        for file_path in segment_files:
            self.create_chart(file_path)

        print("\nProcessing merged_segments_output_ files:")
        for file_path in merged_files:
            self.create_chart(file_path)

        print("\n✅ All charts created and saved!")
