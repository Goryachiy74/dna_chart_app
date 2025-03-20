# 🧬 DNA Chart App

**DNA Chart App** is a powerful bioinformatics tool designed to analyze DNA sequences and generate insightful charts.  
The app supports multiple types of DNA analysis and visualization, including:  
✅ Word Frequency Analysis  
✅ Isochore GC Content Distribution  
✅ Scatter Plots  

Built with **Python** and a clean graphical user interface using **Tkinter**, this tool is ideal for genomic analysis and visualization.

---

## 📌 **Features**
### 🔎 **1. Word Frequency Chart**
- Analyzes DNA segments to calculate word frequency.  
- Filters based on a threshold value.  
- Generates a clean bar chart of the most common words.  

### 🧬 **2. Isochore GC Content Chart**
- Calculates the GC content across different segments.  
- Plots GC content against genomic positions.  
- Marks the classification boundaries (`L1/L2`, `H1/H2`, `H2/H3`).  

### 📊 **3. Scatter Plot**
- Visualizes DNA segment lengths vs. starting positions.  
- Interactive plots using **Plotly**.  
- Highlights best-matching DNA words.  

### 🎯 **4. View Saved Charts**
- Opens the saved charts folder directly from the app.  
- Works on **Windows, MacOS, and Linux**.  

---

## 🏗️ **Project Structure**
dna_chart_app/ ├── src/ │ ├── chart_generator.py # Word frequency chart logic │ ├── isochore_plotter.py # GC content calculation and plotting │ ├── scatter_plotter.py # Scatter plot generation │ ├── gui.py # GUI interface with Tkinter │ ├── main.py # CLI and GUI entry point ├── icons/ # Application icons ├── dist/ # Generated executable ├── build/ # PyInstaller build files ├── .gitignore # Git ignore file ├── README.md # Project documentation └── requirements.txt # Dependencies


---

## 🖥️ **Installation**
### 1️⃣ **Clone the Repository**
Clone the project from GitHub:
```bash
git clone https://github.com/your-username/dna_chart_app.git
cd dna_chart_app```

2️⃣ Set Up Virtual Environment
Create and activate a virtual environment:
```python -m venv venv```

# Activate it:
# Windows

```.\venv\Scripts\activate```

# MacOS / Linux

```source venv/bin/activate```

3️⃣ Install Dependencies
Install the required dependencies:
```pip install -r requirements.txt```

4️⃣ Run the App
To launch the GUI:
```python src/main.py```

