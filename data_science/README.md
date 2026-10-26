# 📊 Data Science, Machine Learning & Scientific Computing

A curated collection of practical Python scripts demonstrating numerical computation with **NumPy**, tabular data manipulation with **Pandas**, exploratory visualization with **Matplotlib**, descriptive analytics with **Statistics**, and classical machine learning models with **Scikit-Learn**.

---

## 📂 Module Catalog

### 1. 🔢 NumPy & Vectorized Numerical Computing

| Module | Description & Key Concepts |
| :--- | :--- |
| [`numpy_array_creation.py`](./numpy_array_creation.py) | Array instantiation from Python iterables, dimensions, and shape inspection. |
| [`numpy_data_types.py`](./numpy_data_types.py) | Data types (`int32`, `float64`, `bool_`), type conversion (`astype`), and memory precision. |
| [`numpy_basic_operations.py`](./numpy_basic_operations.py) | Element-wise arithmetic, scalar operations, and array broadcasting. |
| [`numpy_math_operations.py`](./numpy_math_operations.py) | Universal mathematical functions (ufuncs): trigonometric, logarithmic, square roots, and powers. |
| [`numpy_array_indexing.py`](./numpy_array_indexing.py) | 1D & 2D array indexing, multi-axis slicing (`arr[row, col]`), and boolean masking. |
| [`numpy_array_formatting.py`](./numpy_array_formatting.py) | Controlling console printing behavior, float precision formatting, and suppression of scientific notation. |

### 2. 🐼 Pandas & Tabular Data Manipulation

| Module | Description & Key Concepts |
| :--- | :--- |
| [`pandas_series_from_list.py`](./pandas_series_from_list.py) | One-dimensional labeled array creation, index alignment, and data access. |
| [`pandas_dataframe_from_dict.py`](./pandas_dataframe_from_dict.py) | Constructing two-dimensional tabular DataFrames from nested dictionaries and key-value records. |
| [`pandas_dataframe_exploration.py`](./pandas_dataframe_exploration.py) | Exploratory data analysis (EDA): previewing records (`head()`, `tail()`), structure inspection (`info()`, `shape`), and summary statistics. |
| [`pandas_read_csv_json.py`](./pandas_read_csv_json.py) | Ingesting external structured formats: parsing CSV (`read_csv`) and JSON (`read_json`) records into DataFrames. |

### 3. 🤖 Machine Learning (Scikit-Learn)

| Module | Description & Key Concepts |
| :--- | :--- |
| [`kmeans_clustering.py`](./kmeans_clustering.py) | Unsupervised partitioning: centroid-based clustering using Scikit-Learn's `KMeans`, cluster label assignment, and inertia evaluation. |
| [`logistic_regression.py`](./logistic_regression.py) | Supervised binary classification: feature preparation, train/test splitting (`train_test_split`), model fitting, and accuracy score evaluation. |

### 4. 📈 Visualization & Statistical Analysis

| Module | Description & Key Concepts |
| :--- | :--- |
| [`matplotlib_visualization.py`](./matplotlib_visualization.py) | Data plotting with Matplotlib: creating line plots, bar charts, custom axes labels, titles, and figure legends. |
| [`statistics_operations.py`](./statistics_operations.py) | Central tendency and dispersion calculations using Python's standard `statistics` module (mean, median, mode, variance, stdev). |

---

## 🚀 Getting Started

### Prerequisites

Ensure you have the required scientific libraries installed. From the repository root:

```powershell
pip install numpy pandas matplotlib scikit-learn
```

*(Alternatively: `pip install -r requirements.txt`)*

### Running Modules

Execute any script directly from the terminal.

#### From the Repository Root:
```powershell
# NumPy
python data_science/numpy_array_creation.py
python data_science/numpy_basic_operations.py

# Pandas
python data_science/pandas_dataframe_exploration.py
python data_science/pandas_read_csv_json.py

# Machine Learning
python data_science/logistic_regression.py
python data_science/kmeans_clustering.py

# Visualization & Stats
python data_science/statistics_operations.py
python data_science/matplotlib_visualization.py
```

#### From Within the `data_science/` Directory:
```powershell
cd data_science
python logistic_regression.py
```

---

## 🛠️ Standards & Best Practices

- **PEP 8 Compliance**: Consistent `snake_case` naming and zero whitespace in file names.
- **No Shadowing**: Module names avoid collisions with Python standard library packages (e.g., `statistics_operations.py` avoids shadowing built-in `statistics`).
- **Data Safety**: File paths resolve relative to the repository assets directory (`text_files/`) for reliable cross-platform execution.
