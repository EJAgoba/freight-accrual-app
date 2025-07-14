import pandas as pd

# Load Excel files
accrual_updated = pd.read_excel(r"C:\Users\c1354623\OneDrive - Cintas Corporation\Documents\Miscellaneous_Excel_Analysis\Done\New Accrual Logic II\June Accrual Updated2.xlsx")
location_table = pd.read_excel(r"C:\Users\c1354623\OneDrive - Cintas Corporation\Documents\Miscellaneous_Excel_Analysis\Done\New Accrual Logic II\Coding_Cintaslocation 02.06.25.xlsx")

# Strip column names
accrual_updated.columns = accrual_updated.columns.str.strip()
location_table.columns = location_table.columns.str.strip()

# Standardize 'Profit Center' format across both
accrual_updated['Profit Center'] = accrual_updated['Profit Center'].apply(str).str.strip().str.replace('.0', '', regex=False)
location_table['Prof_Cntr'] = location_table['Prof_Cntr'].apply(str).str.strip().str.replace('.0', '', regex=False)

# Merge and rename
accrual_updated = accrual_updated.merge(
    location_table[['Prof_Cntr', 'Cost_Cntr']].rename(columns={'Prof_Cntr': 'Profit Center', 'Cost_Cntr': 'Cost Center'}),
    on='Profit Center',
    how='left'
)

# Export final result
accrual_updated.to_excel("June Final Updated Accrual.xlsx", index=False)
