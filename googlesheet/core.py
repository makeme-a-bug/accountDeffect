from typing import List,Union
import gspread
import pandas as pd

from .creds import get_creds
import time

CREDS = get_creds()
G_CLIENT = gspread.authorize(CREDS)
MASTER_SHEET = "https://docs.google.com/spreadsheets/d/1I-qSO4iNGuQO8_6nWiWZpOO3_pW3dZ3g9iFwIbq4bms/edit#gid=0"



def get_input_sheet_values() -> List[List]:

    """
    Get all the reviews link sheets from master google spread sheet
    """

    try:

        spread_sheet = G_CLIENT.open_by_url(MASTER_SHEET)
        sheet = spread_sheet.get_worksheet(0)
        # Call the Sheets API
        profiles = sheet.col_values(1)
        table = sheet.get_values()
        table = pd.DataFrame(table[1:],columns=['Account Name',"JSON"]+[f"JSON{i-1}" for i in range(3,len(table[0])+1)])
        # table = pd.DataFrame(sheet.get_all_records())
        # profiles = table['Account Name'].to_list()
        
        
        if len(profiles) < 1:
            print('No data found.')
            return []

        result = list(filter(lambda x: len(x) > 1 ,profiles))
        return result 

    except Exception as e:
        print("couldn't work with master sheet")
        print(e)
        return []


def update_sheet(profile_name , data):
    try:
        spread_sheet = G_CLIENT.open_by_url(MASTER_SHEET)
    except:
        print(f"main working sheet not found: {MASTER_SHEET}",)
    
    try:
        sheet = spread_sheet.get_worksheet(0)
    except:
        print(f"sheet not found")
        return
    table = sheet.get_values()
    table = pd.DataFrame(table[1:],columns=['Account Name',"JSON"]+[f"JSON{i-1}" for i in range(3,len(table[0])+1)])
    profiles = table['Account Name'].to_list()
    index = profiles.index(profile_name) + 2
    print(len(data))
    col = 2
    batch = 1
    for i in range(2,len(table.columns)+2):
        sheet.update_cell(index, i, "")
        time.sleep(1)

    for i in range(0,len(data),50000):
        print(i,batch*50000)
        print(len(data[i:batch*50000]))
        sheet.update_cell(index, col, data[i:batch*50000])
        col += 1
        batch +=1
        time.sleep(1)
    time.sleep(5)
    print(col)


        

    


