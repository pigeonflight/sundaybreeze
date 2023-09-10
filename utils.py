import datetime

def get_birthdays(entries, next_week=False):
    # Get the current date
    today = datetime.date.today()

    # Calculate the start and end dates for this week or next week
    if next_week:
        if today.weekday() != 6:  # Check if today is not Sunday (0 = Monday, 1 = Tuesday, ..., 6 = Sunday)
            start_of_week = today + datetime.timedelta(days=(6 - today.weekday()))
        else:
            start_of_week = today
    else:
        if today.weekday() != 6:
            start_of_week = today - datetime.timedelta(days=today.weekday())
        else:
            start_of_week = today
    end_of_week = start_of_week + datetime.timedelta(days=6)
    print(f"************************* start of week {start_of_week},end of week: {end_of_week}")
    # Initialize a list to store birthdays for this or next week
    birthdays = []

    # Iterate through the entries and check if the birthdate falls within the selected week
    entries_with_details = [entry for entry in entries if 'birthdate' in entry['details'] or 'birthdate' in entry]
    entries_with_no_birthdate = [entry for entry in entries if 'birthdate' not in entry['details']]
    print(f"************************* count of entries with details: {len(entries_with_details)}")
    
    for entry in entries_with_details:
        print(f"************************* {entry}")
        details = entry['details']
        if 'birthdate' in details:
            print(f"************************* {entry['first_name']}")
            this_year_birthday_str = f"{today.year}{details['birthdate'][4:]}"
        else:
            continue
            # this_year_birthday_str = today.year + entry['birthdate'][4:]
        birthdate = datetime.datetime.strptime(this_year_birthday_str, '%Y-%m-%d').date()
        print(f"************************* birthdate string: {this_year_birthday_str}")
        # birthdate = datetime.datetime.strptime(details['birthdate'], '%Y-%m-%d').date()
        if start_of_week <= birthdate <= end_of_week:
            birthdays.append((entry,birthdate))
        sorted_birthdays = sorted(birthdays, key=lambda x: x[1])  # Sort by birthdate (the second element in each tuple)
    return sorted_birthdays


