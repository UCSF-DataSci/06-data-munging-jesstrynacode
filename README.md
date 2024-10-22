
# Data Cleaning Project: Population Dataset

## 1. Load and review dataset

### Dataset Overview
- Name of dataset: messy_population_data.csv
- Rows: 125,717
- Variables (Columns): 5

### Details on the variables in the dataset
| Column Name     | Data Type | Non-Null | Missing (%) | Mean, SD; Unique, mode *          |
|-----------------|-----------|----------|-------------|-----------------------------------|
| income_groups   | object    | 119412   | 6306 (5)    | 8, low_income                     |
| age             | float     | 119495   | 6223 (5)    | 50.0, 29.2                        |
| gender          | float     | 119811   | 5907 (5)    | 1.6, 0.6                          |
| year            | float     | 119516   | 6202 (5)    | 2025, 43.6                        |
| population      | float     | 119378   | 6340 (5)    | 111298303, 1265205486             |

 *For numeric variable, mean and standard deviation are provided. For categorical variable, number of unique value and the mode, the most frequent value, will be provided.

During the exploratory data analysis of the messy dataset, I identified that the dataset have five variables: income_groups, age, gender, year, and population with 125,717 rows but each column have several missing values. The type of data, non-null count, number and percentage of missing value, the mean and standard deviation for the numeric variable, and the number of unique values and most common value for the categorical varaibles are summarized in the table above. 

### Identified Issues
1. **Typos**
- Description: There are typos in the income_groups column where categories like low_income_typo are mistakenly counted as seprate categories from low_income. This creates redundant groups with similar names. 
- Affected Column(s): income_groups
- Example: The value count for low_income is 28433, while low_income_typo has 1505 oentries. These should likely be merged into a single group, resulting in a total of 29,938 entries for low_income.
- Potential Impact: Typos create duplicate categories (e.g., low_income and low_income_typo), which can lead to incorrect aggregations, value counts, and summary statistics. This could distort the analysis by inflating or splitting group counts unnecessarily.

2. **Incorrect data types**
- Description: The gender column is being treated as a numeric variable, but it should be categorical. It likely represents three distinct categories (1 for male, 2 for female, 3 for binary), though no data dictionary is provided to confirm this. 
- Affected Column(s): gender
- Example: The gender column contains values like 1.0, 2.0, and 3.0, which should be treated as category 'one', 'two', and 'three'. 
- Potential Impact: Treating gender as a numeric variable may lead to inappropriate calculations or summary statistics. Numeric operations may mistakenly be applied to gender. 

3. **Future dates**
- Description: There are 60,211 entries in the year column that are beyond 2024. It’s unclear whether these represent projected population data or if they are errors (such as a year shift or typo). Rather than removing these rows immediately, they will be flagged for review by the individual who provided the data.
- Affected Column(s): year
- Example: Values like 2025, 2030, and 2050 exist in the dataset, but there is insufficient context of the data to indicate if the data reflects current population such that the maximum year is 2023 or if the data also include projected years beyond 2024.
- Potential Impact: Future dates could distort time-series analyses or trend analysis if they are not meant to be in the dataset, but there is also insufficient information to know if these future dates are correct. Flagging these rows for review allows for investigation before they are permanently removed or adjusted, preserving potentially valuable information.

4. **Duplicate rows**
- Description: There are 2,950 duplicate rows in the dataset. It's unclear whether these duplicates are valid or if they represent redundant data. In reviewing the data, it seems that each row is expected to correspond to unique combinations of income_groups, age, gender, and year, suggesting that duplicates should not exist.
- Affected Column(s): income_groups, age, gender, year, population
- Example: Identical rows with the same values for income_groups, age, gender, and year are repeated multiple times (i.e., row 138, 210).
- Potential Impact: Duplicate rows can inflate counts and skew analysis, leading to incorrect results when aggregating data or performing statistical analysis. Removing duplicates will prevent biased analyses caused by duplicate data points.

5. **Outliers**
- Description: Boxplots of numeric columns (age, year, population) demonstrated that the population column contains extreme outliers. These outliers are much larger than the typical values and are likely errors or misrepresentations.
- Affected Column(s): population
- Example: Population values far exceed the typical range, with extreme values that do not align with expected distributions as demonstrated by the boxplot of population.
- Potential Impact: Outliers can distort the results of statistical analysis, leading to incorrect means, medians, and standard deviations

6. **Missing data**
- Description: Approximately 5% of the data is missing across all variables. This missing data is small enough that it should not significantly affect the overall analysis. To allow for sensitivity analysis to see if the missing data did affect overall analysis, I will create another data set in which missing values will be imputed using the median for numeric variables and the mode for categorical variables.
- Affected Column(s): income_groups, age, gender, year, population
- Example: Missing values in the age column could be replaced with the median age, while missing values in the gender column could be replaced with the most frequent gender (mode).
- Potential Impact: While 5% missing data may not significantly affect the analysis, ignoring it could reduce the dataset size and skew results. Imputation helps retain all data points while ensuring that missing values do not bias the analysis.

