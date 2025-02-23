import pandas as pd
import re

# Load the transaction data from the file
file_path = 'csv/CARDNAME.csv'


data = pd.read_csv(file_path)

df = pd.DataFrame(data)

# Filter relevant columns
df_filtered = df[['Description', 'Amount', 'Type']]

# Define a function to clean and normalize descriptions
def clean_and_normalize(description):
    # Convert to lowercase for consistency
    description = description.lower()

    # Group specific patterns
    if "facebk" in description:
        return "facebook transaction"
    if "amazon" in description or "amzn" in description:
        return "amazon purchase"
    if "uber" in description:
        return "uber trip"
    if "walmart" in description:
        return "walmart purchase"
    if "autozone" in description:
        return "autozone store"
    if "panera bread" in description:
        return "panera bread"
    if "delta gas" in description:
        return "delta gas station"
    if "dollar tree" in description:
        return "dollar tree"
    if "shoprite" in description:
        return "shoprite store"
    if "sunoco" in description:
        return "sunoco gas station"
    if "starbucks" in description:
        return "starbucks"
    if "dbbkrg" in description:
        return "brokerage debit"


    # Remove unnecessary details like dates, web IDs, and phone numbers
    description = re.sub(r'\b\d{2}/\d{2}\b', '', description)  # Remove dates
    description = re.sub(r'\b\d{3}-\d{3}-\d{4}\b', '', description)  # Remove phone numbers
    description = re.sub(r'\bweb id: \d+\b', '', description, flags=re.IGNORECASE)  # Remove web IDs
    
    # Remove special characters and standalone numbers
    description = re.sub(r'[^a-z\s]', '', description)

    # Keep the first 3 meaningful words to retain context
    words = description.strip().split()
    if len(words) > 3:
        return ' '.join(words[:3])  # Keep first three words
    elif len(words) > 0:
        return ' '.join(words)  # Keep whatever words remain
    else:
        return "miscellaneous"
# Apply the cleaning function to the 'Description' column
df_filtered['Normalized'] = df_filtered['Description'].apply(clean_and_normalize)

# Save the intermediate data for debugging (optional)
# df_filtered.to_csv('Started/UnitedExplorer_Intermediate.csv', index=False)

# Group by the normalized description, sum the 'Amount', and round to 2 decimal places
grouped_df = (
    df_filtered.groupby('Normalized', as_index=False)
    .agg({'Amount': 'sum'})
    .round(2)
)

# Sort by 'Amount' in ascending order to show negative values first
grouped_df = grouped_df.sort_values(by='Amount', ascending=True)


# Save the grouped transactions to a new CSV file
grouped_df.to_csv('Started/CARDNAME.csv', index=False)

# Display unique normalized values and grouped transactions
print("Unique Normalized Values:")
print(df_filtered['Normalized'].unique())
print("\nGrouped Transactions (Negative Values First):")
print(grouped_df.head())
