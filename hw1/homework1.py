# Homework 1
# Andrea Gomez - akg180000

import sys
import pathlib
import pickle
import re


class Person(object):
    def __init__(self, last, first, mi, id, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.id = id
        self.phone = phone

    # Display employee information
    def displays(self):
        print('\nEmployee id: ', self.id)
        print('\t', self.first, self.mi, self.last)
        print('\t', self.phone)


def process_data(text):
    # create empty dict
    employees_in = {}
    for line in text:
        # split on ',' to get text variables
        last, first, mi, id, phone = line.split(',')

        # Change full name to lower case
        first = first.lower()
        mi = mi.lower()
        last = last.lower()

        # Capitalize name
        first = first.capitalize()
        mi = mi.capitalize()
        last = last.capitalize()

        # if loop to add X if person has no middle name
        if not mi:
            mi = mi.replace('', 'X')

        # create regex object to match the pattern of ID
        id_pattern = re.compile(r'(\w{2})(\d{4})')
        # if id is not in the correct format, prompt user to re-enter & update id with uppercase letters
        if not re.match(id_pattern, id):
            id_replacement = input('Please enter your ID (2 letters followed by 4 numbers)')
            id_replacement = id_replacement.upper()
            id = id_replacement

        # create regex object to change phone number format
        phone = re.sub(r'(\d{3})(\s|\S|-|\.)?(\d{3})(\s|\S|-|\.)?(\d{4})', r'\1-\3-\5', phone)

        #person = Person(last, first, mi, id, phone)
        #employees_in[person]

        employees_in[id] = Person(last, first, mi, id, phone)

    return employees_in


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please enter a filename for system arg")
        quit()

    rel_path = sys.argv[1]
    # read entire file & split on newlines
    with open(pathlib.Path.cwd().joinpath(rel_path), 'r') as f:
        # text_in= string of lists, each string is a line from csv file
        text_in = f.read().splitlines()

    employees = process_data(text_in[1:])

    # pickle the employees
    pickle.dump(employees, open('employees.pickle', 'wb'))

    # read the pickle back in
    employees_in = pickle.load(open('employees.pickle', 'rb'))

    # output employees
    print('\nEmployees lists:')

    for emp_id in employees_in.keys():
        employees_in[emp_id].displays()
