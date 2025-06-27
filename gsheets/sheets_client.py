import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import sys
sys.path.append(r'd:\ai new\growth_intern')
from config import GSHEETS_CREDENTIALS_PATH, GSHEETS_SPREADSHEET_NAME

def get_gsheets_client():
    """
    Authenticates with Google Sheets and returns a client object.
    """
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(GSHEETS_CREDENTIALS_PATH, scope)
        client = gspread.authorize(creds)
        return client
    except FileNotFoundError:
        print(f"Error: The credentials file was not found at {GSHEETS_CREDENTIALS_PATH}")
        print("Please update the path in config.py and ensure the file exists.")
        return None
    except Exception as e:
        print(f"An error occurred during Google Sheets authentication: {e}")
        return None

def write_to_gsheet(spreadsheet_name, worksheet_name, df):
    """
    Writes a DataFrame to a Google Sheet.

    Args:
        spreadsheet_name (str): The name of the Google Sheet.
        worksheet_name (str): The name of the worksheet.
        df (pd.DataFrame): The DataFrame to write.
    """
    client = get_gsheets_client()
    if client:
        try:
            spreadsheet = client.open(spreadsheet_name)
            try:
                worksheet = spreadsheet.worksheet(worksheet_name)
                spreadsheet.del_worksheet(worksheet)
            except gspread.WorksheetNotFound:
                pass # Worksheet doesn't exist, which is fine
            
            worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows=df.shape[0]+1, cols=df.shape[1]+1)
            
            # Convert NaN to empty string
            df_filled = df.fillna('')
            
            worksheet.update([df_filled.columns.values.tolist()] + df_filled.values.tolist())
            print(f"Successfully wrote data to '{worksheet_name}' in '{spreadsheet_name}'.")
        except gspread.exceptions.SpreadsheetNotFound:
            print(f"Error: Spreadsheet '{spreadsheet_name}' not found.")
            print("Please create the spreadsheet and share it with the service account email.")
        except Exception as e:
            print(f"An error occurred while writing to Google Sheets: {e}")

if __name__ == '__main__':
    # Example usage
    # This requires you to have your credentials set up
    if GSHEETS_CREDENTIALS_PATH != "path/to/your/credentials.json":
        # Create a dummy DataFrame
        data = {'col1': [1, 2, 3], 'col2': ['A', 'B', 'C']}
        df = pd.DataFrame(data)
        
        write_to_gsheet(GSHEETS_SPREADSHEET_NAME, 'TestSheet', df)
    else:
        print("Please configure your Google Sheets credentials in config.py to run this example.")
