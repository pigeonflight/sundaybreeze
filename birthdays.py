from monabreeze import get_people
from utils import get_birthdays
import datetime

# people = get_people_by_tag(tagname="August Birthdays")
people = get_people(details=1)

today = datetime.date.today()
is_sunday = today.weekday() == 6  # Sunday corresponds to 6 in the weekday() method

# Get birthdays for this week or next week based on whether today is Sunday
if is_sunday:
    birthdays = get_birthdays(people)
else:
    birthdays = get_birthdays(people, next_week=True)

# Print the birthdays
for person,birthdate in birthdays:
    formatted_birthdate = birthdate.strftime('%B %d')
    print(f"{person['first_name']} {person['last_name']} has a birthday this week on {formatted_birthdate}.")