## Data cleaning process

### Issue 1: Typos in income_groups
- **Cleaning Method**:  Remove the _typo string from entries in the income_groups column using a custom function and apply the function to each value in the column using .apply().
- Implementation:
  ```python
  def correct_typo(value):
  if '_typo' in str(value):
      return value.replace('_typo', '')  # Remove '_typo'
  return value

  df['income_groups'] = df['income_groups'].apply(correct_typo)  # Apply the function to the 'income_groups' column
  ```
- **Justification**: Writing a custom function targeting only the specific pattern ('_typo') allowed precise correction without affecting other columns, compared to using global replacement methods (e.g., str.replace()). The .apply() functon ensures that this correction is applied consistently across all rows of the income_groups column, avoiding changes to other columns. 
- **Impact**: 
  - Rows affected: 5959
  - Data distribution change: The income_groups column now has correct groupings without duplicate categories caused by typos. Values previously spread across low_income and low_income_typo were merged into a single low_income group. Now there are 4 distint groups: low_income (29938), lower_middle_income (29840), high_income (29818), and upper_middile_income (29816). There are still 6306 missing data, which will be addressed later under issue 6

### Issue 2: Incorrect data type 
- **Cleaning Method**: Convert gender from numeric (1, 2, 3) to categorical ('one', 'two', 'three') using .map(). 
- **Implementation**:
  ```python
   # Convert gender from numeric to string using a mapping dictionary
    gender_mapping = {
    1: 'one',
    2: 'two',
    3: 'three'
    }
    df['gender'] = df['gender'].map(gender_mapping)
    df['gender'] = pd.Categorical(df['gender'], categories=['one', 'two', 'three'])
  ```
- **Justification**: Converting the gender column from numeric to categorical allows proper data analysis and prevents misleading operations (e.g., average gender values). Since gender is a categorical variable, operations designed for numeric data would be inappropriate. The .map() function simplifies the process of mapping numeric codes to categorical labels and maintains the flexibility for future label changes (i.e., clarifying with the individual who provided the data which number refers to male, female, binary). The pd.Categorical() ensures that the gender data is interpreted as a categorical type in pandas.
- **Impact**: 
- Rows affected: 119811
- Data distribution change: The gender column is now a categorical variable, improving accuracy of data analysis and interpretability. 

### Issue 3: Flagging Future Dates
- **Cleaning Method**: Create a year_flag column to flag rows where the year column contains values beyond 2024 ('future_year'), valid years ('valid_year'), or missing (NaN).
- **Implementation**:
  ```python
  max_valid_year = 2024
  def flag_year(row):
    if pd.isna(row):  # Check for missing values
        return np.nan
    elif row > max_valid_year:
        return 'future_year'
    else:
        return 'valid_year'

  df['year_flag'] = df['year'].apply(flag_year)
  ```
- **Justification**: I initially used np.where() but this function failed to handle NaN values appropriately and as mentioned above, I did not want to remove the missing values. By switching to .apply() and a custom function, it became possible to assign NaN to missing years and distinguish between valid and future years. This flagging is useful for isolating and reviewing the future years with the individual who provided the data to make sure the years are correct.
- **Impact**: 
  - Rows affected: [60211]
  - Data distribution change: The new dataset now contains 6 columns (previously 5) after adding this new is_future_year variable. The overall number of rows did not change.

### Issue 4: Duplicate Rows
- **Cleaning Method**: Remove duplicate rows using drop_duplicates().
- **Implementation**:
  ```python
    duplicate_rows = df[df.duplicated()].index
    df = df.drop_duplicates()
  ```
- **Justification**: Pandas' drop_duplicates() method is specifically designed to efficiently remove duplicate rows based on all columns. It ensures that only the first occurrence of each row is retained, preventing double-counting and skewed or inflated results during data analysis.
- **Impact**: 
  - Rows affected: [3219]
  - Data distribution change: Duplicates were removed and now the new dataset contains 122,499 rows from the original 125,718.

### Issue 5: Outliers in population
- **Cleaning Method**: Identify and remove outliers in the population column using the Interquartile Range (IQR) method.
- **Implementation**:
  ```python
    Q1 = df['population'].quantile(0.25)
    Q3 = df['population'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df = df[(df['population'] >= lower_bound) & (df['population'] <= upper_bound)]
  ```
- **Justification**: The Interquartile Range (IQR) method was selected because it effectively removes outliers in skewed distributions, focusing on the middle 50% of the data. This ensures that extreme population values (which might distort statistics) are excluded while preserving the majority of the data for accurate analysis.
- **Impact**: 
  - Rows affected: 2242
  - Data distribution change: Extreme outliers in the population column were removed resulting in a dataset with 114,131 rows.

### Issue 6: Missing Data
- **Cleaning Method**: Impute missing values using the median for numeric columns and the mode for categorical columns.
- **Implementation**:
  ```python
    # Fill missing values in numeric columns with the median
    df[numeric_columns] = df[numeric_columns].apply(lambda col: col.fillna(col.median()))

    # Fill missing values in categorical columns with the mode
    df[categorical_columns] = df[categorical_columns].apply(lambda col: col.fillna(col.mode()[0]))
    
  ```
