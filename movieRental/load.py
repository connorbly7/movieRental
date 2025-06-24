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