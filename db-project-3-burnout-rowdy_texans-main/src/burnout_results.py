"""
CS3810: Principles of Database Systems
Instructor: Thyago Mota
Student(s): William Hellems-Moody, David Carter
Description: Burnout Results
"""

import sys
from datetime import datetime
from helper_functions import get_db_params, yes_no_question, rate_question, date_question
from models import Base, BurnoutQuestion, Surveyee, Result
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

if __name__ == "__main__": 

    # connection to the database (make sure postgres is running!)
    params = get_db_params()
    engine = create_engine(f"postgresql://{params['user']}:{params['passwd']}@{params['host']}:{params['port']}/{params['dbname']}")
    if not engine: 
        print('Couldn\'t conect to the database!')
        sys.exit(1)
    Session = sessionmaker(engine)
    session = Session()

    # TODO #3: show the result of a burnout test previously applied to a surveyee on a specific date ✅

    # VARIABLES 😑

    # Set the question numbers for each category
    signs = [] # Append the signs of burnout
    exhaust_q_list = [1, 4, 7, 10, 13]
    cyn_q_list = [2, 5, 11, 14]
    acad_eff_q_list = [3, 6, 8, 9, 12, 15]
    exhst_sign, cyn_sign, acad_eff_sign = 14, 9, 23 # Burnout Signs 
    exhaustion, cynicism, academic_effectiveness = 0, 0, 0 # Initial values
    reason_arr = ['high exhaustion', 'high cynicism', 'low academic effectiveness'] # Burnout Reason
    question_number = 0 # 🔥 used to track index of the question number 1-15 (which is sequential in the db)

    # LOGIC 🧐
    email = input("What's your email? ") # Get user email & check if user exists
    surveyee = session.query(Surveyee).filter_by(email=email).first()
    if not surveyee:
        print('Surveyee not found!')
        sys.exit(1)
    print(f'Welcome back {surveyee.name}!')

    # Use helper function to get the date of the survey
    date = date_question('When did you take the survey')
    results = session.query(Result).filter_by(surveyee_email=surveyee.email, date=date).all()
    if not results: print('No results found!')
    print('Results:')
    for result in results:

        # Increment the question number for each result then calc if the question number is in the list for each category
        question_number += 1
        if question_number in exhaust_q_list: exhaustion += result.rate
        if question_number in cyn_q_list: cynicism += result.rate
        if question_number in acad_eff_q_list: academic_effectiveness += result.rate

    # Check user has signs of burnout ✅
    if exhaustion > exhst_sign: 
        signs.append(reason_arr[0])
    if cynicism > cyn_sign: 
        signs.append(reason_arr[1])
    if academic_effectiveness < acad_eff_sign: 
        signs.append(reason_arr[2])
    print(f"Based on the results of the survey you took on {date}, you have signs of being exhausted because of {signs}")
    session.close() # close session
