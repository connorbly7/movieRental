import pandas as pd

def extract_data():
    """
    Extracts data from CSV files into dataframes usable for transformation and loading

    Returns:
        Resulting dataframes for customers, employees, movies, and rentals

    """
    customers_data = pd.read_csv('movieRental/customer.csv')
    employees_data = pd.read_csv('movieRental/employee.csv')
    movies_data = pd.read_csv('movieRental/movie.csv')
    rentals_data = pd.read_csv('movieRental/rental.csv')
    
    return customers_data, employees_data, movies_data, rentals_data
