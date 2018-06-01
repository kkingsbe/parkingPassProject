import gspread
from oauth2client.service_account import ServiceAccountCredentials

def main(person):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    # Make sure you use the right name here.
    sheet = client.open("Parking Pass Application (Responses)").worksheet("Tattler List")

    # Extract all of the values
    list_of_hashes = sheet.get_all_records()

    nextRow = len(list_of_hashes) + 2
    #print(nextRow)

    email = person.get("Enter your first and last name below:")
    name = person.get("Email Address")

    sheet.update_cell(nextRow, 2, name)
    sheet.update_cell(nextRow, 1, email)