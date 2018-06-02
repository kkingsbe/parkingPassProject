import json

def main(name):
    with open('administrators.json', 'r') as f:
        admins = json.load(f)

    for admin in admins:
        if admin["Name"] == name:
            return admin["Email"]