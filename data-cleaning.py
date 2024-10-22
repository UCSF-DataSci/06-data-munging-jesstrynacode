import pandas as pd
import numpy as np
import logging

# Set up logging configuration
logging.basicConfig(
    filename='data_cleaning.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load data
try:
    df = pd.read_csv('messy_population_data.csv')
    logging.info('Successfully loaded messy_population_data.csv')
except FileNotFoundError:
    logging.error("File 'messy_population_data.csv' not found.")
    raise
except Exception as e:
    logging.error(f"Error loading data: {e}")
    raise

# Create a copy of the original dataset to compare changes
df_original = df.copy()

# --- Issue 1: Fixing Typos ---
def correct_typo(value):
    if '_typo' in str(value):
        return value.replace('_typo', '')  # Remove '_typo'
    return value

# Apply the function to the 'income_groups' column
try:
    affected_rows_typos = df[df['income_groups'].str.contains('_typo', na=False)].index
    df['income_groups'] = df['income_groups'].apply(correct_typo)
    logging.info(f"Corrected typos in income_groups column. Rows affected: {len(affected_rows_typos)}")
except KeyError:
    logging.error("Column 'income_groups' not found.")
    raise
except Exception as e:
    logging.error(f"Error correcting typos: {e}")
    raise

# --- Issue 2: Incorrect Data Types ---
# Convert gender from numeric to string variable using a mapping dictionary
gender_mapping = {
    1: 'one',
    2: 'two',
    3: 'three'
}

# Map the values to categories and track affected rows
try:
    affected_rows_gender = df[df['gender'].isin([1, 2, 3])].index
    df['gender'] = df['gender'].map(gender_mapping)
    df['gender'] = pd.Categorical(df['gender'], categories=['one', 'two', 'three'])
    logging.info(f"Converted 'gender' column to categorical type. Rows affected: {len(affected_rows_gender)}")
except KeyError:
    logging.error("Column 'gender' not found.")
    raise
except Exception as e:
    logging.error(f"Error converting 'gender' column: {e}")
    raise

# --- Issue 3: Flagging Future Dates ---
try:
    max_valid_year = 2024

    # Use Pandas apply to create a flag for future years, valid years, and missing values
    def flag_year(row):
        if pd.isna(row):  # Check for missing values
            return 'missing'
        elif row > max_valid_year:
            return 'future_year'
        else:
            return 'valid_year'

    # Apply the flag_year function to the 'year' column
    df['year_flag'] = df['year'].apply(flag_year)

    affected_rows_future_dates = df[df['year_flag'] == 'future_year'].index
    future_rows_count = len(affected_rows_future_dates)

    logging.info(f"Flagged {future_rows_count} rows with future dates.")
except KeyError:
    logging.error("Column 'year' not found.")
    raise
except Exception as e:
    logging.error(f"Error flagging future dates: {e}")
    raise

# --- Issue 4: Remove Duplicate Rows ---
try:
    duplicate_rows = df[df.duplicated()].index
    df = df.drop_duplicates()
    logging.info(f"Removed {len(duplicate_rows)} duplicate rows. New shape: {df.shape}")
except Exception as e:
    logging.error(f"Error removing duplicates: {e}")
    raise

# --- Issue 5: Remove Outliers ---
try:
    Q1 = df['population'].quantile(0.25)
    Q3 = df['population'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    affected_rows_outliers = df[(df['population'] < lower_bound) | (df['population'] > upper_bound)].index
    df = df[(df['population'] >= lower_bound) & (df['population'] <= upper_bound)]
    logging.info(f"Removed outliers in 'population'. Rows affected: {len(affected_rows_outliers)}. New shape: {df.shape}")
except KeyError:
    logging.error("Column 'population' not found.")
    raise
except Exception as e:
    logging.error(f"Error removing outliers: {e}")
    raise

# --- Save Cleaned Data Before Imputation ---
try:
    df.to_csv('cleaned_data.csv', index=False)
    logging.info("Cleaned data saved to 'cleaned_data.csv' before imputing missing data")
except Exception as e:
    logging.error(f"Error saving cleaned data: {e}")
    raise

# --- Issue 6: Impute Missing Data ---
try:
    # Ensure gender is treated as an object (categorical) column
    df['gender'] = df['gender'].astype('object')

    # Separate numeric and categorical columns
    numeric_columns = df.select_dtypes(include=['float', 'int']).columns
    categorical_columns = df.select_dtypes(include=['object']).columns

    affected_rows_missing_numeric = df[df[numeric_columns].isnull().any(axis=1)].index
    affected_rows_missing_categorical = df[df[categorical_columns].isnull().any(axis=1)].index

    # Fill missing values in numeric columns with the median
    df[numeric_columns] = df[numeric_columns].apply(lambda col: col.fillna(col.median()))
    logging.info(f"Filled missing numeric values with median. Rows affected: {len(affected_rows_missing_numeric)}")

    # Fill missing values in categorical columns with the mode
    df[categorical_columns] = df[categorical_columns].apply(lambda col: col.fillna(col.mode()[0]))
    logging.info(f"Filled missing categorical values with mode. Rows affected: {len(affected_rows_missing_categorical)}")
except Exception as e:
    logging.error(f"Error imputing missing data: {e}")
    raise

# --- Save Cleaned Data After Imputation ---
try:
    df.to_csv('clean_imputed_data.csv', index=False)
    logging.info("Cleaned and imputed data saved to 'clean_imputed_data.csv'")
except Exception as e:
    logging.error(f"Error saving cleaned and imputed data: {e}")
    raise
