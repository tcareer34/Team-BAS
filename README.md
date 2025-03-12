# Graduation Rates at Texas Public Universities (2020-2022)

This repository contains data and analysis of **4-year graduation rates** at **Texas public universities** from **2020 to 2022**.

## Overview

The dataset provides insights into **graduation rates** across public universities in Texas, identifying trends, high-performing institutions, and areas for improvement. The analysis includes data cleaning, visualization, and database integration.

## Dataset

The dataset used in this analysis is located in the project folder and includes:

- `graduation_rates_at_public_universities_2020-2022.csv`: Raw data on **4-year graduation rates** at public universities in Texas from 2020 to 2022 located at: https://data.austintexas.gov/api/views/59bi-74ad/rows.csv?accessType=DOWNLOAD

## Analysis

This project:
- Reads the dataset and transfers it to a **local phpMyAdmin MySQL database**.
- Performs data analysis and visualization using **Python, Pandas, and Matplotlib**.
- Identifies **the top** universities with the highest graduation rates.
- Highlights **the bottom 3** universities with the lowest graduation rates.
- Compares **all institutions** against the **average graduation rate**.

## Example Visualizations

### <u>**Top Public Institutions by Graduation Rate (2020-2022)**</u>

![Top 3 Public Institution](https://github.com/tcareer34/Team-BAS/blob/Team_Test/Figure_1.png)



### **Top 3 Public Institutions by Graduation Rate (2020-2022)**

![Top 3 Public Institution](https://github.com/tcareer34/Team-BAS/blob/Team_Test/Figure_2.png)



### **Bottom 3 Public Institutions by Graduation Rate (2020-2022)**

![Bottom 3 Institutions](https://github.com/tcareer34/Team-BAS/blob/Team_Test/Figure_3.png)



### **All Public Institutions by Graduation Rate (2020-2022)**

![Average graduation rate](https://github.com/tcareer34/Team-BAS/blob/Team_Test/Figure_4.png)




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
git clone https://github.com/tcareer34/Team-BAS.git
 Navigate to the cloned directory:

sh
cd Team-BAS
Explore the dataset and analysis in the data and files, respectively.
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


