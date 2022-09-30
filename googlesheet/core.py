from typing import List,Union
import gspread
import pandas as pd

from .creds import get_creds
import time
import json

CREDS = get_creds()
G_CLIENT = gspread.authorize(CREDS)
MASTER_SHEET = "https://docs.google.com/spreadsheets/d/1I-qSO4iNGuQO8_6nWiWZpOO3_pW3dZ3g9iFwIbq4bms/edit#gid=0"




def flatten_json(nested_json, exclude=['']):
    out = {}

    def flatten(x, name='', exclude=exclude):
        if type(x) is dict:
            for a in x:
                if a not in exclude: flatten(x[a], name + a + '/')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '/')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(nested_json)
    return out


def get_input_sheet_values() -> List[List]:

    """
    Get all the reviews link sheets from master google spread sheet
    """

    try:

        spread_sheet = G_CLIENT.open_by_url(MASTER_SHEET)
        sheet = spread_sheet.get_worksheet(0)
        # Call the Sheets API
        profiles = sheet.col_values(1)[1:]
        sheets = sheet.col_values(2)[1:]
        data = list(zip(profiles,sheets))
        # table = pd.DataFrame(sheet.get_all_records())
        # profiles = table['Account Name'].to_list()

        
        if len(data) < 1:
            print('No data found.')
            return []

        result = list(filter(lambda x: len(x[0]) > 1 and x[1].startswith("https")  ,data))
        return result 

    except Exception as e:
        print("couldn't work with master sheet")
        print(e)
        return []


def update_sheet(sheet_link , data):
    try:
        spread_sheet = G_CLIENT.open_by_url(sheet_link)
    except:
        print(f"main working sheet not found: {sheet_link}",)
    
    try:
        sheet = spread_sheet.get_worksheet(0)
    except:
        print(f"sheet not found")
        return

    try:
        json_data = json.loads(data)
        if json_data.get("defects",None):
            json_data = pd.DataFrame([flatten_json(x) for x in json_data['defects']]).fillna('').astype(str)
            sheet.update([json_data.columns.values.tolist()] + json_data.values.tolist())

    except Exception as e:
        print("")
        print(e)
        
    


        

    


