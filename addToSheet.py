import gspread
from oauth2client.service_account import ServiceAccountCredentials

def addToNextRow(name,email,score,Pass):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open("Parking Pass Application (Responses)").worksheet("Accepted")

    # Extract all of the values
    list_of_hashes = sheet.get_all_records()

    nextRow = len(list_of_hashes) + 2
    print(nextRow)

    sheet.update_cell(nextRow,1,name)
    sheet.update_cell(nextRow,2,email)
    sheet.update_cell(nextRow,3,score)
    sheet.update_cell(nextRow,4,Pass)