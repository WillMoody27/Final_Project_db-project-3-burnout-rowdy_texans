"""
CS3810: Principles of Database Systems
Instructor: Thyago Mota
Student(s): William Hellems-Moody, David Carter
Description: Test Application
"""
# Update 4-27-2024 ✅: Code Refactored (D.R.Y. Principle) & Added Functionality to allow user to retake the test and update db for every additional survey attempt.

import sys
from datetime import datetime
from helper_functions import get_db_params, yes_no_question, rate_question
from models import Base, BurnoutQuestion, Surveyee, Result
from sqlalchemy import create_engine
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

    # tables creation from the model
    Base.metadata.create_all(engine)

    # TODO #2: apply a burnout test to a surveyee and save the test results in the database; you should also save the surveyee's information if it is the first time that the test is being administered to them

    '''
    NOTE: 
     - Add the functionality to allow user to retake the test and update the queries as the user cannot take the test again if they have already taken it that day.
    '''

    # Function For Questions
    def ask_question(email): 
        # Get the questions and save the results
        print('Please rate the questions using a scale from 0 (never) to 6 (always).')
        questions = session.query(BurnoutQuestion).all() # Get all the questions from the db
        
        # Check if results exists for the email
        results_exists = session.query(Result).filter_by(surveyee_email=email).all()
    
        # Update ratings and dates for existing results ✓
        if results_exists:
            for quest in questions:
                # Removed indcies since using enhanced for loop (4-27-2024) ✅
                rate = rate_question(quest.description, 0, 6)
                session.query(Result).filter_by(surveyee_email=email, question_number=quest.number).update({Result.rate: rate, Result.date: datetime.now()})
            session.commit()

        else:
            # Add new results for the email
            for quest in questions:
                rate = rate_question(quest.description, 0, 6)
                session.add(Result(question_number=quest.number, surveyee_email=email, date=datetime.now(), rate=rate))
            session.commit()

    # Function For Welcome Back & Re-Taking Survey
    def welcome_back(surveyee, email, survey_date):
        # Welcome User Back To Survey
        print(f'Welcome back {surveyee.name}, you have already taken the test on {survey_date}.')
        res = yes_no_question('Do you want to retake the test?')
        if res: 
            ask_question(email) # Retake
        else: 
            print('Bye!') # Don't Retake

            
    # Get surveyee's email
    print('Welcome to the Burnout Test!')
    while True:
        res = yes_no_question('Is this the first time you are taking this test?')
        email = input('What is your email? ')
        surveyee = session.query(Surveyee).filter_by(email=email).first()
        
        survey_date = session.query(Result.date).filter_by(surveyee_email=email).order_by(Result.date.desc()).first()

        # Check if survey_date exists and set it to the first element in the tuple, else set it to None
        if survey_date:
            survey_date = survey_date[0]
        else:
            survey_date = None

        if res: # Yes - Y
            if surveyee:
                # Email exists -> they've taken before ask for retake
                welcome_back(surveyee, email, survey_date)
                break
            else:
                # They dont exist -> Add them to the db
                name = input('What is your name? ')
                session.add(Surveyee(email=email, name=name))
            ask_question(email)
            break
        else: # No - N
            if surveyee:
                # Email exists -> they've taken before ask for retake
                welcome_back(surveyee, email, survey_date)
                break
            else:
                print('Survey not found!')
                break
            
    session.close()


