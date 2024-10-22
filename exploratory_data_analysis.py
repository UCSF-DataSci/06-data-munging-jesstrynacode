import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

JUPYTER = False

# Load the dataset
df = pd.read_csv('cleaned_data.csv')

# Step 1: Basic Information
rows, columns = df.shape
print(f"Initial dataset contains {rows} rows and {columns} columns")
df.info()

# Step 2: Explore Each Variable
for col in df.columns:
    print(f"\nExploring variable: {col}")
    
    # If the column is numeric, get summary statistics
    if pd.api.types.is_numeric_dtype(df[col]):
        print("Numeric variable:")
        print(df[col].describe())  # Summary statistics (count, mean, std, min, max, etc.)
    
    # If the column is categorical, get the count of unique values and mode
    else:
        print("Categorical variable:")
        unique_values = df[col].nunique()
        print(f"Unique values in '{col}': {unique_values}")
        
        mode_value = df[col].mode()[0] if not df[col].mode().empty else "No mode"
        print(f"Most common value (mode) in '{col}': {mode_value}")
        print(f"\nValue counts for '{col}' column:")
        print(df[col].value_counts(dropna=False))  # Show counts for each unique value including NaN

# Step 3: Check for Duplicates
duplicate_count = df.duplicated().sum()
print(f"\nNumber of duplicate rows: {duplicate_count}")

# Step 3.1: Show duplicate rows if any exist
if duplicate_count > 0:
    print("\nDuplicate rows:")
    print(df[df.duplicated(keep=False)])  # Display all rows that have duplicates, keep=False shows all instances

# Step 4: Check for Missing Values and Percentage of Missing
print("\nMissing values and percentage of missing values in each column:")

# Calculate missing values and percentage
missing_values = df.isnull().sum()
missing_percentage = (missing_values / len(df)) * 100

# Combine into a DataFrame for cleaner output
missing_df = pd.DataFrame({
    'Missing Values': missing_values,
    'Percentage of Missing (%)': missing_percentage
})

# Print the missing values and percentage for each column
print(missing_df)

# Step 5: Compute Mean and Standard Deviation for Numeric Columns
print("\nMean and standard deviation for numeric columns:")
for col in df.select_dtypes(include=['float64', 'int64']).columns:
    mean_value = df[col].mean()
    std_value = df[col].std()
    print(f"{col} - Mean: {mean_value}, Standard Deviation: {std_value}")

# check for negative value# Filter the DataFrame for negative values in any numeric column
negative_values_df = df[(df.select_dtypes(include=['float', 'int']) < 0).any(axis=1)]

# Display rows with negative values in any numeric column
print("Rows with negative values in any numeric column:")
print(negative_values_df)

# Check for unique values in categorical variables
unique_values = df['income_groups'].unique()
print("Unique values in 'income_groups':")
print(unique_values)

# Count how many years beyond 2024
df['year'] = pd.to_numeric(df['year'], errors='coerce')

# Filter rows where the 'year' is greater than 2024
years_beyond_2024 = df[df['year'] > 2024]

# Count the number of rows with 'year' > 2024
count_years_beyond_2024 = len(years_beyond_2024)

# Output the result
print(f"Number of entries where 'year' is beyond 2024: {count_years_beyond_2024}")


# Step 6: Check for outliers
JUPYTER = False  # or True depending on the environment

def plot_boxplot(df, column, filename=None):
    """Plot and save a boxplot for the specified column."""
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=df[column])
    plt.title(f'Boxplot of {column}')  # Use the `column` variable for the title
    if JUPYTER:
        plt.show()  # Show the plot in Jupyter notebook
    else:
        if filename:
            plt.savefig(filename)  # Save the plot to a file if not in Jupyter
        plt.close()  # Close the plot to avoid displaying it in non-Jupyter environments

# Define the columns to create boxplots for
columns_to_plot = ['population', 'age', 'year']

# Loop through the columns and generate boxplots for each
for column in columns_to_plot:
    if JUPYTER:
        plot_boxplot(df, column)
    else:
        plot_boxplot(df, column, f'{column}_boxplot_after.png')  # Save each plot with a distinct filename

    