import pandas as pd
import numpy as np


def transform_data(customers, employees, movies, rentals):
    """
        Cleans the data by filling null values, creating new columns, and deleting rows as needed
        
        Parameters:
            customers: Dataframe containing customer data
            employees: Dataframe containing employee data
            movies: Dataframe containing movie data
            rentals: Dataframe containing rental data

        Returns:
            Cleaned dataframes for customers, employees, movies, and rentals
    """

    ## Creates a copy of the dataframe to avoid modifying the original data
    customers = customers.copy()

    ## Drops rows where customer_id is null
    customers = customers.dropna(subset=['customer_id'])

    ## Fills null values in customer_fname, customer_lname, customer_email, and customer_phone with "Unknown"
    customers["customer_fname"] = customers["customer_fname"].fillna("Unknown")
    customers["customer_lname"] = customers["customer_lname"].fillna("Unknown")
    customers["customer_email"] = customers["customer_email"].fillna("Unknown")
    customers["customer_phone"] = customers["customer_phone"].fillna("Unknown")

    # Casts 'customer_id' back to an int
    customers['customer_id'] = customers['customer_id'].astype(int)
    customers.to_csv("movieRental/cleaned_customer.csv", index=False)

    ## Creates a copy of the dataframe to avoid modifying the original data
    employees = employees.copy()

    ## Drops rows where employee_id is null
    employees = employees.dropna(subset=['employee_id'])

    ## Fills null values in employee_fname and employee_lname with "Unknown"
    employees["employee_fname"] = employees["employee_fname"].fillna("Unknown")
    employees["employee_lname"] = employees["employee_lname"].fillna("Unknown")

    ## Fills null values in role with "Not Assigned"
    employees["role"] = employees["role"].fillna("Not Assigned")

    ## Fills null values in salary with the mean salary
    employees["salary"] = employees["salary"].fillna(round(employees["salary"].mean(), 2))

    ## Creates days_since_hire column, calculating the number of days since the employee was hired, or returning NaN if hire_date is null
    employees['days_since_hire'] = np.where(pd.notna(employees['hire_date']),
                                            (pd.Timestamp.now() - pd.to_datetime(employees['hire_date'], errors='coerce')).dt.days, np.nan)

    ## Fills null values in employee_email and employee_phone with "Unknown"
    employees["employee_email"] = employees["employee_email"].fillna("Unknown")
    employees["employee_phone"] = employees["employee_phone"].fillna("Unknown")

    ## Casts employee_id back to an int
    employees['employee_id'] = employees['employee_id'].astype(int)

    employees.to_csv("movieRental/cleaned_employee.csv", index=False)

    ## Creates a copy of the dataframe to avoid modifying the original data
    movies = movies.copy()

    ## Drops rows where movie_id or title is null
    movies = movies.dropna(subset=['movie_id', 'title'])

    ## Fills null values in genre, release_date, and rating with "Unknown"
    movies['genre'] = movies['genre'].fillna("Unknown")
    movies['release_date'] = movies['release_date'].fillna("Unknown")
    movies['rating'] = movies['rating'].fillna("Unknown")
    
    ## Converts release_date to correct datetime format
    movies['release_date'] = pd.to_datetime(movies['release_date'], errors='coerce')
    
    ## Fills null runtime values with -1
    movies['runtime'] = movies['runtime'].fillna(-1)

    ## Casts movie_id back to an int
    movies['movie_id'] = movies['movie_id'].astype(int)

    ## Casts runtime back to int
    movies['runtime'] = movies['runtime'].astype(int)

    movies.to_csv("movieRental/cleaned_movie.csv", index=False)

    ## Creates a copy of the dataframe to avoid modifying the original data
    rentals = rentals.copy()

    ## Drops rows where rental_id is null
    rentals = rentals.dropna(subset=['rental_id'])

    ## Converts rental_id back to int
    rentals['rental_id'] = rentals['rental_id'].astype(int)

    ## Fills null values in customer_id, employee_id, and movie_id with -1
    rentals['customer_id'] = rentals['customer_id'].fillna(-1).astype(int)
    rentals['employee_id'] = rentals['employee_id'].fillna(-1).astype(int)
    rentals['movie_id'] = rentals['movie_id'].fillna(-1).astype(int)

    ## Converts rental_date to correct datetime format
    rentals['rental_date'] = pd.to_datetime(rentals['rental_date'], format='%Y-%m-%d', errors='coerce')

    ## Converts due_date to correct datetime format
    rentals['due_date'] = pd.to_datetime(rentals['due_date'], format='%Y-%m-%d', errors='coerce')

    ## Converts return_date to correct datetime format
    rentals['return_date'] = pd.to_datetime(rentals['return_date'], format='%Y-%m-%d', errors='coerce')

    ## Fills null values in rental_fee with -1
    rentals['rental_fee'] = rentals['rental_fee'].fillna(-1)

    ## Adds is_overdue column to indicate if the rental is overdue
    rentals['is_overdue'] = np.where((pd.notna(rentals['due_date'])) & pd.notna(rentals['rental_date']) & ((rentals['return_date'] > rentals['due_date']) | (rentals['return_date'].isna())),
                                    True, False)
    
    ## Adds days_overdue column to calculate the number of days the rental is overdue when the rental has been returned
    rentals['days_overdue'] = np.where((rentals['is_overdue']) & (pd.notna(rentals['return_date'])) & (pd.notna(rentals['due_date'])) & pd.notna(rentals['rental_date']),
                                        (rentals['return_date'] - rentals['due_date']).dt.days, 0).astype(int)

    ## Adds days_overdue column to calculate the number of days the rental is overdue when the rental has not been returned
    rentals['days_overdue'] = np.where((rentals['is_overdue']) & (pd.isna(rentals['return_date'])) & (pd.notna(rentals['due_date'])) & pd.notna(rentals['rental_date']),
                                        (pd.Timestamp.now() - rentals['due_date']).dt.days, rentals['days_overdue']).astype(int)

    ## Adds daily_overdue_fee column
    rentals['daily_overdue_fee'] = round(rentals['rental_fee'] * .10, 2)

    ## Adds total_overdue_fee column, calculating the total overdue fee based on days overdue and daily overdue fee
    rentals['total_overdue_fee'] = round(rentals['days_overdue'] * rentals['daily_overdue_fee'], 2)

    rentals.to_csv("movieRental/cleaned_rental.csv", index=False)

    return customers, employees, movies, rentals

