import datetime
import csv
import os
import re

DATE_FORMAT = "%m/%d/%y"


class Entry:
    work_done = ""
    date = None
    time = None
    comments = ""

    def __init__(self, work_done, date, time, comments=""):
        self.work_done = work_done
        self.date = date
        self.time = time
        self.comments = comments

    def to_string(self):
        return "{} on {}. Took {} minutes. {}".format(self.work_done,
                                                      datetime.datetime.strftime(self.date, DATE_FORMAT),
                                                      self.time,
                                                      self.comments)


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def verify_int(prompt):
    success = False
    while not success:
        try:
            result = int(input(prompt))
        except ValueError:
            print("Please enter the number of your choice...")
        else:
            success = True

    return result


# TODO: Update with all (or most common) possible formats
def user_friendly_date(date_format):
    friendly_date = date_format
    friendly_date = friendly_date.replace("%d", "DD")
    friendly_date = friendly_date.replace("%m", "MM")
    friendly_date = friendly_date.replace("%y", "YY")
    friendly_date = friendly_date.replace("%Y", "YYYY")

    return friendly_date


def verify_date(prompt, date_format):
    success = False
    while not success:
        try:
            result = datetime.datetime.strptime(input(prompt), date_format)
        except ValueError:
            print("Please enter the date in a {} format.".format(user_friendly_date(date_format)))
        else:
            success = True

    return result


def input_new_entry():
    work_done = input("Please enter the work done: ")
    date = verify_date("Please enter the date {} took place (MM/DD/YY): ".format(work_done), DATE_FORMAT)
    time = input("Please enter the time in minutes that {} took: ".format(work_done))
    comments = input("Please enter any extra comments (optional): ")
    return Entry(work_done, date, time, comments)


def search_by_date(some_entries, search_date):
    entries_by_date = []
    for entry in some_entries:
        if entry.date == search_date:
            entries_by_date.append(entry)

    return entries_by_date


def edit_entry(an_entry):
    current_data = "Current: {}"
    new_data_prompt = "What would you like to change {} to? "
    success = "{} updated!"
    editing = True
    while editing:
        print("What would you like to edit?")
        print("1. Work done")
        print("2. Date")
        print("3. Time worked")
        print("4. Comments")
        print("5. Nothing, go back")
        choice = verify_int("> ")

        if choice == 1:
            print(current_data.format(an_entry.work_done))
            new_data = input(new_data_prompt.format("work done"))
            an_entry.work_done = new_data
            cls()
            print(success.format("Work done"))
        elif choice == 2:
            print(current_data.format(datetime.datetime.strftime(an_entry.date, DATE_FORMAT)))
            new_data = verify_date(new_data_prompt.format("date"), DATE_FORMAT)
            an_entry.date = new_data
            cls()
            print(success.format("Date"))
        elif choice == 3:
            print(current_data.format(an_entry.time))
            new_data = verify_int(new_data_prompt.format("time worked (in minutes)"))
            an_entry.time = new_data
            cls()
            print(success.format("Time worked"))
        elif choice == 4:
            print(current_data.format(an_entry.comments))
            new_data = input(new_data_prompt.format("comments"))
            an_entry.comments = new_data
            cls()
            print(success.format("Comments"))
        elif choice == 5:
            editing = False
        else:
            print("Please enter your choice between 1 and 5.")


def enter():
    input("Please press enter to continue")


