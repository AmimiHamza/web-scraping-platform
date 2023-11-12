import pandas as pd

def generate_delta_file():
    # Read the two Excel files
    cryptos_df = pd.read_excel("crypto/cryptos.xlsx")
    cryptosn_df = pd.read_excel("crypto/cryptosn.xlsx")

    # Merge the two DataFrames based on the 4th column
    merged_df = cryptosn_df.merge(cryptos_df, on=cryptosn_df.columns[3], how='left', indicator=True)

    # Filter out the rows that are only in CRYPTOSN
    delta_df = merged_df[merged_df['_merge'] == 'left_only'].drop('_merge', axis=1)

    # Delete the last 10 rows from the DataFrame
    delta_df = delta_df.iloc[:11]

    # Write the result to a new Excel file called delta.xlsx
    delta_df.to_excel("crypto/delta.xlsx", index=False)
    

    
    # cols_to_compare = ['1h', '24h']  # Replace with the actual column names you want to compare
    # filtered_rows = cryptosn_df[~cryptosn_df[cols_to_compare].isin(cryptos_df[cols_to_compare].values).all(axis=1)]

    # # Write the result to a new Excel file called delta.xlsx
    # filtered_rows.to_excel("crypto/delta.xlsx", index=False)
