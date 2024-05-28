"""
CS3810: Principles of Database Systems
Instructor: Thyago Mota
Student(s): William Hellems-Moody, David Carter
Description: Helper functions
"""

import configparser as cp
from datetime import datetime

# reads the db configuration file and returns the params dictionary
def get_db_params() -> dict:
    config = cp.RawConfigParser()
    # assuming config.ini is in src and script is running from the folder right above src
    config.read('src/config.ini') 
    return dict(config.items('db'))

# display a y/n question until the user enters a valid answer
# returns true/false depending whether the user answered yes or no, respectively
def yes_no_question(question: str) -> bool:
    question = question.strip()
    if question[-1] == '?':
        question = question[:-1]
    answer = None
    while answer != 'Y' and answer != 'N': 
        answer = input(f'{question} [Y|N]? ').upper()
        answer = 'Y' if answer == 'YES' or answer == 'Y' else answer
        answer = 'N' if answer == 'NO' or answer == 'N' else answer
    return answer == 'Y'    

# displays a rating question until the user enters a number in [min_rate,max_rate]
# returns the rate read
def rate_question(question: str, min_rate: int, max_rate: int) -> int:
    question = question.strip()
    rate = -1
    while rate < min_rate or rate > max_rate: 
        try:
            rate = int(input(f'{question} [{min_rate}|{max_rate}]? '))
        except: 
            rate = -1
            pass
    return rate

# returns true/false depending whether the given string is in the format 'YYYY-MM-DD'
def is_valid_date_format(date_str: str) -> bool:
    format = "%Y-%m-%d"
    try:
        return bool(datetime.strptime(date_str, format))
    except ValueError:
        return False

# display a question that reads a date until the date is in the format 'YYYY-MM-DD'
# returns the date as a string
def date_question(question: str) -> str:
    question = question.strip()
    date_str = ''
    while not is_valid_date_format(date_str):
        date_str = input(f'{question} [YYYY-MM-DD]? ')
    return date_str