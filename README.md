# Graduation Rates at Texas Public Universities (2020-2022)

This repository contains data and analysis of **4-year graduation rates** at **Texas public universities** from **2020 to 2022**.

## Overview

The dataset provides insights into **graduation rates** across public universities in Texas, identifying trends, high-performing institutions, and areas for improvement. The analysis includes data cleaning, visualization, and database integration.

## Dataset

The dataset used in this analysis is located in the project folder and includes:

- `graduation_rates_at_public_universities_2020-2022.csv`: Raw data on **4-year graduation rates** at public universities in Texas from 2020 to 2022.

## Analysis

This project:
- Reads the dataset and transfers it to a **local phpMyAdmin MySQL database**.
- Performs data analysis and visualization using **Python, Pandas, and Matplotlib**.
- Identifies **the top** universities with the highest graduation rates.
- Highlights **the bottom 3** universities with the lowest graduation rates.
- Compares **all institutions** against the **average graduation rate**.

### Example Visualizations

**Top Public Institutions by Graduation Rate (2020-2022)**

![Figure 1](figure_1.jpg)


**Bottom 3 Public Institutions by Graduation Rate (2020-2022)**

![Bottom 3 Institutions](figure_2.jpg)

![figure #3.jpg](figure%20%233.jpg)

## Usage

To use this repository:

### 1. Install Python 3 and Dependencies

Ensure you have **Python 3.11** installed:  
[Download Python](https://www.python.org/downloads/)

Install the required Python packages:

```sh
pip install pandas matplotlib SQLAlchemy pymysql
```

### 2. Clone the Repository

```sh
git clone https://github.com/tcareer34/Team-BAS/tree/main
cd Graduation_Rates_Texas
```

### 3. Create a Local Database

1. Set up a **phpMyAdmin MySQL database**.
2. Update the **database connection settings** in `main.py`:

```python
hostname = 'localhost'
uname = 'root'
pwd = ''
dbname = 'bas final'
```

3. Ensure that the table name in `main.py` matches your MySQL database:

```python
table_name = 'public_institutions_graduation_rate'
```

### 4. Run the Analysis

Run the script to process the data and generate visualizations:

```sh
python main.py
```


