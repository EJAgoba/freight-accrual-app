import streamlit as st
import pandas as pd

from extract_codes import Extractor
from address_merge import CombinedAddress
from address_crossref import Merger
from clean_codes import CodeFormatter
from map_types import TypeMapper, TypeCleaner
from coding_matrix import SPECIAL_TYPE_MAPPINGS, Coding_Matrix
from matrix_map import MatrixMapper
from location_codes import location_codes  # <-- match local script source

# App title
st.title("Freight Accrual Assignment Tool")

st.markdown("""
Upload:
- 📄 **Location Excel File** (e.g., `Coding_CintasLocation 02.06.25.xlsx`)  
- 📄 **Accrual Excel File** (e.g., your accrual workbook)

This version matches your local Python script logic exactly and outputs **Weekly Detail.xlsx**.
""")

# Uploads
location_file = st.file_uploader("Upload Location Excel File", type=["xlsx"])
accrual_file = st.file_uploader("Upload Accrual Excel File", type=["xlsx"])

if location_file and accrual_file:
    try:
        # Read Excel files
        accrual_table = pd.read_excel(accrual_file)
        cintas_location_table = pd.read_excel(location_file)

        # --- Extract Location Codes (same order) ---
        extractor = Extractor()
        extractor.create_columns(accrual_table)
        extractor.lower_columns(accrual_table, 'Consignor', 'Consignee')
        extractor.extract1(accrual_table, 'Consignor', 'Consignor Code', location_codes)
        extractor.extract1(accrual_table, 'Consignee', 'Consignee Code', location_codes)

        # --- Create Combined Address (same columns and casing) ---
        combined_address = CombinedAddress()
        combined_address.create_combined_address_accrual(
            cintas_location_table, 'Combined Address', 'Loc_Address', 'Loc_City', 'Loc_ST'
        )
        combined_address.create_combined_address_accrual(
            accrual_table, 'Consignee Combined Address', 'Dest Address1', 'Dest City', 'Dest State Code'
        )
        combined_address.create_combined_address_accrual(
            accrual_table, 'Consignor Combined Address', 'Origin Addresss', 'Origin City', 'Origin State Code'
        )

        cintas_location_table['Combined Address'] = cintas_location_table['Combined Address'].str.upper()
        accrual_table['Consignee Combined Address'] = accrual_table['Consignee Combined Address'].str.upper()
        accrual_table['Consignor Combined Address'] = accrual_table['Consignor Combined Address'].str.upper()

        # --- Cross reference combined address (same order) ---
        merger = Merger()
        accrual_table = merger.merge(accrual_table, cintas_location_table, 'Consignor Code')
        accrual_table = merger.merge(accrual_table, cintas_location_table, 'Consignee Code')

        # --- Clean up the codes ---
        formatter = CodeFormatter()
        accrual_table = formatter.pad_codes(accrual_table, 'Consignor Code', 'Consignee Code')

        # --- Populate Type Codes (same calls) ---
        type_mapper = TypeMapper()
        accrual_table = type_mapper.map_types(accrual_table, cintas_location_table, 'Consignor Code', 'Consignor Type')
        accrual_table = type_mapper.map_types(accrual_table, cintas_location_table, 'Consignee Code', 'Consignee Type')

        cleaner = TypeCleaner()
        accrual_table = cleaner.fill_non_cintas(accrual_table, 'Consignor Type', 'Consignee Type')

        # --- Profit Center + de-dupe (same as local) ---
        matrix_mapper = MatrixMapper()
        accrual_table['Profit Center'] = accrual_table.apply(matrix_mapper.determine_profit_center, axis=1)
        accrual_table = accrual_table.drop_duplicates(subset=['Invoice Number', 'Paid Amount'])

        # --- Save EXACT filename like your script ---
        output_filename = "Weekly Detail.xlsx"
        from io import BytesIO
        output = BytesIO()
        accrual_table.to_excel(output, index=False)
        output.seek(0)

        st.success(f"✅ Processing complete! Download: {output_filename}")
        st.dataframe(accrual_table.head(20))

        st.download_button(
            label="📥 Download Processed Excel",
            data=output,
            file_name=output_filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"⚠️ Error: {e}")

else:
    st.info("Please upload both the location and accrual Excel files to proceed.")