def search_entries(some_entries):
    search_menu = {1: "date",
                   2: "date range",
                   3: "time spent",
                   4: "search title or comments",
                   5: "regex pattern (advanced)",
                   6: "main menu"}
    print("Here are your search options:")
    for item in search_menu:
        print("{}. {}".format(item, search_menu[item]))
    search_type = verify_int("Please enter the number of your chosen search type: ")

    choosing = True
    while choosing:
        if search_type == 1:
            choosing = False
            dates = []
            for entry in some_entries:
                if entry.date not in dates:
                    dates.append(entry.date)
            print("Here are the dates with entries: ")
            for index, date in enumerate(dates, 1):
                print("{}. {}".format(index, datetime.datetime.strftime(date, DATE_FORMAT)))
            selection = verify_int("Please enter the number of the date you would like to view entries for: ")
            results = search_by_date(some_entries, dates[selection - 1])

            page_entries(results, some_entries)

        elif search_type == 2:
            choosing = False
            date_1 = verify_date("Please enter the beginning of your desired date range: ", DATE_FORMAT)
            date_2 = verify_date("Please enter the end of your desired date range: ", DATE_FORMAT)
            results = []
            for entry in some_entries:
                if date_2 > entry.date > date_1:
                    results.append(entry)

            page_entries(results, some_entries)

        elif search_type == 3:
            choosing = False
            time_query = verify_int("Please enter the time spent you would like to search entries for: ")
            results = []
            for entry in some_entries:
                if entry.time == time_query:
                    results.append(entry)

            page_entries(results, some_entries)

        elif search_type == 4:
            choosing = False
            search_phrase = input("Please enter the phrase you would like to search with: ")
            results = []
            for entry in some_entries:
                if search_phrase in entry.work_done or search_phrase in entry.comments:
                    results.append(entry)

            page_entries(results, some_entries)

        elif search_type == 5:
            choosing = False
            regex = input("Please enter the regex pattern you would like to search by: ")
            results = []
            for entry in some_entries:
                if re.search(regex, entry.work_done) or re.search(regex, entry.comments):
                    results.append(entry)

            page_entries(results, some_entries)

        elif search_type == 6:
            choosing = False

        else:
            search_type = verify_int("Please select a proper menu selection (1 - 6): ")


def page_entries(results, some_entries):
    entry_index = 0
    loop = True
    while loop:
        if len(results) == 0:
            print("No entries found!")
            loop = False
            enter()
        elif entry_index == -1:
            entry_index = len(results) - 1
        elif entry_index == len(results):
            entry_index = 0
        else:
            options = "(P) Previous entry | (E) Edit current entry | (D) Delete current entry | (M) Main menu | " \
                      "(N) Next entry"
            cls()
            print("Result {} of {}:".format(entry_index + 1, len(results)))
            print(results[entry_index].to_string())
            print(options)
            choice = input("> ").lower()
            choosing = True
            while choosing:
                if choice == 'p':
                    entry_index -= 1
                    choosing = False
                elif choice == 'e':
                    edit_entry(results[entry_index])
                    choosing = False
                elif choice == 'd':
                    deleted_entry = results[entry_index]
                    results.remove(deleted_entry)
                    some_entries.remove(deleted_entry)
                    entry_index -= 1
                    choosing = False
                elif choice == 'm':
                    choosing = False
                    loop = False
                elif choice == 'n':
                    entry_index += 1
                    choosing = False
                else:
                    print("Please enter the letter corresponding with your desired option.")
                    print(options)
                    choice = input("> ").lower()


def main():
    menu = {1: "Add entry", 2: "Search entries", 3: "Quit"}
    online = True
    entries = []
    try:
        with open("entries.csv", newline='') as entries_file:
            rows = csv.DictReader(entries_file)
            for row in rows:
                entries.append(Entry(work_done=row["work done"],
                                     date=datetime.datetime.strptime(row["date"], DATE_FORMAT),
                                     time=int(row["time"]),
                                     comments=row["comments"]))
    except FileNotFoundError:
        print("No 'entries.csv' file found. No entries imported.")
        with open("entries.csv", 'w', newline='') as entries_file:
            field_names = ["work done", "date", "time", "comments"]
            writer = csv.DictWriter(entries_file, field_names)
            writer.writeheader()

    while online:
        print("Welcome to the work log! Here's what you can do:")
        for item in menu:
            print("{}. {}".format(item, menu[item]))
        choice = verify_int("Enter the number of which choice you would like: ")

        if choice == 1:
            new_entry = input_new_entry()
            entries.append(new_entry)
            with open('entries.csv', 'a', newline='') as entries_file:
                writer = csv.writer(entries_file)
                writer.writerow([new_entry.work_done,
                                 datetime.datetime.strftime(new_entry.date, DATE_FORMAT),
                                 new_entry.time,
                                 new_entry.comments])
            print("Entry added successfully!")
            enter()
            cls()

        elif choice == 2:
            if len(entries) == 0:
                print("No entries! Please add one before searching.")
            else:
                search_entries(entries)

        elif choice == 3:
            print("Saving...")
            with open('entries.csv', 'w', newline='') as entries_file:
                field_names = ["work done", "date", "time", "comments"]
                writer = csv.DictWriter(entries_file, field_names)
                writer.writeheader()
                for entry in entries:
                    writer.writerow({'work done': entry.work_done,
                                     'date': datetime.datetime.strftime(entry.date, DATE_FORMAT),
                                     'time': entry.time,
                                     'comments': entry.comments})
            print("Entries saved!")
            online = False


if __name__ == '__main__':
    main()
