# Team BAS
# CNE 340 Final Project
# 4-Year Graduation Rates at Texas Public Universities between 2020-2022


# Import required libraries
import pandas as pd # For handling datasets
import numpy as np  # For numerical operations
from matplotlib import pyplot as plt  # For data visualization
from sqlalchemy import create_engine  # For database connection
import matplotlib.cm as cm  # For colormap in visualization

# Install cryptography
# SQL connection and Database
# Database credentials and connection details
hostname = 'localhost'  # Database host
username = 'root'  # Database username
password = ''  # Database password (empty in this case)
dbname = ('bas final')  # Database name

# Connect to MySQL on W/LAMP Server
try:
    connection_string = f"mysql+pymysql://{username}:{password}@{hostname}/{dbname}"
    engine = create_engine(connection_string)  # Create database engine
    print("Database connection successful")
except Exception as e:
    print(f"Error connecting to database: {e}")   # Print error if connection fails
    exit()

# Open CSV file from the project folder (use your actual file path) with error handling
# Read CSV file into a DataFrame
try:
    df = pd.read_csv('graduation_rates_at_public_universities_2020-2022.csv')  # Load dataset
    print("CSV read successful")
except FileNotFoundError:
    print("Error: CSV file not found.")  # Handle file not found error
    exit()
except Exception as e:
    print(f"Error reading CSV file: {e}")  # Handle other CSV errors
    exit()

# Load data into SQL database table
table_name = 'public_institutions_graduation_rate'
df.to_sql(table_name, engine, if_exists='replace', index=False)  # Store DataFrame into SQL table


# Query data sorted by highest 4-year graduation rate
query = f"SELECT * FROM {table_name} ORDER BY GradRate4yr DESC"  # Pulling data from the table
db_sorted = pd.read_sql(query, engine)

# Calculate average graduation rate
avg_grad_rate = db_sorted['GradRate4yr'].mean()


# Function to sort out the 3 institutions with the highest graduation rates
#def top_three_public_institutions(table, engine):
#    df = pd.read_sql_table(table, con=engine)
#    highest_grad_rate_data = df.sort_values(by='GradRate4yr', ascending=False).head(3)[['Institution', 'GradRate4yr']]
#    institutions = highest_grad_rate_data['Institution'].tolist()
#    grad_rates = highest_grad_rate_data['GradRate4yr'].tolist()
#    return institutions, grad_rates

# Function to sort out the 3 institutions with the highest graduation rates
def top_three_public_institutions(table, engine):
    df = pd.read_sql_table(table, con=engine) # Read table into DataFrame

    # Handle missing values, convert types, and remove duplicates
    df = df.dropna(subset=['GradRate4yr'])  # Remove rows where GradRate4yr is NaN
    df['GradRate4yr'] = pd.to_numeric(df['GradRate4yr'], errors='coerce')  # Ensure numeric sorting
    df = df.drop_duplicates(subset=['Institution'])  # Ensure unique institutions

    # Sort and select top 3 institutions
    highest_grad_rate_data = df.sort_values(by='GradRate4yr', ascending=False).head(3)[['Institution', 'GradRate4yr']]
    institutions = highest_grad_rate_data['Institution'].tolist()
    grad_rates = highest_grad_rate_data['GradRate4yr'].tolist()

    return institutions, grad_rates

# Function to sort out the institution with the highest 4-year graduation rate
def top_institution(table, engine):
    df = pd.read_sql_table(table, con=engine)
    top_inst_data = df.sort_values(by='GradRate4yr', ascending=False).head(1)[['Institution', 'GradRate4yr']]
    institution = top_inst_data['Institution'].values[0]
    grad_rate = top_inst_data['GradRate4yr'].values[0]
    return institution, grad_rate

# Function to sort out the 3 institutions with the lowest graduation rates
def three_lowest_institutions(table, engine):
    df = pd.read_sql_table(table, con=engine)
    lowest_grad_rate_data = df.sort_values(by='GradRate4yr').head(3)[['Institution', 'GradRate4yr']]
    institutions = lowest_grad_rate_data['Institution'].tolist()
    grad_rates = lowest_grad_rate_data['GradRate4yr'].tolist()
    return institutions, grad_rates