- **Justification**: During my data exploratory analysis, the population variable did not appear normally distributed so I choose to use median for the numeric variables becuase it is a better choice for skewed data. While age and year did appear to have normal distribution, using median for both of them would still be appropriate. For categorical variables, I choose to use the most frequent value as a way to preserve the original distribution of the data. I mentioned earlier that I didn't think 5% missing data would affect the data analysis significantly so these imputed values were saved as a different dataset to allow for sensitivity analysis.
- **Impact**: 
  - Rows affected: 10988 for numeric variable, 11069 for categorical variable
  - Data distribution change: Missing values were filled, ensuring that no gaps remain in the dataset, while maintaining the integrity of the distribution for both numeric and categorical data.


## 3. Final State Analysis

### Overview of cleaned_data.csv
- Rows: 114,131
- Variables (Columns): 6

### Details on the variables in the clean dataset
| Column Name     | Data Type | Non-Null | Missing (%) | Mean, SD; Unique, mode *          |
|-----------------|-----------|----------|-------------|-----------------------------------|
| income_groups   | object    | 108414   | 5715 (5)    | 4, low_income                     |
| age             | float     | 108475   | 5656 (5)    | 50.0, 29.2                        |
| gender          | float     | 108777   | 5354 (5)    | 3, two                            |
| year            | float     | 108509   | 5622 (5)    | 2025, 43.6                        |
| population      | float     | 114131   | 0 (0)       | 9228925, 8489086                  |
| year_flag       | float     | 108509   | 5622 (5)    | 3, future_year                    |

### Overview of clean_imputed_data.csv
- Rows: 114,131
- Variables (Columns): 6

### Details on the variables in the clean dataset with imputed data
| Column Name     | Data Type | Non-Null | Missing (%) | Mean, SD; Unique, mode *          |
|-----------------|-----------|----------|-------------|-----------------------------------|
| income_groups   | object    | 114131   | 0 (0)       | 4, low_income                     |
| age             | float     | 114131   | 0 (0)       | 50.1, 28.4                        |
| gender          | object    | 114131   | 0 (0)       | 3, two                            |
| year            | float     | 114131   | 0 (0)       | 2025, 42.5                        |
| population      | float     | 114131   | 0 (0)       | 9228925, 8489086                  |
| year_flag       | object    | 114131   | 0 (0)       | 3, future_year                    |
 
 *For numeric variable, mean and standard deviation are provided. For categorical variable, number of unique value and the mode, the most frequent value, will be provided.

### Summary of Changes
- Major changes to the Dataset:
1. Typos Removed: Merged entries like low_income_typo into low_income, reducing redundancy in the income_groups column and ensuring cleaner categories.
2. Duplicate Rows Removed: 2,950 duplicate rows were dropped, reducing the dataset size and improving accuracy by preventing double-counting.
3. Outliers in Population Removed: Extreme outliers in the population column were identified and removed using the IQR method. This step reduced the skewness in population distribution and resulted in a smaller, more representative dataset.
4. Gender Converted to Categorical: The gender column was converted from numeric to categorical (one, two, three), ensuring that it is handled appropriately during analysis and imputation.
5. Future Dates Flagged: Entries in the year column with values beyond 2024 were flagged for review using a new year_flag column (valid_year, future_year, NaN).
6. Missing Data Imputed: Missing values were imputed using the median for numeric columns and the mode for categorical columns, allowing for sensitivity analysis without affecting data distribution significantly.

- Boxplot Analysis:
    - Before Cleaning (Messy Data): The boxplot of population showed significant skewness due to the presence of outliers, while age and year distributions appeared relatively normal.
    - After Cleaning (Cleaned Data): After outlier removal, the population distribution became less skewed, while the distributions for age and year remained unchanged.
    - Sensitivity Analysis (Cleaned Imputed Data): There were no significant changes in the data distribution after imputing missing values, confirming that the imputation method (median and mode) preserved the overall data characteristics.

- Notable Changes in Data Distribution:
    - Population: The removal of outliers significantly reduced the skewness in the population column. This is reflected in the comparison of boxplots before and after cleaning. However, the imputation of missing population values did not further change the distribution.
    - Age and Year: The distributions of age and year remained unchanged across the three stages (messy, cleaned, and imputed data), suggesting that these columns were not significantly impacted by outlier removal or imputation.
    - Comparison of Descriptive Statistics and Boxplots: The comparison between the descriptive statistics and boxplots for the cleaned data (without imputed values) and the imputed data showed minimal differences. This suggests that the 5% of missing data did not significantly impact the overall data analysis. However, it’s important to note that we made the assumption that the missing data reflects the overall data distribution. It is possible that the missing data might disproportionately represent certain groups, such as the high_income category or gender group 3 (binary). Therefore, it may be worth conducting further sensitivity analyses using different imputation strategies (e.g., group-based imputation) to explore how different imputation methods could influence the results.

