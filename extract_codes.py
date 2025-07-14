import re
import numpy as np

class Extractor:
    def create_columns(self, df):
        df[['Consignor Code', 'Consignor Type', 'Consignee Code', 'Consignee Type']] = ""
        df['Consignor Type'] = df['Consignor Type'].astype(str).str.strip().str.upper()
        df['Consignee Type'] = df['Consignee Type'].astype(str).str.strip().str.upper()
        df['Consignor Code'] = df['Consignor Code'].astype(str).str.strip().str.upper()
        df['Consignee Code'] = df['Consignee Code'].astype(str).str.strip().str.upper()
    def lower_columns(self, df, *columns):
        for i in columns:
            df[i] = df[i].astype(str).str.lower()
    def extract1(self, df, column1, new_column, location_codes):
        location_patterns = [re.escape(str(x).lower()) for x in location_codes]
    
        # Create regex pattern to match whole words or exact phrases
        search_pattern = r'\b(' + '|'.join(location_patterns) + r')\b'  # \b ensures whole word match
        
        mask = df[column1].astype(str).str.contains(r'cintas|millennium', case = False, na = False)
        # Extract the first matching location code
        df.loc[mask, new_column] = df.loc[mask, column1].astype(str).str.extract(search_pattern, expand=False)

        df[new_column] = df[new_column].replace("", np.nan)
    
    