# Function to sort all institutions
def sort_all_institutions(table, engine):
    df = pd.read_sql_table(table, con=engine)
    all_institutions = df.sort_values(by='Institution')
    all_institutions_institution = all_institutions['Institution'].tolist()
    grad_rate = all_institutions['GradRate4yr'].tolist()
    return all_institutions_institution, grad_rate

# Call the functions to get the top institution, top 3 and lowest 3 public institutions
# Retrieve required data
top_inst, top_inst_grad_rate = top_institution(table_name, engine)
high_3_institutions, high_3_grad_rates = top_three_public_institutions(table_name, engine)
low_3_institutions, low_3_grad_rates = three_lowest_institutions(table_name, engine)
all_institution, all_institution_grad_rate = sort_all_institutions(table_name, engine)

# Plotting

# Plot highest graduation rate institution
plt.figure(figsize=(10, 7))
plt.bar(top_inst, top_inst_grad_rate, width=0.35, color='blue', edgecolor='black')
plt.text(top_inst, top_inst_grad_rate, f'{top_inst_grad_rate:.2f}', ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.title('Institution with the Highest 4-Year Graduation Rate (2020-2022)', fontsize=16, fontweight='bold')
plt.xlabel('Public Institution in Texas', fontsize=14, fontweight='bold')
plt.ylabel('4 Year Graduation Rate (%)', fontsize=14, fontweight='bold')
plt.xticks(rotation=0, fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()

# Plot top 3 institutions
plt.figure(figsize=(10, 7))
bar_colors = ['red', 'purple', 'green']
bar_width = 0.35

# Plot each bar separately to ensure distinct colors
for i, (institution, grad_rate) in enumerate(zip(high_3_institutions, high_3_grad_rates)):
    plt.bar(institution, grad_rate, width=bar_width, color=bar_colors[i], edgecolor='black')
    plt.text(institution, grad_rate, f'{grad_rate:.2f}', ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.title('Top 3 Public Institutions by Graduation Rates (2020-2022)', fontsize=16, fontweight='bold')
plt.xlabel('Public Institutions in Texas', fontsize=14, fontweight='bold')
plt.ylabel('4 Year Graduation Rate (%)', fontsize=14, fontweight='bold')
plt.xticks(rotation=0, fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()

# Plot bottom 3 institutions
plt.figure(figsize=(10, 7))
bar_colors = ['cyan', 'magenta', 'yellow']
bar_width = 0.35

plt.bar(low_3_institutions, low_3_grad_rates, width=bar_width, color=bar_colors, edgecolor='black')

for i in range(len(low_3_institutions)):
    plt.text(low_3_institutions[i], low_3_grad_rates[i], str(low_3_grad_rates[i]), ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.title('Bottom 3 Public Institutions by Graduation Rate (2020-2022)', fontsize=16, fontweight='bold')
plt.xlabel('Public Institutions in Texas', fontsize=14, fontweight='bold')
plt.ylabel('4 Year Graduation Rate (%)', fontsize=14, fontweight='bold')
plt.xticks(rotation=0, fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()

# Plot all institutions and average graduation rate
plt.figure(figsize=(14, 8))
cmap = plt.get_cmap('viridis')
colors = cmap(np.linspace(0, 1, len(all_institution)))
plt.bar(all_institution, all_institution_grad_rate, color=colors, edgecolor='black')
plt.axhline(avg_grad_rate, color='blue', linestyle='--', linewidth=2)
plt.text(39, avg_grad_rate, f'Average Rate: {avg_grad_rate:.2f}', color='blue', fontsize=12, fontweight='bold')

#plt.title('Graduation Rates of All Public Institutions (2020-2022)', fontsize=12, fontweight='bold')
#plt.xlabel('All Public Institutions in Texas', fontsize=12, fontweight='bold')
#plt.ylabel('Graduation Rate (%)', fontsize=12, fontweight='bold')

# Adding title and label
plt.title('Graduation Rates of All Public Institutions (2020-2022)', fontsize=14, fontweight='bold')
plt.xlabel('All Public Institutions in Texas', fontsize=16, fontweight='bold')
plt.ylabel('4 Year Graduation Rate (%)', fontsize=14, fontweight='bold')
plt.xticks(rotation=90)
plt.tight_layout()


# Show all plots at the same time
plt.show()

# Close database connection made by engine
engine.dispose()
print("Database connection closed.")
