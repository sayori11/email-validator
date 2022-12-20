import json

def get_disposable_emails():
    with open('files/disposable-emails.json', 'r') as f:
        emails = json.loads(f.read())
    return emails