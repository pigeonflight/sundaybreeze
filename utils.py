import datetime

def get_birthdays(entries, next_week=False):
    # Get the current date
    today = datetime.date.today()

    # Calculate the start and end dates for this week or next week
    if next_week:
        start_of_week = today + datetime.timedelta(days=(7 - today.weekday()))
        end_of_week = start_of_week + datetime.timedelta(days=6)
    else:
        start_of_week = today - datetime.timedelta(days=today.weekday())
        end_of_week = start_of_week + datetime.timedelta(days=6)

    # Initialize a list to store birthdays for this or next week
    birthdays = []

    # Iterate through the entries and check if the birthdate falls within the selected week
    entries_with_details = [entry for entry in entries if 'birthdate' in entry['details']]
    for entry in entries_with_details:
        details = entry['details']
        birthdate_str = details['birthdate'].replace('0000', '1900')
        birthdate = datetime.datetime.strptime(birthdate_str, '%Y-%m-%d').date()
        # birthdate = datetime.datetime.strptime(details['birthdate'], '%Y-%m-%d').date()
        if start_of_week <= birthdate <= end_of_week:
            birthdays.append((entry,birthdate))

    return birthdays

# Example data
data = [
    {
        "last_name": "Samuels",
        "first_name": "Sadaka",
        "birthdate": "2012-08-11"
    },
    {
        "last_name": "Stewart",
        "first_name": "Chelsea",
        "birthdate": "0000-08-31"
    },
    {
        "last_name": "Stewart",
        "first_name": "Tyefah",
        "birthdate": "0000-08-20"
    }
]


