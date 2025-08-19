import pandas as pd
from extract_codes import Extractor
from address_merge import CombinedAddress
from address_crossref import Merger
from clean_codes import CodeFormatter
from map_types import TypeMapper, TypeCleaner
from coding_matrix import SPECIAL_TYPE_MAPPINGS, Coding_Matrix
from matrix_map import MatrixMapper
from location_codes import location_codes

accrual_table = pd.read_excel(r"c:\Users\c1354623\OneDrive - Cintas Corporation\Documents\Miscellaneous_Excel_Analysis\A3 Weekly Detail\Weekly Detail.xlsx")
cintas_location_table = pd.read_excel(r"C:\Users\c1354623\OneDrive - Cintas Corporation\Documents\Miscellaneous_Excel_Analysis\Done\New Accrual Logic II\MY LOCATION TABLE.xlsx")

#Extract Location Codes
extractor = Extractor()
extractor.create_columns(accrual_table)
extractor.lower_columns(accrual_table, 'Consignor', 'Consignee')
extractor.extract1(accrual_table, 'Consignor', 'Consignor Code', location_codes)
extractor.extract1(accrual_table, 'Consignee', 'Consignee Code', location_codes)

#Create Combined Address
combined_address = CombinedAddress()
combined_address.create_combined_address_accrual(cintas_location_table, 'Combined Address', 'Loc_Address', 'Loc_City', 'Loc_ST')
combined_address.create_combined_address_accrual(accrual_table, 'Consignee Combined Address', 'Dest Address1', 'Dest City', 'Dest State Code')
combined_address.create_combined_address_accrual(accrual_table, 'Consignor Combined Address', 'Origin Addresss', 'Origin City', 'Origin State Code')
cintas_location_table['Combined Address'] = cintas_location_table['Combined Address'].str.upper()
accrual_table['Consignee Combined Address'] = accrual_table['Consignee Combined Address'].str.upper()
accrual_table['Consignor Combined Address'] = accrual_table['Consignor Combined Address'].str.upper()

#Cross reference the combined address
merger = Merger()
accrual_table = merger.merge(accrual_table, cintas_location_table, 'Consignor Code')
print("Before cleaning, accrual_table type:", type(accrual_table))
accrual_table = merger.merge(accrual_table, cintas_location_table, 'Consignee Code')

#Clean up the codes
formatter = CodeFormatter()
accrual_table = formatter.pad_codes(accrual_table, 'Consignor Code', 'Consignee Code')

#Populate Type Codes
type_mapper = TypeMapper()
accrual_table = type_mapper.map_types(accrual_table, cintas_location_table, 'Consignor Code', 'Consignor Type')
accrual_table = type_mapper.map_types(accrual_table, cintas_location_table, 'Consignee Code', 'Consignee Type')

cleaner = TypeCleaner()
accrual_table = cleaner.fill_non_cintas(accrual_table, 'Consignor Type', 'Consignee Type')

matrix_mapper = MatrixMapper()
accrual_table['Profit Center'] = accrual_table.apply(matrix_mapper.determine_profit_center, axis=1)
accrual_table = accrual_table.drop_duplicates(subset=['Invoice Number', 'Paid Amount'])

accrual_table.to_excel("Weekly Detail-Re-Coded.xlsx", index=False)