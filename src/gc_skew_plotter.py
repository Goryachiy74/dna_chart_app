import os
import glob
import pandas as pd
import matplotlib.pyplot as plt


class GCSkewPlotter:
    def __init__(self, input_dir, output_dir, sequence_file=None):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.sequence_file = sequence_file
        os.makedirs(self.output_dir, exist_ok=True)

    def get_files(self):
        return glob.glob(os.path.join(self.input_dir, 'segments_output_*.csv')) + \
            glob.glob(os.path.join(self.input_dir, 'merged_segments_output_*.csv'))

    def calculate_gc_skew(self, sequence):
        g_count = sequence.count('G')
        c_count = sequence.count('C')
        if g_count + c_count == 0:
            return 0
        return (g_count - c_count) / (g_count + c_count)

    def load_fna_sequence(self):
        if not self.sequence_file or not os.path.exists(self.sequence_file):
            print("⚠️ No sequence file selected or file not found.")
            return None

        try:
            print(f"🔎 Loading sequence data from {self.sequence_file}...")

            sequences = {}
            current_sequence = []
            current_id = None

            # ✅ Read .fna file line-by-line
            with open(self.sequence_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith(">"):
                        if current_id is not None:
                            sequences[current_id] = "".join(current_sequence)
                        current_id = line[1:]  # Remove ">"
                        current_sequence = []
                    else:
                        current_sequence.append(line)

                # Add the last sequence
                if current_id is not None:
                    sequences[current_id] = "".join(current_sequence)

            print(f"✅ Loaded {len(sequences)} sequences.")

            # ✅ Create DataFrame from FASTA data
            sequence_df = pd.DataFrame(list(sequences.items()), columns=['Start', 'Sequence'])

            # ✅ Attempt to convert 'Start' to integers (if possible)
            try:
                sequence_df['Start'] = sequence_df['Start'].astype(int)
            except ValueError:
                print("⚠️ Start values are not numeric; using index-based match instead.")
                # Create index-based key if Start is not numeric
                sequence_df['Index'] = range(len(sequence_df))
                sequence_df.set_index('Index', inplace=True)

            print(sequence_df.head())
            return sequence_df

        except Exception as e:
            print(f"❌ Error loading sequence file: {e}")
            return None

    def process_and_plot(self, file):
        try:
            df = pd.read_csv(file)
            print(f"\n🔎 Columns in {file}: {df.columns.tolist()}")

            if 'Start' not in df.columns:
                print(f"⚠️ Skipping {file} - Missing required 'Start' column")
                return

            # ✅ Load and merge sequence data
            sequence_data = self.load_fna_sequence()
            if sequence_data is not None:
                try:
                    # Try to merge on 'Start' if it's numeric
                    if 'Start' in sequence_data.columns:
                        df = df.merge(sequence_data, on='Start', how='left')
                    else:
                        # If merge fails, concatenate using index
                        df = pd.concat([df, sequence_data], axis=1)
                except Exception as merge_error:
                    print(f"⚠️ Merge failed: {merge_error}. Trying index-based match...")
                    df = pd.concat([df.reset_index(drop=True), sequence_data.reset_index(drop=True)], axis=1)

            if 'Sequence' not in df.columns or df['Sequence'].isna().all():
                print(f"⚠️ Skipping {file} - No sequence data after merge.")
                return

            # ✅ Calculate GC Skew
            df['GC_Skew'] = df['Sequence'].apply(self.calculate_gc_skew)

            # ✅ Plot GC Skew
            plt.figure(figsize=(16, 6))
            plt.plot(df['Start'], df['GC_Skew'], color='blue', label='GC Skew')

            plt.title(f'GC Skew - {os.path.basename(file)}')
            plt.xlabel('Start Position')
            plt.ylabel('GC Skew')
            plt.legend()
            plt.grid(True)

            # ✅ Save plot
            output_file = os.path.join(self.output_dir, os.path.basename(file).replace('.csv', '_gc_skew.png'))
            plt.savefig(output_file, format='png', dpi=300)
            plt.close()

            print(f"✅ GC Skew plot saved to {output_file}")

        except Exception as e:
            print(f"❌ Error processing {file}: {e}")

    def process_all(self):
        files = self.get_files()
        if not files:
            print("⚠️ No matching files found.")
            return

        print("\n🚀 Generating GC Skew plots:")
        for file in files:
            self.process_and_plot(file)

        print("\n✅ All GC Skew plots have been generated!")
