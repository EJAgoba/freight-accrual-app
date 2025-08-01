from coding_matrix import SPECIAL_TYPE_MAPPINGS, Coding_Matrix

SPECIAL_CODES = {'0K35', '024P', '067N'}

class MatrixMapper:
    def determine_profit_center(self, row):
        if row['Consignee Code'] in SPECIAL_CODES:
            return row['Consignee Code']
        
        key = (row['Consignor Type'], row['Consignee Type'])
        
        if key in SPECIAL_TYPE_MAPPINGS:
            return SPECIAL_TYPE_MAPPINGS[key]
        
        if key in Coding_Matrix:
            direction = Coding_Matrix[key]
            if direction == "ORIGIN":
                return row['Consignor Code']
            elif direction == "DESTINATION":
                return row['Consignee Code']
        
        return 'UNKNOWN'
    





















































































































































