import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os




def load_data(customers, employees, movies, rentals):
    """
        Loads the cleaned data into MySQL as the movierental database
        
        Parameters:
            customers: Cleaned customer data
            employees: Cleaned employee data
            movies: Cleaned movie data
            rentals: Cleaned rental data
    """
    
    load_dotenv()
    username = "root"
    host = "localhost"
    port = 3306
    database = "movierental"
    password = os.getenv("PASSWORD")


    engine = create_engine(f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}")
    
    customers.to_sql("customers", con=engine, if_exists="append", index=False)
    employees.to_sql("employees", con=engine, if_exists="append", index=False)
    movies.to_sql("movies", con=engine, if_exists="append", index=False)
    rentals.to_sql("rentals", con=engine, if_exists="append", index=False)





'''
employees = pd.read_csv("orgPipeline/employee_data2.csv")
employees = clean_employee(employees)

departments = pd.read_csv("orgPipeline/department_data.csv")
projects = pd.read_csv("orgPipeline/projects.csv")
assignments = pd.read_csv("orgPipeline/employee_project.csv")

engine = create_engine(f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}")

departments.to_sql("departments", con=engine, if_exists="append", index=False)
employees.to_sql("employees", con=engine, if_exists="append", index=False)
projects.to_sql("projects", con=engine, if_exists="append", index=False)

assignments = assignments[assignments['employee_id'].isin(employees['employee_id'])]
assignments.to_sql("assignments", con=engine, if_exists="append", index=False)

df = pd.read_sql("SELECT * FROM employees LIMIT 5;", con=engine)
print(df)
'''