# Team BAS
# CNE 340 Final Project
# 4-Year Graduation Rates at Texas Public Universities 2020-2022


# Import section
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sqlalchemy import create_engine
import matplotlib.cm as cm

# Install cryptography
# SQL connection and Database
hostname = 'localhost'
uname = 'root'
pwd = ''
dbname = ('bas final')

# Connect to MySQL on W/LAMP Server
connection_string = f"mysql+pymysql://{uname}:{pwd}@{hostname}/{dbname}"
engine = create_engine(connection_string)

# Open CSV file from the project folder (use your actual file path)
df = pd.read_csv('graduation_rates_at_public_universities_2020-2022.csv')

# Table name
table_name = 'public_institutions_graduation_rate'
df.to_sql(table_name, engine, if_exists='replace', index=False)

# Query from the table in the database
query = f"SELECT * FROM {table_name} ORDER BY GradRate4yr DESC"  # Pulling data from the table
db_sorted = pd.read_sql(query, engine)

# Sort out top institution with the highest graduation rates
top_institutions = db_sorted.nlargest(3, 'GradRate4yr')  #  Highest institution by row GradRate4r from the database
num_institutions = len(top_institutions)
colors = cm.rainbow(np.linspace(0, 3, num_institutions))  # Color mapping

# Plotting figure and adding a counter i and using zip for the two-column tuple
plt.figure(figsize=(7, 7))

# Plot the bar chart
bar_colors = ['red','purple','green']
bar_width = 0.25
for i, (institution, grad_rate) in enumerate(zip(top_institutions['Institution'], top_institutions['GradRate4yr'])):
    plt.bar(institution, grad_rate, color=bar_colors[i], edgecolor='black', width=bar_width)

plt.text(institution, grad_rate, str(round(grad_rate, 2)), ha='center', va='bottom', fontweight='bold')  # Add text to the top of the bar

plt.title('Institution with the Highest 4-Year Graduation Rate (2020-2022)', fontweight='bold')
plt.xlabel('Public Institution In Texas', fontweight='bold')
plt.ylabel('Graduation Rate (%)', fontweight='bold')

# Function to sort out the 3 institutions with the highest graduation rates
def top_three_public_institutions(table, engine):
    df = pd.read_sql_table(table, con=engine)

    # Handle missing values, convert types, and remove duplicates
    df = df.dropna(subset=['GradRate4yr'])  # Remove rows where GradRate4yr is NaN
    df['GradRate4yr'] = pd.to_numeric(df['GradRate4yr'], errors='coerce')  # Ensure numeric sorting
    df = df.drop_duplicates(subset=['Institution'])  # Ensure unique institutions

    # Sort and select top 3 institutions
    highest_grad_rate_data = df.sort_values(by='GradRate4yr', ascending=False).head(3)[['Institution', 'GradRate4yr']]
    institutions = highest_grad_rate_data['Institution'].tolist()
    grad_rates = highest_grad_rate_data['GradRate4yr'].tolist()

    return institutions, grad_rates

high_3_institutions, high_3_grad_rates = top_three_public_institutions(table_name, engine)

# Plot the bar chart for top 3 institutions with the highest graduation rates
plt.figure(figsize=(10, 7))
bar_colors = ['red', 'purple', 'green']
bar_width = 0.35

# Calculate average graduation rate
avg_grad_rate = db_sorted['GradRate4yr'].mean()

# Function to sort all institutions
def sort_all_institutions(table, engine):
    df = pd.read_sql_table(table, con=engine)
    all_institutions = df.sort_values(by='Institution')  # Ensure the column name matches exactly
    all_institutions_institution = all_institutions['Institution'].tolist()  # Match column names
    grad_rate = all_institutions['GradRate4yr'].tolist()
    return all_institutions_institution, grad_rate

# Function to sort out the 3 institutions with the lowest graduation rates
def three_lowest_institutions(table, engine):
    df = pd.read_sql_table(table, con=engine)
    lowest_grad_rate_data = df.sort_values(by='GradRate4yr').head(3)[['Institution', 'GradRate4yr']]  # Ensure the column name matches exactly
    institutions = lowest_grad_rate_data['Institution'].tolist()  # Match column names
    grad_rates = lowest_grad_rate_data['GradRate4yr'].tolist()
    return institutions, grad_rates


# Graph 2 - lowest 3 institutions with the lowest graduation rates
low_3_institutions, low_3_grad_rate = three_lowest_institutions(table_name, engine)

# Define figure size
plt.figure(figsize=(7, 7))

# Plot the bar chart
bar_colors = ['red', 'purple', 'green']
bar_width = 0.25
plt.bar(low_3_institutions, low_3_grad_rate, width=bar_width, color=bar_colors, edgecolor='black')

# Add values on top of each bar
for i in range(len(low_3_institutions)):
    plt.text(low_3_institutions[i], low_3_grad_rate[i], str(low_3_grad_rate[i]), ha='center', va='bottom', fontweight='bold')

# Chart title, X and Y labels:
plt.title('Bottom 3 Public Institutions by Graduation Rate (2020-2022)', fontweight='bold')
plt.xlabel('Public Institutions in Texas', fontweight='bold')
plt.ylabel('Graduation Rate (%)', fontweight='bold')
plt.tight_layout()


# Plot chart including all institutions' rates and the average rate
all_institution, all_institution_grad_rate = sort_all_institutions(table_name, engine)

plt.figure(figsize=(12, 6))
cmap = plt.get_cmap('viridis')
colors = cmap(np.linspace(0, 1, len(all_institution)))
plt.bar(all_institution, all_institution_grad_rate, color=colors, edgecolor='black')
plt.axhline(avg_grad_rate, color='blue', linestyle='--', linewidth=2)
plt.text(40, avg_grad_rate, f'Average Rate: {avg_grad_rate:.2f}', color='blue', fontsize=10, fontweight='bold')

# Adding title and label
plt.title('Graduation Rates of All Public Institutions (2020-2022)', fontweight='bold')
plt.xlabel('All Public Institutions in Texas', fontweight='bold')
plt.ylabel('Graduation Rate (%)', fontweight='bold')
plt.xticks(rotation=90)
plt.tight_layout()

# Plot only once at the end to show all plots
plt.show()

# Close connection made by engine
engine.dispose()
