from gsheets.sheets_client import write_to_gsheet
import pandas as pd

df = pd.DataFrame({'col1': [1, 2], 'col2': ['A', 'B']})
write_to_gsheet('AlgoTradingLog', 'TestSheet', df)
