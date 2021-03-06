from operator import itemgetter
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def main():
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open("Parking Pass Application (Responses)").worksheet("Accepted")

    # Extract all of the values
    list_of_hashes = sheet.get_all_records()
    unsortedList = []

    # Compile list of scores
    for row in range(len(list_of_hashes)):
        scoreRowTuple = row + 1, list_of_hashes[row].get("Score")  # (row,score)
        unsortedList.append(scoreRowTuple)
    print(unsortedList)

    # Sort the scores
    sortedList = sorted(unsortedList, key=itemgetter(1), reverse=True)
    print(sortedList)
    sortedHashes = []

    for sortTup in sortedList:
        for row in range(len(list_of_hashes)):
            if list_of_hashes[row].get("Score") == sortTup[1]:
                sortedHashes.append(list_of_hashes[row])
                list_of_hashes.pop(row)
                break

    print(sortedHashes)
    for row in range(len(sortedHashes)):
        print(sortedHashes[row])
        for col in range(len(sortedHashes[row])):
            sheet.update_cell(row + 2, col + 1, sortedHashes[row].get(list(sortedHashes[row].keys())[col]))
