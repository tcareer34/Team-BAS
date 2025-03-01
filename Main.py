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
table_name = 'public_institutions_graduation_rate'  # Replace with your actual table name
df.to_sql(table_name, engine, if_exists='replace', index=False)

# Query from the table in the database
query = f"SELECT * FROM {table_name} ORDER BY GradRate4yr DESC"  # Pulling data from the table
db_sorted = pd.read_sql(query, engine)

# Sort out top institutions with the highest graduation rates
top_institutions = db_sorted.nlargest(3, 'GradRate4yr')  #  highest institutions by row from the db
num_institutions = len(top_institutions)
colors = cm.rainbow(np.linspace(0, 1, num_institutions))  # Color mapping

# Plotting figure and adding a counter i and using zip for the two-column tuple
plt.figure(figsize=(7, 7))
bar_width = 0.25
for i, (institution, grad_rate) in enumerate(zip(top_institutions['Institution'], top_institutions['GradRate4yr'])):
    plt.bar(institution, grad_rate, color=colors[i], edgecolor='black', width=bar_width)
    plt.text(institution, grad_rate, str(round(grad_rate, 2)), ha='center', va='bottom', fontweight='bold')  # Add text to the top of the bar

plt.title('Institution with 4 Years Highest Graduation Rates (2020-2022)', fontweight='bold')
plt.xlabel('Public Institution In Texas', fontweight='bold')
plt.ylabel('Graduation Rate (%)', fontweight='bold')


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
plt.title('3 Public Institutions with Lowest Graduation Rates (2020-2022)', fontweight='bold')
plt.xlabel('Public Institutions in Texas', fontweight='bold')
plt.ylabel('Graduation Rate (%)', fontweight='bold')
plt.tight_layout()


# Plot chart including all institutions' rates and the average rate
all_institution, all_institution_grad_rate = sort_all_institutions(table_name, engine)

plt.figure(figsize=(12, 6))
all_institutions_bar_colors = np.random.rand(len(all_institution), 3)
plt.bar(all_institution, all_institution_grad_rate, color=all_institutions_bar_colors, edgecolor='black')
plt.axhline(avg_grad_rate, color='blue', linestyle='--', linewidth=2)
plt.text(44, avg_grad_rate, f'Average Rate: {avg_grad_rate:.2f}', color='blue', fontsize=10, fontweight='bold')

# Adding title and label
plt.title('All Public Institutions Graduation Rate (2020-2022)', fontweight='bold')
plt.xlabel('All Public Institutions in Texas', fontweight='bold')
plt.ylabel('Graduation Rate (%)', fontweight='bold')
plt.xticks(rotation=90)
plt.tight_layout()

# Plot only once at the end to show all plots
plt.show()

# Close connection made by engine
engine.dispose()
